# WasteWise API Testing Guide

Complete guide for testing WasteWise APIs using Postman and Python scripts.

## Quick Start

### 1. Import Postman Collection

1. Open Postman
2. Click **Import** button
3. Select `WasteWise_Complete_API_Collection.postman_collection.json`
4. Select `WasteWise_Environment.postman_environment.json`
5. Set environment to "WasteWise - Development"

### 2. Start Flask Backend

```bash
cd backend
python app.py
```

Server should start on: `http://localhost:5000`

---

## Testing AI Classification Endpoints

### Test 1: AI Service Health Check

**Request:**
```
GET http://localhost:5000/api/ai/test
```

**Expected Response:**
```json
{
  "success": true,
  "message": "AI service is running",
  "active_provider": "gemini",
  "provider_status": {
    "active_provider": "gemini",
    "fallback_provider": "local",
    "providers_status": {
      "local": true,
      "huggingface": true,
      "gemini": true,
      "openai": true
    }
  }
}
```

### Test 2: Get AI Providers Info

**Request:**
```
GET http://localhost:5000/api/ai/providers
```

**Expected Response:**
```json
{
  "success": true,
  "provider_info": {
    "active_provider": "gemini",
    "fallback_provider": "local",
    "providers_status": {
      "local": true,
      "huggingface": true,
      "gemini": true,
      "openai": true
    }
  }
}
```

### Test 3: Classify Waste Image ⭐ MAIN FEATURE

**Request:**
```
POST http://localhost:5000/api/ai/predict
Content-Type: multipart/form-data

Body:
  - image: <select an image file>
```

**Postman Steps:**
1. Open the "Classify Waste Image" request
2. Go to **Body** tab
3. Select **form-data**
4. Set key as `image` and change type to `File`
5. Click "Select Files" and choose a test image
6. Click **Send**

**Expected Response:**
```json
{
  "success": true,
  "waste_type": "plastic",
  "raw_category": "plastic",
  "confidence": 0.95,
  "provider_used": "gemini",
  "fallback_used": false,
  "recommendations": [
    "Check recycling number on the bottom",
    "Rinse containers before recycling",
    "Remove caps (often different plastic type)",
    "Avoid single-use plastics when possible"
  ],
  "all_predictions": [
    {
      "class": "plastic",
      "mapped_type": "plastic",
      "confidence": 0.95
    }
  ],
  "timestamp": "2025-10-30T12:00:00.000000"
}
```

### Test 4: Switch AI Provider

**Request:**
```
POST http://localhost:5000/api/ai/switch-provider
Content-Type: application/json

{
  "provider": "local"
}
```

**Available Providers:**
- `gemini` - Google Gemini Vision AI (default)
- `local` - Local TensorFlow model
- `huggingface` - Hugging Face API
- `openai` - OpenAI GPT-4 Vision

**Expected Response:**
```json
{
  "success": true,
  "message": "Switched to local provider",
  "active_provider": "local"
}
```

---

## Testing with Python Scripts

### Quick AI Test Script

```bash
cd backend
python test_ai_debug.py
```

**What it tests:**
- Provider configuration status
- Classifier initialization
- Image classification
- Full error handling

### Endpoint Test Script

```bash
cd backend
python test_endpoints.py
```

**What it tests:**
- `/api/ai/predict` endpoint
- File upload handling
- Response format

---

## Testing Authentication Flow

### 1. Register a New User

**Request:**
```
POST http://localhost:5000/api/auth/register
Content-Type: application/json

{
  "name": "Test User",
  "email": "test@example.com",
  "password": "TestPassword123!",
  "phone": "+1234567890",
  "address": "123 Test St",
  "user_type": "resident"
}
```

### 2. Login

**Request:**
```
POST http://localhost:5000/api/auth/login
Content-Type: application/json

{
  "email": "test@example.com",
  "password": "TestPassword123!",
  "remember_me": false
}
```

**Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "user": {
    "id": 1,
    "name": "Test User",
    "email": "test@example.com",
    "user_type": "resident"
  },
  "tokens": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

**Note:** The access token is automatically saved to Postman environment variable `{{access_token}}`

### 3. Test Protected Endpoint

**Request:**
```
GET http://localhost:5000/api/auth/profile
Authorization: Bearer {{access_token}}
```

---

## Testing Booking Flow

### 1. Search for Service Providers

**Request:**
```
GET http://localhost:5000/api/services/search?waste_type=plastic&latitude=28.7041&longitude=77.1025&radius=10
```

### 2. Create a Booking

**Request:**
```
POST http://localhost:5000/api/bookings/create
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "service_provider_id": 1,
  "waste_type": "plastic",
  "quantity": 5,
  "unit": "kg",
  "scheduled_date": "2025-11-15",
  "time_slot": "morning",
  "pickup_address": "123 Main St, City",
  "notes": "Please ring doorbell"
}
```

### 3. Get Booking Details

**Request:**
```
GET http://localhost:5000/api/bookings/{{booking_id}}
Authorization: Bearer {{access_token}}
```

---

## Testing Payment Flow

### 1. Initiate Payment

**Request:**
```
POST http://localhost:5000/api/payments/initiate
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "booking_id": 1,
  "amount": 150.00,
  "payment_method": "razorpay",
  "currency": "INR"
}
```

**Response:**
```json
{
  "success": true,
  "payment_id": 1,
  "razorpay_order_id": "order_abc123",
  "amount": 150.00,
  "currency": "INR",
  "key_id": "rzp_test_xxx"
}
```

### 2. Verify Payment

**Request:**
```
POST http://localhost:5000/api/payments/verify
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "razorpay_order_id": "order_abc123",
  "razorpay_payment_id": "pay_xyz789",
  "razorpay_signature": "signature_here"
}
```

---

## Testing Rewards System

### 1. Get User Points

**Request:**
```
GET http://localhost:5000/api/rewards/points
Authorization: Bearer {{access_token}}
```

### 2. Get Leaderboard

**Request:**
```
GET http://localhost:5000/api/rewards/leaderboard?period=month&limit=10
```

### 3. Redeem Reward

**Request:**
```
POST http://localhost:5000/api/rewards/redeem
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "reward_id": 1,
  "points_to_redeem": 100
}
```

---

## Testing Marketplace

### 1. Create Listing

**Request:**
```
POST http://localhost:5000/api/marketplace/listings/create
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "waste_type": "plastic",
  "quantity": 10,
  "unit": "kg",
  "price_per_unit": 5.0,
  "description": "Clean plastic bottles",
  "pickup_location": "123 Main St",
  "available_from": "2025-11-01",
  "available_until": "2025-11-30"
}
```

### 2. Search Listings

**Request:**
```
GET http://localhost:5000/api/marketplace/listings/search?waste_type=plastic&max_price=10
```

### 3. Calculate Price

**Request:**
```
POST http://localhost:5000/api/marketplace/calculate-price
Content-Type: application/json

{
  "waste_type": "plastic",
  "quantity": 10,
  "unit": "kg",
  "quality": "high"
}
```

---

## Common Error Responses

### 400 Bad Request
```json
{
  "error": "No image file provided"
}
```

### 401 Unauthorized
```json
{
  "msg": "Missing Authorization Header"
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "error": "Classification failed",
  "message": "Classification failed. Please check AI provider configuration.",
  "provider_status": {
    "active_provider": "gemini",
    "fallback_provider": "local",
    "providers_status": {
      "gemini": true,
      "local": true
    }
  }
}
```

---

## Environment Variables

Set these in your Postman environment:

| Variable | Description | Example |
|----------|-------------|---------|
| `base_url` | Base API URL | `http://localhost:5000` |
| `access_token` | JWT access token | Auto-set after login |
| `refresh_token` | JWT refresh token | Auto-set after login |
| `user_id` | Current user ID | Auto-set after login |
| `booking_id` | Test booking ID | `1` |
| `payment_id` | Test payment ID | `1` |

---

## Testing Tips

### 1. Auto-Save Tokens

The Login request has a test script that automatically saves tokens:
```javascript
var jsonData = pm.response.json();
if (jsonData.tokens && jsonData.tokens.access_token) {
    pm.environment.set("access_token", jsonData.tokens.access_token);
    pm.environment.set("refresh_token", jsonData.tokens.refresh_token);
}
```

### 2. Test Image Sources

For testing AI classification, use images from:
- **Test Images Folder**: Create a `test_images/` folder with sample waste images
- **Online Sources**: Download sample images from waste datasets
- **Screenshot**: Use your phone camera to take waste pictures

### 3. Monitor Flask Logs

Watch the Flask terminal for debug output:
```
[AI-ROUTES] Image saved to: uploads/temp_abc123.jpg
[AI-ROUTES] Classifier initialized with provider: gemini
[AI-ROUTES] Classification successful: plastic (95.00%)
```

### 4. Database Reset

If you need to reset the database:
```bash
cd backend
rm wastewise.db
python app.py  # Database will be recreated
```

---

## Troubleshooting

### Issue: "All AI providers failed"

**Solution:**
1. Check `.env` file has correct API keys
2. Verify `google-generativeai` is installed: `pip install google-generativeai`
3. Run diagnostic: `python test_ai_debug.py`
4. Check internet connection (for cloud providers)

### Issue: "Connection refused"

**Solution:**
1. Make sure Flask is running: `python app.py`
2. Check port 5000 is not in use
3. Verify `base_url` in Postman environment

### Issue: "401 Unauthorized"

**Solution:**
1. Login first to get access token
2. Check `{{access_token}}` is set in environment
3. Token may have expired - login again

### Issue: "File upload failed"

**Solution:**
1. Check file size < 16MB
2. Use supported formats: JPG, PNG, JPEG, GIF
3. Ensure `Content-Type: multipart/form-data` header

---

## Next Steps

1. ✅ Import Postman collection
2. ✅ Start Flask backend
3. ✅ Test AI classification endpoint
4. ✅ Create user account and login
5. ✅ Test booking flow
6. ✅ Test payment integration
7. ✅ Explore marketplace features

---

## Support

If you encounter issues:
1. Check Flask terminal logs
2. Run diagnostic tests: `python test_ai_debug.py`
3. Verify environment configuration
4. Review `AI_ERROR_FIX_SUMMARY.md` for known issues

Happy Testing! 🚀
