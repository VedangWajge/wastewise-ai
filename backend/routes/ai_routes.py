from flask import Blueprint, request, jsonify
import os
import uuid
from datetime import datetime

# Import unified classifier
from models.unified_classifier import UnifiedWasteClassifier
from config.ai_config import AIConfig, AIProvider

ai_bp = Blueprint("ai_bp", __name__, url_prefix='/api/ai')

# Initialize classifier (recreate each request to pick up config changes)
def get_classifier():
    """Get a fresh classifier instance"""
    return UnifiedWasteClassifier()

@ai_bp.route("/predict", methods=["POST"])
def predict():
    """Classify waste from uploaded image using configured AI provider"""
    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image = request.files["image"]

    # Generate unique filename
    temp_filename = f"temp_{uuid.uuid4().hex}.jpg"
    temp_path = os.path.join("uploads", temp_filename)

    # Create uploads directory if it doesn't exist
    os.makedirs("uploads", exist_ok=True)

    try:
        # Save uploaded image
        image.save(temp_path)
        print(f"[AI-ROUTES] Image saved to: {temp_path}")

        # Classify using unified classifier (create fresh instance)
        classifier = get_classifier()
        print(f"[AI-ROUTES] Classifier initialized with provider: {classifier.provider.value}")

        result = classifier.classify(temp_path)
        print(f"[AI-ROUTES] Classification successful: {result.get('waste_type')} ({result.get('confidence'):.2%})")

        # Get recommendations
        recommendations = classifier.get_recommendations(result['waste_type'])

        # Clean up temp file (with retry for Windows file locking)
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except PermissionError:
                # Windows file locking issue - file will be cleaned up later
                import time
                time.sleep(0.1)
                try:
                    os.remove(temp_path)
                except:
                    pass  # File will be cleaned up on next run

        # Format response to match frontend expectations
        # Convert all_predictions array to object format
        all_predictions_obj = {}
        all_predictions_list = result.get('all_predictions', [])
        if isinstance(all_predictions_list, list):
            for pred in all_predictions_list:
                if isinstance(pred, dict) and 'class' in pred and 'confidence' in pred:
                    all_predictions_obj[pred['class']] = pred['confidence']
                elif isinstance(pred, dict) and 'mapped_type' in pred and 'confidence' in pred:
                    all_predictions_obj[pred['mapped_type']] = pred['confidence']

        classification = {
            'waste_type': result['waste_type'],
            'raw_category': result.get('raw_category'),
            'confidence': result['confidence'],
            'provider_used': result.get('provider_used', 'unknown'),
            'fallback_used': result.get('fallback', False),
            'recommendations': recommendations,
            'environmental_impact': f"Proper disposal of {result['waste_type']} helps protect the environment",
            'all_predictions': all_predictions_obj
        }

        return jsonify({
            "success": True,
            "classification": classification,
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        # Clean up temp file on error (with retry for Windows file locking)
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass  # File cleanup failed, will be cleaned up later

        # Provide more detailed error information
        error_msg = str(e)
        if "google-generativeai" in error_msg:
            error_msg = "Gemini API package not installed. Please run: pip install google-generativeai"
        elif "GEMINI_API_KEY" in error_msg or "API key" in error_msg:
            error_msg = "AI provider API key not configured. Please check your .env file."
        elif "All AI providers failed" in error_msg:
            error_msg = "All AI providers failed. Please check: 1) API keys are set, 2) google-generativeai is installed, 3) Local model exists"

        return jsonify({
            "success": False,
            "error": error_msg,
            "message": "Classification failed. Please check AI provider configuration.",
            "provider_status": AIConfig.get_provider_info()
        }), 500

@ai_bp.route("/providers", methods=["GET"])
def get_providers():
    """Get information about available AI providers"""
    return jsonify({
        "success": True,
        "provider_info": AIConfig.get_provider_info()
    })

@ai_bp.route("/switch-provider", methods=["POST"])
def switch_provider():
    """Switch to a different AI provider"""
    data = request.get_json()
    provider_name = data.get('provider', '').lower()

    try:
        # Map string to enum
        provider_map = {
            'local': AIProvider.LOCAL,
            'huggingface': AIProvider.HUGGINGFACE,
            'gemini': AIProvider.GEMINI,
            'openai': AIProvider.OPENAI
        }

        if provider_name not in provider_map:
            return jsonify({
                "success": False,
                "error": f"Invalid provider. Choose from: {list(provider_map.keys())}"
            }), 400

        provider = provider_map[provider_name]

        # Check if provider is configured
        if not AIConfig.is_provider_configured(provider):
            return jsonify({
                "success": False,
                "error": f"Provider '{provider_name}' is not configured. Please set API keys in environment variables."
            }), 400

        # Switch provider
        AIConfig.switch_provider(provider)

        # Provider switched successfully
        # Next request will use the new provider via get_classifier()

        return jsonify({
            "success": True,
            "message": f"Switched to {provider_name} provider",
            "active_provider": AIConfig.ACTIVE_PROVIDER.value
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@ai_bp.route("/test", methods=["GET"])
def test_endpoint():
    """Test endpoint to check if AI service is working"""
    return jsonify({
        "success": True,
        "message": "AI service is running",
        "active_provider": AIConfig.ACTIVE_PROVIDER.value,
        "provider_status": AIConfig.get_provider_info()
    })
