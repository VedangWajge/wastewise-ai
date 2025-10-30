"""
AI Model Configuration
Centralized configuration for waste classification AI models
Supports: Local Model, Hugging Face, Google Gemini, OpenAI
"""

import os
from enum import Enum
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AIProvider(Enum):
    """Available AI providers for waste classification"""
    LOCAL = "local"  # Your trained model
    HUGGINGFACE = "huggingface"  # Hugging Face Inference API
    GEMINI = "gemini"  # Google Gemini Vision API
    OPENAI = "openai"  # OpenAI GPT-4 Vision API

class AIConfig:
    """Configuration for AI classification"""

    # Select which AI provider to use (can be changed easily)
    ACTIVE_PROVIDER = AIProvider.GEMINI  # LOCAL or HUGGINGFACE, GEMINI, OPENAI

    # Fallback provider if primary fails
    FALLBACK_PROVIDER = AIProvider.LOCAL  # Changed from HUGGINGFACE to LOCAL due to API permissions

    # Local Model Configuration
    LOCAL_MODEL_PATH = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'models',
        'waste_classifier_model.h5'
    )
    LOCAL_MODEL_INPUT_SIZE = (128, 128)

    # Hugging Face Configuration
    HUGGINGFACE_API_KEY = os.environ.get('HUGGINGFACE_API_KEY', '')
    # Using image-to-text models since they work better with free-tier API
    HUGGINGFACE_MODEL = 'nlpconnect/vit-gpt2-image-captioning'
    # Alternative models that work with free tier:
    # - 'Salesforce/blip-image-captioning-base'
    # - 'nlpconnect/vit-gpt2-image-captioning'
    HUGGINGFACE_API_URL = f"https://api-inference.huggingface.co/models/{HUGGINGFACE_MODEL}"

    # Google Gemini Configuration
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
    GEMINI_MODEL = 'gemini-2.0-flash-exp'  # Updated to valid model name

    # OpenAI Configuration
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
    OPENAI_MODEL = 'gpt-4o'  # or 'gpt-4-vision-preview'

    # Classification Settings
    CONFIDENCE_THRESHOLD = 0.3  # Minimum confidence to accept classification
    TOP_K_PREDICTIONS = 3  # Number of top predictions to return

    # Waste Categories (standardized across all providers)
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
    def get_api_key(cls, provider: AIProvider) -> str:
        """Get API key for specified provider"""
        if provider == AIProvider.HUGGINGFACE:
            return cls.HUGGINGFACE_API_KEY
        elif provider == AIProvider.GEMINI:
            return cls.GEMINI_API_KEY
        elif provider == AIProvider.OPENAI:
            return cls.OPENAI_API_KEY
        return ""

    @classmethod
    def is_provider_configured(cls, provider: AIProvider) -> bool:
        """Check if provider is properly configured"""
        if provider == AIProvider.LOCAL:
            return os.path.exists(cls.LOCAL_MODEL_PATH)
        else:
            api_key = cls.get_api_key(provider)
            return bool(api_key and api_key.strip())

    @classmethod
    def switch_provider(cls, provider: AIProvider):
        """Switch to a different AI provider"""
        if cls.is_provider_configured(provider):
            cls.ACTIVE_PROVIDER = provider
            return True
        return False

    @classmethod
    def get_provider_info(cls):
        """Get information about current provider configuration"""
        return {
            'active_provider': cls.ACTIVE_PROVIDER.value,
            'fallback_provider': cls.FALLBACK_PROVIDER.value,
            'providers_status': {
                'local': cls.is_provider_configured(AIProvider.LOCAL),
                'huggingface': cls.is_provider_configured(AIProvider.HUGGINGFACE),
                'gemini': cls.is_provider_configured(AIProvider.GEMINI),
                'openai': cls.is_provider_configured(AIProvider.OPENAI)
            }
        }
