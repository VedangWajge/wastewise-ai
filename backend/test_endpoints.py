"""
Test the actual endpoints that are failing
"""
import requests
from PIL import Image
import io
import json

# Create a test image
print("Creating test image...")
img = Image.new('RGB', (200, 200), color='blue')
img_bytes = io.BytesIO()
img.save(img_bytes, format='JPEG')
img_bytes.seek(0)

print("\n" + "=" * 60)
print("Testing AI Classification Endpoints")
print("=" * 60)

# Test endpoint 1: /api/ai/predict (what frontend uses)
print("\n1. Testing /api/ai/predict (Frontend endpoint)")
print("-" * 60)
try:
    response = requests.post(
        'http://localhost:5000/api/ai/predict',
        files={'image': ('test.jpg', img_bytes.getvalue(), 'image/jpeg')},
        timeout=30
    )

    print(f"Status Code: {response.status_code}")

    try:
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")
    except:
        print(f"Raw Response: {response.text[:500]}")

except requests.ConnectionError:
    print("[ERROR] Cannot connect to Flask server")
    print("  Make sure Flask is running: python app.py")
except Exception as e:
    print(f"[ERROR] {str(e)}")

# Reset BytesIO for second test
img_bytes = io.BytesIO()
img.save(img_bytes, format='JPEG')
img_bytes.seek(0)

# Test endpoint 2: /api/classify (legacy endpoint)
print("\n2. Testing /api/classify (Legacy endpoint)")
print("-" * 60)
try:
    response = requests.post(
        'http://localhost:5000/api/classify',
        files={'image': ('test.jpg', img_bytes.getvalue(), 'image/jpeg')},
        timeout=30
    )

    print(f"Status Code: {response.status_code}")

    try:
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")
    except:
        print(f"Raw Response: {response.text[:500]}")

except requests.ConnectionError:
    print("[ERROR] Cannot connect to Flask server")
    print("  Make sure Flask is running: python app.py")
except Exception as e:
    print(f"[ERROR] {str(e)}")

print("\n" + "=" * 60)
