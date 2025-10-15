import os
import numpy as np
import cv2
import json
from tensorflow.keras.models import load_model

class WasteClassifier:
    def __init__(self, model_path=None):
        """
        Initialize the WasteClassifier with model and category information.

        Args:
            model_path: Path to the trained model file. If None, uses default path.
        """
        # Use relative path from current file location
        if model_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            model_path = os.path.join(base_dir, 'models', 'waste_classifier_model.h5')

        self.model_path = model_path

        # Load class indices if available
        class_indices_path = os.path.join(
            os.path.dirname(model_path),
            'class_indices.json'
        )

        if os.path.exists(class_indices_path):
            with open(class_indices_path, 'r') as f:
                class_indices = json.load(f)
                # Reverse the mapping (index -> class_name)
                self.waste_categories = {v: k for k, v in class_indices.items()}
        else:
            # Fallback to hardcoded categories
            self.waste_categories = {
                0: 'battery',     1: 'biological',  2: 'brown-glass',
                3: 'cardboard',   4: 'clothes',     5: 'green-glass',
                6: 'metal',       7: 'paper',       8: 'plastic',
                9: 'shoes',      10: 'trash',      11: 'white-glass'
            }

        # Detailed recommendations for each category
        self.recommendations = {
            'battery': [
                'Never throw batteries in regular trash',
                'Take to designated e-waste collection centers',
                'Many electronics stores accept old batteries',
                'Rechargeable batteries can be reused multiple times'
            ],
            'biological': [
                'Compost at home if possible',
                'Use for organic fertilizer production',
                'Keep separate from other waste types',
                'Avoid mixing with plastics or metals'
            ],
            'brown-glass': [
                'Rinse before recycling',
                'Remove caps and lids',
                'Keep separate from other glass colors',
                'Can be recycled infinitely without quality loss'
            ],
            'cardboard': [
                'Flatten boxes to save space',
                'Keep dry for better recycling',
                'Remove tape and labels when possible',
                'Cardboard is highly recyclable'
            ],
            'clothes': [
                'Donate wearable clothes to charity',
                'Recycle at textile collection bins',
                'Repurpose into cleaning rags',
                'Avoid throwing in regular trash'
            ],
            'green-glass': [
                'Rinse thoroughly before disposal',
                'Separate from other glass types',
                'Remove metal caps and corks',
                'Green glass is 100% recyclable'
            ],
            'metal': [
                'Clean metal containers before recycling',
                'Aluminum cans are infinitely recyclable',
                'Steel cans can be recycled with magnets',
                'Metal recycling saves significant energy'
            ],
            'paper': [
                'Keep paper dry and clean',
                'Shred confidential documents',
                'Remove plastic windows from envelopes',
                'Paper can be recycled 5-7 times'
            ],
            'plastic': [
                'Check recycling number on the bottom',
                'Rinse containers before recycling',
                'Remove caps (often different plastic type)',
                'Avoid single-use plastics when possible'
            ],
            'shoes': [
                'Donate wearable pairs to charity',
                'Drop at shoe recycling programs',
                'Some manufacturers accept old shoes',
                'Can be repurposed into sports surfaces'
            ],
            'trash': [
                'Minimize non-recyclable waste',
                'Consider if items can be repurposed',
                'Dispose in designated trash bins',
                'Reduce consumption to minimize waste'
            ],
            'white-glass': [
                'Most valuable glass for recycling',
                'Keep completely separate from colored glass',
                'Remove all caps, lids, and corks',
                'Rinse thoroughly before disposal'
            ]
        }

        # Environmental impact information
        self.environmental_impact = {
            'battery': 'Batteries contain toxic materials that can contaminate soil and water. Proper disposal prevents environmental damage and allows material recovery.',
            'biological': 'Composting organic waste reduces methane emissions from landfills and creates nutrient-rich soil. Returns valuable nutrients to the earth.',
            'brown-glass': 'Recycling glass saves 30% energy compared to making new glass. Every ton of glass recycled saves 300kg of CO2 emissions.',
            'cardboard': 'Recycling cardboard saves 17 trees per ton and reduces water usage by 50%. Prevents deforestation and conserves resources.',
            'clothes': 'Textile recycling prevents 1.5 million tons of waste annually. Reduces water pollution from textile production by up to 90%.',
            'green-glass': 'Glass recycling saves raw materials and energy. One recycled bottle saves enough energy to power a computer for 25 minutes.',
            'metal': 'Recycling aluminum saves 95% of the energy needed to make new aluminum. Steel recycling saves 60% energy and reduces mining impact.',
            'paper': 'Recycling one ton of paper saves 17 trees, 7000 gallons of water, and 4000 kW of energy. Reduces landfill waste significantly.',
            'plastic': 'Plastic recycling reduces ocean pollution and saves fossil fuels. Every ton recycled saves 5,774 kWh of energy.',
            'shoes': 'Shoe recycling prevents toxic materials from landfills. Recycled materials can be used for sports tracks, playground surfaces.',
            'trash': 'Non-recyclable waste in landfills produces methane. Minimizing trash through reduction and reuse is most impactful.',
            'white-glass': 'Clear glass is essential for food containers and medical uses. 100% recyclable without quality degradation.'
        }

        # Load the model
        self.model = self._load_model()
        self.img_size = (128, 128)  # Match training size

    def _load_model(self):
        """Load the trained Keras model."""
        try:
            print(f"[INFO] Loading model from {self.model_path}...")
            model = load_model(self.model_path)
            print("[INFO] Model loaded successfully!")
            return model
        except Exception as e:
            print(f"[ERROR] Failed to load model: {e}")
            return None

    def preprocess_image(self, image_path):
        """
        Preprocess image for model prediction.

        Args:
            image_path: Path to the image file

        Returns:
            Preprocessed image array ready for prediction
        """
        try:
            # Read image
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError(f"Could not load image from {image_path}")

            # Convert BGR to RGB
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Resize to model input size
            img = cv2.resize(img, self.img_size)

            # Normalize to [0, 1]
            img = img.astype(np.float32) / 255.0

            # Add batch dimension
            img = np.expand_dims(img, axis=0)

            return img
        except Exception as e:
            raise ValueError(f"Error preprocessing image: {str(e)}")

    def classify(self, image_path, top_k=3):
        """
        Classify waste image and return predictions with recommendations.

        Args:
            image_path: Path to the image file
            top_k: Number of top predictions to return (default: 3)

        Returns:
            Dictionary containing classification results compatible with app.py
        """
        if self.model is None:
            raise RuntimeError("Model not loaded. Cannot perform classification.")

        try:
            # Preprocess image
            processed_img = self.preprocess_image(image_path)

            # Make prediction
            predictions = self.model.predict(processed_img, verbose=0)[0]

            # Get top k predictions
            top_indices = np.argsort(predictions)[-top_k:][::-1]

            # Get the top prediction details
            top_class = self.waste_categories[top_indices[0]]
            top_confidence = float(predictions[top_indices[0]])

            # Prepare results in the format expected by app.py
            results = {
                'waste_type': top_class,
                'confidence': top_confidence,
                'recommendations': self.recommendations.get(
                    top_class,
                    ['Dispose properly']
                ),
                'environmental_impact': self.environmental_impact.get(
                    top_class,
                    'Proper disposal helps protect the environment'
                ),
                'all_predictions': [
                    {
                        'class': self.waste_categories[idx],
                        'confidence': float(predictions[idx])
                    }
                    for idx in top_indices
                ]
            }

            return results

        except Exception as e:
            raise RuntimeError(f"Classification failed: {str(e)}")

    def batch_classify(self, image_paths, top_k=3):
        """
        Classify multiple images at once.

        Args:
            image_paths: List of image file paths
            top_k: Number of top predictions per image

        Returns:
            List of classification results
        """
        results = []
        for img_path in image_paths:
            try:
                result = self.classify(img_path, top_k=top_k)
                results.append({'success': True, 'result': result})
            except Exception as e:
                results.append({
                    'success': False,
                    'error': str(e),
                    'image_path': img_path
                })
        return results

    def get_category_info(self, category_name):
        """Get detailed information about a specific waste category."""
        if category_name not in self.recommendations:
            return None

        return {
            'category': category_name,
            'recommendations': self.recommendations[category_name],
            'environmental_impact': self.environmental_impact[category_name]
        }

# Example usage
if __name__ == "__main__":
    # Initialize classifier
    classifier = WasteClassifier()

    # Test on a single image
    test_image = "path/to/test/image.jpg"

    if os.path.exists(test_image):
        result = classifier.classify(test_image)
        print("\nClassification Result:")
        print(f"Class: {result['waste_type']}")
        print(f"Confidence: {result['confidence']:.2%}")
        print(f"\nRecommendations:")
        for rec in result['recommendations']:
            print(f"  - {rec}")
