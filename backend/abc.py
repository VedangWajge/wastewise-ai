print("[INFO] Starting model load...")

from tensorflow.keras.models import load_model

model_path = "D:\WasteWiseAi\wastewise-ai\backend\models\garbage_cnn_model.h5"

try:
    model = load_model(model_path)
    print("[INFO] Model loaded successfully!")
    print(model.summary())
except Exception as e:
    print(f"[ERROR] Failed to load model: {e}")
