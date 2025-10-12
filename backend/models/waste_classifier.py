import numpy as np
import cv2
from tensorflow.keras.models import load_model

class WasteClassifier:
    def __init__(self):
        self.model_path = r"D:\WasteWiseAi\wastewise-ai\backend\models\garbage_cnn_model.h5"
        self.waste_categories = {
            0: 'battery',     1: 'biological',  2: 'brown-glass',
            3: 'cardboard',   4: 'clothes',     5: 'green-glass',
            6: 'metal',       7: 'paper',       8: 'plastic',
            9: 'shoes',      10: 'trash',      11: 'white-glass'
        }
        self.recommendations = {
            cat: [f"Dispose of {cat} properly"]
            for cat in self.waste_categories.values()
        }
        self.environmental_impact = {
            cat: f"Impact info for {cat}"
            for cat in self.waste_categories.values()
        }
        self.model = self._load_model()

    def _load_model(self):
        try:
            print(f"[INFO] Loading model from {self.model_path} ...")
            model = load_model(self.model_path)
            print("[INFO] Model loaded successfully!")
            return model
        except Exception as e:
            print(f"[ERROR] Failed to load model: {e}")
            return None

    def preprocess_image(self, image_path):
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError("Could not load image")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (128, 128))           # ← match your training size
        img = img.astype(np.float32) / 255.0
        return np.expand_dims(img, axis=0)