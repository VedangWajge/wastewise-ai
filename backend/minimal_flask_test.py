"""
Minimal Flask app to test AI endpoint
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Add to path
sys.path.insert(0, os.path.dirname(__file__))

from models.unified_classifier import UnifiedWasteClassifier
from config.ai_config import AIConfig

app = Flask(__name__)
CORS(app)

os.makedirs('uploads', exist_ok=True)

@app.route('/test', methods=['GET'])
def test():
    return jsonify({
        "status": "OK",
        "provider_info": AIConfig.get_provider_info()
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Test the AI prediction endpoint"""
    try:
        print("[DEBUG] Predict endpoint called")

        if 'image' not in request.files:
            print("[DEBUG] No image in request")
            return jsonify({"error": "No image file provided"}), 400

        image = request.files['image']
        print(f"[DEBUG] Image received: {image.filename}")

        # Save temp file
        temp_path = os.path.join('uploads', 'temp_test.jpg')
        image.save(temp_path)
        print(f"[DEBUG] Image saved to: {temp_path}")

        # Try to classify
        print("[DEBUG] Creating classifier...")
        classifier = UnifiedWasteClassifier()
        print(f"[DEBUG] Classifier created with provider: {classifier.provider.value}")

        print("[DEBUG] Starting classification...")
        result = classifier.classify(temp_path)
        print(f"[DEBUG] Classification result: {result}")

        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)
            print("[DEBUG] Temp file cleaned up")

        return jsonify({
            "success": True,
            "result": result
        })

    except Exception as e:
        print(f"[ERROR] Exception occurred: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()

        return jsonify({
            "success": False,
            "error": str(e),
            "error_type": type(e).__name__
        }), 500

if __name__ == '__main__':
    print("Starting minimal Flask test server...")
    print(f"Provider info: {AIConfig.get_provider_info()}")
    app.run(host='localhost', port=5001, debug=True)
