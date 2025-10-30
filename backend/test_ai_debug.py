"""
Debug script to test AI classification
"""
import os
import sys
from PIL import Image
import io

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from models.unified_classifier import UnifiedWasteClassifier
from config.ai_config import AIConfig

def create_test_image():
    """Create a simple test image"""
    img = Image.new('RGB', (100, 100), color='red')
    test_path = 'test_image_temp.jpg'
    img.save(test_path)
    return test_path

def test_classifier():
    """Test the unified classifier"""
    print("=" * 60)
    print("AI CLASSIFIER DIAGNOSTIC TEST")
    print("=" * 60)

    # Check configuration
    print("\n1. Configuration Status:")
    print("-" * 60)
    provider_info = AIConfig.get_provider_info()
    print(f"Active Provider: {provider_info['active_provider']}")
    print(f"Fallback Provider: {provider_info['fallback_provider']}")
    print("\nProvider Status:")
    for provider, status in provider_info['providers_status'].items():
        status_str = 'Configured' if status else 'Not Configured'
        print(f"  {provider}: {status_str}")

    # Create test image
    print("\n2. Creating Test Image:")
    print("-" * 60)
    test_image = create_test_image()
    print(f"[OK] Test image created: {test_image}")

    # Test classifier
    print("\n3. Testing Classifier:")
    print("-" * 60)
    try:
        classifier = UnifiedWasteClassifier()
        print(f"[OK] Classifier initialized with provider: {classifier.provider.value}")

        print("\n4. Running Classification:")
        print("-" * 60)
        result = classifier.classify(test_image)

        print("\n[SUCCESS] CLASSIFICATION SUCCESSFUL!")
        print(f"  Waste Type: {result['waste_type']}")
        print(f"  Confidence: {result['confidence']:.2%}")
        print(f"  Provider Used: {result.get('provider_used', 'unknown')}")
        print(f"  Fallback Used: {result.get('fallback', False)}")

        if 'reasoning' in result:
            print(f"  Reasoning: {result['reasoning']}")

        # Cleanup
        if os.path.exists(test_image):
            os.remove(test_image)

        return True

    except Exception as e:
        print(f"\n[ERROR] ERROR OCCURRED:")
        print(f"  Error Type: {type(e).__name__}")
        print(f"  Error Message: {str(e)}")

        import traceback
        print("\nFull Traceback:")
        print("-" * 60)
        traceback.print_exc()

        # Cleanup
        if os.path.exists(test_image):
            os.remove(test_image)

        return False

if __name__ == "__main__":
    success = test_classifier()
    print("\n" + "=" * 60)
    print(f"Test Result: {'PASSED' if success else 'FAILED'}")
    print("=" * 60)
