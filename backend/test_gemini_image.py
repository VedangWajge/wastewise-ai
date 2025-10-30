"""
Test Gemini with actual image classification
"""
import os
import sys
from PIL import Image
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, os.path.dirname(__file__))

from config.ai_config import AIConfig

# Create a test image
print("Creating test image...")
test_img = Image.new('RGB', (200, 200), color='green')
test_path = 'test_gemini_img.jpg'
test_img.save(test_path)
print(f"Test image saved: {test_path}")

print("\n" + "=" * 60)
print("Testing Gemini Vision API with Image")
print("=" * 60)

try:
    import google.generativeai as genai
    print("[OK] google.generativeai imported")

    api_key = AIConfig.GEMINI_API_KEY
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment")
    print(f"[OK] API key found: {api_key[:10]}...")

    genai.configure(api_key=api_key)
    print("[OK] Gemini configured")

    model_name = AIConfig.GEMINI_MODEL
    print(f"[INFO] Using model: {model_name}")

    model = genai.GenerativeModel(model_name)
    print("[OK] Model loaded")

    # Load the test image
    img = Image.open(test_path)
    print(f"[OK] Image loaded: {img.size}, {img.mode}")

    # Create the prompt
    prompt = f"""Analyze this image and classify the waste type.

Available categories: {', '.join(AIConfig.WASTE_CATEGORIES)}

Respond in this EXACT JSON format:
{{
    "waste_type": "most likely category from the list",
    "confidence": 0.95,
    "reasoning": "brief explanation"
}}"""

    print("\n[INFO] Sending request to Gemini...")
    print(f"[INFO] Prompt length: {len(prompt)} chars")

    # Generate content
    response = model.generate_content([prompt, img])
    print("[OK] Response received")

    print("\n" + "-" * 60)
    print("Response:")
    print("-" * 60)
    print(response.text)
    print("-" * 60)

    # Try to parse JSON
    import json
    import re

    json_match = re.search(r'\{[^}]+\}', response.text, re.DOTALL)
    if json_match:
        result = json.loads(json_match.group())
        print("\n[OK] Parsed JSON result:")
        print(f"  Waste Type: {result.get('waste_type')}")
        print(f"  Confidence: {result.get('confidence')}")
        print(f"  Reasoning: {result.get('reasoning')}")
    else:
        print("\n[WARNING] Could not find JSON in response")

    # Cleanup
    if os.path.exists(test_path):
        os.remove(test_path)
        print("\n[OK] Test image cleaned up")

    print("\n" + "=" * 60)
    print("TEST PASSED")
    print("=" * 60)

except ImportError as e:
    print(f"\n[ERROR] Import failed: {e}")
    print("  Run: pip install google-generativeai")

except Exception as e:
    print(f"\n[ERROR] {type(e).__name__}: {str(e)}")
    import traceback
    print("\nFull traceback:")
    traceback.print_exc()

    # Cleanup
    if os.path.exists(test_path):
        os.remove(test_path)

    print("\n" + "=" * 60)
    print("TEST FAILED")
    print("=" * 60)
