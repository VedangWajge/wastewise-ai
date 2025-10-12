from flask import Blueprint, request, jsonify
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import os

# Import your model functions
from models.garbage_model import predict_waste_category  # use your actual function name

ai_bp = Blueprint("ai_bp", __name__)

# Load your saved model
model_path = "models/garbage_classification_model_inception.h5"
model = load_model(model_path)

@ai_bp.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image = request.files["image"]
    image_path = "temp_image.jpg"
    image.save(image_path)

    try:
        predicted_category, probability = predict_waste_category(image_path, model)
        os.remove(image_path)
        return jsonify({
            "predicted_category": predicted_category,
            "probability": float(probability)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
