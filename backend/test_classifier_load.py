import sys
import traceback

try:
    from models.unified_classifier import WasteClassifier
    print("[TEST] Import successful")
    
    classifier = WasteClassifier()
    print("[TEST] Classifier initialized successfully!")
    print(f"[TEST] Model type: {type(classifier.model)}")
    
except Exception as e:
    print(f"[ERROR] Failed: {e}")
    print("\nFull traceback:")
    traceback.print_exc()
    sys.exit(1)
