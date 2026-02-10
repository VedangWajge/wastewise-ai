from flask import Blueprint, request, jsonify
import os
import uuid
from datetime import datetime

# Import simplified classifier
from models.unified_classifier import WasteClassifier
from config.ai_config import AIConfig

ai_bp = Blueprint("ai_bp", __name__, url_prefix='/api/ai')

# Initialize classifier once
_classifier = None

def get_classifier():
    """Get classifier instance (singleton)"""
    global _classifier
    if _classifier is None:
        _classifier = WasteClassifier()
    return _classifier

@ai_bp.route("/predict", methods=["POST"])
def predict():
    """Classify waste from uploaded image"""
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

        # Classify using classifier
        classifier = get_classifier()
        print(f"[AI-ROUTES] Running classification...")

        result = classifier.classify(temp_path)
        print(f"[AI-ROUTES] Classification successful: {result.get('waste_type')} ({result.get('confidence'):.2%})")

        # Get recommendations
        recommendations = classifier.get_recommendations(result['waste_type'])

        # Clean up temp file
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except PermissionError:
                import time
                time.sleep(0.1)
                try:
                    os.remove(temp_path)
                except:
                    pass

        # Format response
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
        # Clean up temp file on error
        if os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass

        error_msg = str(e)
        if "Model not found" in error_msg:
            error_msg = "AI model file not found. Please ensure waste_model.pkl exists in models directory."
        elif "Failed to load model" in error_msg:
            error_msg = "Failed to load AI model. Please check model file integrity."

        return jsonify({
            "success": False,
            "error": error_msg,
            "message": "Classification failed. Please check AI model configuration."
        }), 500

@ai_bp.route("/test", methods=["GET"])
def test_endpoint():
    """Test endpoint to check if AI service is working"""
    model_available = AIConfig.is_model_available()
    
    return jsonify({
        "success": True,
        "message": "AI service is running",
        "model_available": model_available,
        "model_path": AIConfig.LOCAL_MODEL_PATH
    })
