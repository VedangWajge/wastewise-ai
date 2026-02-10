"""
FastAI Provider for Waste Classification
Uses a local .pkl model file trained with FastAI
"""

from fastai.vision.all import load_learner
import os


class FastAIProvider:
    """FastAI-based waste classifier using local .pkl model"""
    
    def __init__(self):
        """Initialize the FastAI learner from the .pkl model file"""
        model_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "models",
            "waste_model.pkl"
        )
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"FastAI model not found at {model_path}")
        
        print(f"[INFO] Loading FastAI model from {model_path}")
        self.learner = load_learner(model_path)
        print(f"[INFO] FastAI model loaded successfully")
    
    def classify(self, image_path):
        """
        Classify waste image using FastAI model
        
        Args:
            image_path: Path to the image file
            
        Returns:
            dict: Classification results with provider, labels, and probabilities
        """
        # Run prediction
        pred_class, pred_idx, outputs = self.learner.predict(image_path)
        
        # Get all class labels from the model
        labels = self.learner.dls.vocab
        
        # Threshold for multi-label detection
        threshold = 0.5
        
        # Get all labels above threshold
        detected = [labels[i] for i, p in enumerate(outputs) if p > threshold]
        
        # If no labels above threshold, use the top prediction
        if not detected:
            detected = [str(pred_class)]
        
        return {
            "provider": "fastai",
            "labels": detected,
            "probabilities": outputs.tolist()
        }
