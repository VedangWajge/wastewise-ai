"""
Quick test to verify the AI API endpoint is working
"""
import requests
from PIL import Image
import io

# Create a test image
img = Image.new('RGB', (200, 200), color='green')
img_bytes = io.BytesIO()
img.save(img_bytes, format='JPEG')
img_bytes.seek(0)

# Test the API endpoint
print("Testing AI classification endpoint...")
print("-" * 60)

try:
    response = requests.post(
        'http://localhost:5000/api/ai/predict',
        files={'image': ('test.jpg', img_bytes, 'image/jpeg')},
        timeout=30
    )

    result = response.json()

    if result.get('success'):
        print("[SUCCESS] API is working!")
        print(f"  Waste Type: {result.get('waste_type')}")
        print(f"  Confidence: {result.get('confidence'):.2%}")
        print(f"  Provider: {result.get('provider_used')}")
    else:
        print("[ERROR] API returned error:")
        print(f"  {result.get('error')}")
        print(f"  {result.get('message')}")

except requests.ConnectionError:
    print("[ERROR] Cannot connect to Flask server")
    print("  Make sure Flask is running on http://localhost:5000")
except Exception as e:
    print(f"[ERROR] {str(e)}")

print("-" * 60)
