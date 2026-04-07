"""
Quick test to verify the AI API endpoint is working
This script ONLY tests the backend API and does NOT affect the website or mobile app.
"""

import requests
from PIL import Image
import io

# Create a test image
img = Image.new('RGB', (200, 200), color='green')
img_bytes = io.BytesIO()
img.save(img_bytes, format='JPEG')
img_bytes.seek(0)

print("Testing AI classification endpoint...")
print("-" * 60)

try:
    # Use the correct backend endpoint
    response = requests.post(
        'http://10.228.33.137:5000/api/ai/predict',
        files={'image': ('test.jpg', img_bytes, 'image/jpeg')},
        timeout=30
    )

    result = response.json()

    print("[SUCCESS] API responded")
    print("Full response from backend:")
    print(result)

    # Try to read common response fields
    prediction = result.get("prediction") or result.get("waste_type")
    confidence = result.get("confidence")

    if prediction:
        print(f"\nPrediction: {prediction}")

    if confidence is not None:
        try:
            print(f"Confidence: {float(confidence):.2%}")
        except:
            print(f"Confidence: {confidence}")

except requests.ConnectionError:
    print("[ERROR] Cannot connect to Flask server")
    print("Make sure Flask backend is running on http://10.228.33.137:5000")

except Exception as e:
    print(f"[ERROR] {str(e)}")

print("-" * 60)
