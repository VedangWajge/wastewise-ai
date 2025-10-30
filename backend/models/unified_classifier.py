"""
Unified Waste Classifier
Supports multiple AI backends: Local Model, Hugging Face, Gemini, OpenAI
Easy switching between providers via configuration
"""

import os
import sys
import base64
import requests
import numpy as np
from PIL import Image
import io

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config.ai_config import AIConfig, AIProvider


class UnifiedWasteClassifier:
    """
    Unified classifier that can use multiple AI backends
    Automatically falls back to alternative provider if primary fails
    """

    def __init__(self, provider=None):
        """
        Initialize classifier with specified provider

        Args:
            provider: AIProvider enum value (if None, uses config default)
        """
        self.config = AIConfig
        self.provider = provider or self.config.ACTIVE_PROVIDER

        # Initialize provider-specific components
        self.local_model = None
        if self.provider == AIProvider.LOCAL:
            self._load_local_model()

    def _load_local_model(self):
        """Load local TensorFlow/Keras model"""
        try:
            from tensorflow.keras.models import load_model
            import cv2

            model_path = self.config.LOCAL_MODEL_PATH
            if os.path.exists(model_path):
                self.local_model = load_model(model_path)
                self.cv2 = cv2
                print(f"[INFO] Local model loaded from {model_path}")
            else:
                print(f"[WARNING] Local model not found at {model_path}")
        except Exception as e:
            print(f"[ERROR] Failed to load local model: {e}")
            self.local_model = None

    def classify(self, image_path, top_k=None):
        """
        Classify waste image using configured AI provider

        Args:
            image_path: Path to image file
            top_k: Number of top predictions (default from config)

        Returns:
            dict: Classification results with waste_type, confidence, etc.
        """
        top_k = top_k or self.config.TOP_K_PREDICTIONS

        try:
            # Try primary provider
            result = self._classify_with_provider(image_path, self.provider, top_k)
            if result:
                result['provider_used'] = self.provider.value
                return result

        except Exception as e:
            print(f"[WARNING] Primary provider ({self.provider.value}) failed: {e}")

        # Try fallback provider
        try:
            fallback = self.config.FALLBACK_PROVIDER
            if fallback != self.provider and self.config.is_provider_configured(fallback):
                print(f"[INFO] Trying fallback provider: {fallback.value}")
                result = self._classify_with_provider(image_path, fallback, top_k)
                if result:
                    result['provider_used'] = fallback.value
                    result['fallback'] = True
                    return result
        except Exception as e:
            print(f"[ERROR] Fallback provider also failed: {e}")

        raise RuntimeError("All AI providers failed. Please check configuration.")

    def _classify_with_provider(self, image_path, provider, top_k):
        """Route to appropriate classification method based on provider"""
        if provider == AIProvider.LOCAL:
            return self._classify_local(image_path, top_k)
        elif provider == AIProvider.HUGGINGFACE:
            return self._classify_huggingface(image_path, top_k)
        elif provider == AIProvider.GEMINI:
            return self._classify_gemini(image_path, top_k)
        elif provider == AIProvider.OPENAI:
            return self._classify_openai(image_path, top_k)
        else:
            raise ValueError(f"Unknown provider: {provider}")

    def _classify_local(self, image_path, top_k):
        """Classify using local TensorFlow model"""
        if not self.local_model:
            raise RuntimeError("Local model not loaded")

        # Preprocess image
        img = self.cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Could not load image from {image_path}")

        img = self.cv2.cvtColor(img, self.cv2.COLOR_BGR2RGB)
        img = self.cv2.resize(img, self.config.LOCAL_MODEL_INPUT_SIZE)
        img = img.astype(np.float32) / 255.0
        img = np.expand_dims(img, axis=0)

        # Predict
        predictions = self.local_model.predict(img, verbose=0)[0]

        # Get top predictions
        top_indices = np.argsort(predictions)[-top_k:][::-1]

        waste_categories = self.config.WASTE_CATEGORIES
        top_class = waste_categories[top_indices[0]]
        top_confidence = float(predictions[top_indices[0]])

        return {
            'waste_type': self.config.CATEGORY_MAPPING.get(top_class, top_class),
            'raw_category': top_class,
            'confidence': top_confidence,
            'all_predictions': [
                {
                    'class': waste_categories[idx],
                    'mapped_type': self.config.CATEGORY_MAPPING.get(waste_categories[idx], waste_categories[idx]),
                    'confidence': float(predictions[idx])
                }
                for idx in top_indices
            ]
        }

    def _classify_huggingface(self, image_path, top_k):
        """Classify using Hugging Face Inference API"""
        api_key = self.config.HUGGINGFACE_API_KEY
        if not api_key:
            raise ValueError("HUGGINGFACE_API_KEY not configured")

        # Read and encode image
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        headers = {"Authorization": f"Bearer {api_key}"}

        # Try image classification endpoint
        response = requests.post(
            self.config.HUGGINGFACE_API_URL,
            headers=headers,
            data=image_bytes,
            timeout=30
        )

        if response.status_code == 403:
            raise RuntimeError("Hugging Face API permission error. Please check your API token permissions or upgrade to Pro tier.")

        if response.status_code != 200:
            raise RuntimeError(f"Hugging Face API error ({response.status_code}): {response.text[:500]}")

        results = response.json()

        # Parse results - find best matching waste category
        best_match = self._match_to_waste_categories(results[:top_k])

        return best_match

    def _classify_gemini(self, image_path, top_k):
        """Classify using Google Gemini Vision API"""
        api_key = self.config.GEMINI_API_KEY
        if not api_key:
            raise ValueError("GEMINI_API_KEY not configured")

        try:
            import google.generativeai as genai
        except ImportError:
            raise ImportError("Install google-generativeai: pip install google-generativeai")

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(self.config.GEMINI_MODEL)

        # Load image into memory to avoid file locking issues on Windows
        with Image.open(image_path) as img:
            # Create a copy in memory so we can close the file handle
            img = img.copy()

        # Create prompt for waste classification
        prompt = f"""Analyze this image and classify the waste type.

Available categories: {', '.join(self.config.WASTE_CATEGORIES)}

Respond in this EXACT JSON format:
{{
    "waste_type": "most likely category from the list",
    "confidence": 0.95,
    "reasoning": "brief explanation"
}}"""

        # Generate content
        response = model.generate_content([prompt, img])

        # Parse response
        import json
        import re

        # Extract JSON from response
        text = response.text
        json_match = re.search(r'\{[^}]+\}', text, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            waste_type = result.get('waste_type', 'trash')
            confidence = result.get('confidence', 0.7)

            return {
                'waste_type': self.config.CATEGORY_MAPPING.get(waste_type, waste_type),
                'raw_category': waste_type,
                'confidence': confidence,
                'reasoning': result.get('reasoning', ''),
                'all_predictions': [
                    {
                        'class': waste_type,
                        'mapped_type': self.config.CATEGORY_MAPPING.get(waste_type, waste_type),
                        'confidence': confidence
                    }
                ]
            }

        raise ValueError("Could not parse Gemini response")

    def _classify_openai(self, image_path, top_k):
        """Classify using OpenAI GPT-4 Vision API"""
        api_key = self.config.OPENAI_API_KEY
        if not api_key:
            raise ValueError("OPENAI_API_KEY not configured")

        # Encode image to base64
        with open(image_path, "rb") as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')

        # Determine image type
        ext = os.path.splitext(image_path)[1].lower()
        mime_type = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }.get(ext, 'image/jpeg')

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        payload = {
            "model": self.config.OPENAI_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"""Analyze this image and classify the waste type.

Available categories: {', '.join(self.config.WASTE_CATEGORIES)}

Respond in this EXACT JSON format:
{{
    "waste_type": "most likely category from the list",
    "confidence": 0.95,
    "reasoning": "brief explanation"
}}"""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{image_data}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }

        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )

        if response.status_code != 200:
            raise RuntimeError(f"OpenAI API error: {response.text}")

        result = response.json()
        content = result['choices'][0]['message']['content']

        # Parse JSON response
        import json
        import re

        json_match = re.search(r'\{[^}]+\}', content, re.DOTALL)
        if json_match:
            parsed = json.loads(json_match.group())
            waste_type = parsed.get('waste_type', 'trash')
            confidence = parsed.get('confidence', 0.7)

            return {
                'waste_type': self.config.CATEGORY_MAPPING.get(waste_type, waste_type),
                'raw_category': waste_type,
                'confidence': confidence,
                'reasoning': parsed.get('reasoning', ''),
                'all_predictions': [
                    {
                        'class': waste_type,
                        'mapped_type': self.config.CATEGORY_MAPPING.get(waste_type, waste_type),
                        'confidence': confidence
                    }
                ]
            }

        raise ValueError("Could not parse OpenAI response")

    def _match_to_waste_categories(self, hf_results):
        """Match Hugging Face generic labels to waste categories"""
        # This is a simple keyword matching - can be enhanced
        category_keywords = {
            'plastic': ['plastic', 'bottle', 'container', 'bag', 'packaging'],
            'paper': ['paper', 'cardboard', 'newspaper', 'magazine', 'book'],
            'metal': ['metal', 'can', 'aluminum', 'steel', 'iron'],
            'glass': ['glass', 'bottle', 'jar'],
            'organic': ['food', 'organic', 'fruit', 'vegetable', 'compost'],
            'e-waste': ['electronics', 'battery', 'phone', 'computer', 'device'],
        }

        for result in hf_results:
            label = result.get('label', '').lower()
            score = result.get('score', 0)

            for category, keywords in category_keywords.items():
                if any(kw in label for kw in keywords):
                    return {
                        'waste_type': category,
                        'raw_category': label,
                        'confidence': score,
                        'all_predictions': [
                            {'class': r.get('label'), 'confidence': r.get('score')}
                            for r in hf_results
                        ]
                    }

        # Default to trash if no match
        return {
            'waste_type': 'general',
            'raw_category': hf_results[0].get('label') if hf_results else 'unknown',
            'confidence': hf_results[0].get('score', 0.5) if hf_results else 0.5,
            'all_predictions': [
                {'class': r.get('label'), 'confidence': r.get('score')}
                for r in hf_results
            ]
        }

    def get_recommendations(self, waste_type):
        """Get disposal recommendations for waste type"""
        recommendations = {
            'plastic': [
                'Check recycling number on the bottom',
                'Rinse containers before recycling',
                'Remove caps (often different plastic type)',
                'Avoid single-use plastics when possible'
            ],
            'paper': [
                'Keep paper dry and clean',
                'Remove plastic windows from envelopes',
                'Flatten cardboard boxes',
                'Paper can be recycled 5-7 times'
            ],
            'metal': [
                'Clean metal containers before recycling',
                'Aluminum cans are infinitely recyclable',
                'Steel cans can be recycled with magnets',
                'Metal recycling saves significant energy'
            ],
            'glass': [
                'Rinse thoroughly before disposal',
                'Remove caps and lids',
                'Can be recycled infinitely without quality loss'
            ],
            'organic': [
                'Compost at home if possible',
                'Use for organic fertilizer production',
                'Keep separate from other waste types'
            ],
            'e-waste': [
                'Never throw in regular trash',
                'Take to designated e-waste collection centers',
                'Many electronics stores accept old devices'
            ],
            'textile': [
                'Donate wearable items to charity',
                'Recycle at textile collection bins',
                'Repurpose into cleaning rags'
            ],
            'general': [
                'Minimize non-recyclable waste',
                'Consider if items can be repurposed',
                'Dispose in designated trash bins'
            ]
        }

        return recommendations.get(waste_type, recommendations['general'])


# Example usage and testing
if __name__ == "__main__":
    # Initialize classifier
    classifier = UnifiedWasteClassifier()

    # Test image path
    test_image = "test_waste.jpg"

    if os.path.exists(test_image):
        result = classifier.classify(test_image)
        print("\nClassification Result:")
        print(f"Provider: {result.get('provider_used')}")
        print(f"Waste Type: {result['waste_type']}")
        print(f"Confidence: {result['confidence']:.2%}")
        if 'reasoning' in result:
            print(f"Reasoning: {result['reasoning']}")
    else:
        print(f"Test image not found: {test_image}")
        print("\nAvailable providers:")
        print(AIConfig.get_provider_info())
