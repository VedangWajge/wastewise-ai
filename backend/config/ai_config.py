"""
AI Model Configuration
Simple configuration for waste classification using FastAI model
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AIConfig:
    """Configuration for AI classification"""

    # Local Model Configuration (FastAI .pkl model)
    LOCAL_MODEL_PATH = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'models',
        'waste_model.pkl'
    )

    # Classification Settings
    CONFIDENCE_THRESHOLD = 0.3  # Minimum confidence to accept classification
    TOP_K_PREDICTIONS = 3  # Number of top predictions to return

    # Waste Categories (standardized)
    WASTE_CATEGORIES = [
        'battery', 'biological', 'brown-glass', 'cardboard',
        'clothes', 'green-glass', 'metal', 'paper',
        'plastic', 'shoes', 'trash', 'white-glass'
    ]

    # Mapping to your app's waste types
    CATEGORY_MAPPING = {
        'battery': 'e-waste',
        'biological': 'organic',
        'brown-glass': 'glass',
        'cardboard': 'paper',
        'clothes': 'textile',
        'green-glass': 'glass',
        'metal': 'metal',
        'paper': 'paper',
        'plastic': 'plastic',
        'shoes': 'textile',
        'trash': 'general',
        'white-glass': 'glass'
    }

    @classmethod
    def is_model_available(cls) -> bool:
        """Check if model file exists"""
        return os.path.exists(cls.LOCAL_MODEL_PATH)