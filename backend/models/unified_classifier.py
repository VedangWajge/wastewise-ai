"""
Waste Classifier using FastAI
Fixed version (handles dtype error + stable inference)
"""

import os
import sys
from fastai.vision.all import load_learner, PILImage
import pathlib

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config.ai_config import AIConfig


class WasteClassifier:
    """
    Waste classifier using FastAI model
    """

    def __init__(self):
        """Initialize classifier with FastAI model"""
        self.config = AIConfig
        self.model = None
        self._load_model()

    def _load_model(self):
        """Load FastAI model from .pkl file"""
        try:
            if os.name == 'nt':
                posix_backup = pathlib.PosixPath
                try:
                    pathlib.PosixPath = pathlib.WindowsPath

                    model_path = self.config.LOCAL_MODEL_PATH

                    if not os.path.exists(model_path):
                        raise FileNotFoundError(f"Model not found at {model_path}")

                    print(f"[INFO] Loading FastAI model from {model_path}")
                    self.model = load_learner(model_path)
                    print(f"[INFO] Model loaded successfully")

                finally:
                    pathlib.PosixPath = posix_backup
            else:
                model_path = self.config.LOCAL_MODEL_PATH

                if not os.path.exists(model_path):
                    raise FileNotFoundError(f"Model not found at {model_path}")

                print(f"[INFO] Loading FastAI model from {model_path}")
                self.model = load_learner(model_path)
                print(f"[INFO] Model loaded successfully")

        except Exception as e:
            print(f"[ERROR] Failed to load model: {e}")
            raise

    def classify(self, image_path, top_k=None):
        """
        Classify waste image
        """
        if not self.model:
            raise RuntimeError("Model not loaded")

        top_k = top_k or self.config.TOP_K_PREDICTIONS

        try:
            # ✅ FIX: Always convert to FastAI PILImage
            img = PILImage.create(image_path)

            # Run prediction safely
            pred_class, pred_idx, outputs = self.model.predict(img)

            labels = self.model.dls.vocab
            probabilities = outputs.tolist()

            # Pair labels with probabilities
            predictions_list = [
                (labels[i], probabilities[i]) for i in range(len(labels))
            ]

            # Sort by confidence
            predictions_list.sort(key=lambda x: x[1], reverse=True)

            # Top predictions
            top_predictions = predictions_list[:top_k]
            top_class = top_predictions[0][0]
            top_confidence = top_predictions[0][1]

            return {
                'waste_type': self.config.CATEGORY_MAPPING.get(top_class, top_class),
                'raw_category': str(top_class),
                'confidence': float(top_confidence),
                'all_predictions': [
                    {
                        'class': str(label),
                        'mapped_type': self.config.CATEGORY_MAPPING.get(label, label),
                        'confidence': float(prob)
                    }
                    for label, prob in top_predictions
                ]
            }

        except Exception as e:
            print(f"[ERROR] Classification failed: {e}")
            raise

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


# Test
if __name__ == "__main__":
    classifier = WasteClassifier()

    test_image = "test_waste.jpg"

    if os.path.exists(test_image):
        result = classifier.classify(test_image)
        print("\nClassification Result:")
        print(f"Waste Type: {result['waste_type']}")
        print(f"Confidence: {result['confidence']:.2%}")
    else:
        print(f"Test image not found: {test_image}")
        print(f"\nModel available: {AIConfig.is_model_available()}")