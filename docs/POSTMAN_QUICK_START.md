# Postman Testing - Quick Start Guide

## 📦 What You Have

Two files created for complete API testing:

1. **FINAL_WasteWise_API.postman_collection.json** - Complete API collection with 50+ requests
2. **FINAL_WasteWise.postman_environment.json** - Environment variables for testing

---

## 🚀 Setup (2 Minutes)

### Step 1: Start Backend

```bash
cd backend
python app.py
```

✅ Server running on: `http://localhost:5000`

### Step 2: Import into Postman

1. Open Postman
2. Click **Import** (top left)
3. Drag & drop both files:
   - `FINAL_WasteWise_API.postman_collection.json`
   - `FINAL_WasteWise.postman_environment.json`
4. Select environment: **"FINAL - WasteWise Local Development"** (top right dropdown)

---

## ⚡ Quick Test (30 Seconds)

### Test 1: Check if AI is Working

1. Open collection: **🤖 AI Classification**
2. Click: **Test AI Service Health**
3. Click: **Send**

✅ Expected: `200 OK` with `"success": true`

### Test 2: Classify an Image

1. Click: **⭐ Classify Waste Image**
2. Go to **Body** tab
3. Click **Select File** next to `image`
4. Choose any waste image (JPG/PNG)
5. Click: **Send**

✅ Expected: Classification result with waste type, confidence, and recommendations

---

## 📚 Collection Structure

### 🤖 AI Classification (4 requests)
- **Test AI Service Health** - Check if AI is running
- **Get AI Provider Info** - View available providers
- **⭐ Classify Waste Image** - Main feature - upload & classify
- **Switch AI Provider** - Change between Gemini/Local/HuggingFace/OpenAI

### 🔐 Authentication (6 requests)
- **Register New User** - Create account
- **Login** - Get auth tokens (auto-saves to environment)
- **Get User Profile** - View profile
- **Update Profile** - Edit profile info
- **Change Password** - Update password
- **Logout** - End session

### 📅 Bookings (7 requests)
- **Create Booking** - Schedule waste pickup
- **Get My Bookings** - View all bookings
- **Get Booking Details** - Specific booking info
- **Track Booking** - Real-time tracking
- **Cancel Booking** - Cancel pickup
- **Reschedule Booking** - Change date/time
- **Rate Booking** - Review service

### 💳 Payments (4 requests)
- **Get Payment Methods** - Available options
- **Initiate Payment** - Create Razorpay order
- **Verify Payment** - Confirm payment
- **Get Payment History** - Transaction history

### 🏆 Rewards & Gamification (6 requests)
- **Get User Points** - Current balance
- **Get User Badges** - Earned achievements
- **Get Leaderboard** - Top users
- **Get Reward Catalog** - Available rewards
- **Redeem Reward** - Spend points
- **Get Challenges** - Active challenges

### 🔍 Service Providers (3 requests)
- **Search Service Providers** - Find nearby services
- **Get Provider Details** - Detailed info
- **Get Provider Reviews** - User ratings

### 📊 Analytics (3 requests)
- **Get Dashboard Stats** - Overview
- **Get Personal Analytics** - Waste patterns
- **Get AI Insights** - Recommendations

### 🛒 Marketplace (4 requests)
- **Search Listings** - Browse available waste
- **Create Listing** - Sell your waste
- **Get My Listings** - Your active listings
- **Calculate Price (AI)** - Get pricing suggestion

---

## 🔄 Complete Testing Workflow

### 1. Authentication Flow
```
Register New User → Login (saves tokens) → Get User Profile
```

### 2. AI Classification Flow
```
Test AI Service → Classify Waste Image → View Recommendations
```

### 3. Booking Flow
```
Search Service Providers → Create Booking → Get Booking Details → Track Booking
```

### 4. Payment Flow
```
Initiate Payment → Verify Payment → Get Payment History
```

### 5. Marketplace Flow
```
Calculate Price → Create Listing → Search Listings
```

---

## 🎯 Key Features to Test

### ⭐ AI Classification (MAIN FEATURE)

**Request:** `POST /api/ai/predict`

**Steps:**
1. Open: **🤖 AI Classification** → **⭐ Classify Waste Image**
2. Body → form-data → Select image file
3. Send

**Response Example:**
```json
{
  "success": true,
  "waste_type": "plastic",
  "confidence": 0.95,
  "provider_used": "gemini",
  "recommendations": [
    "Check recycling number on the bottom",
    "Rinse containers before recycling",
    "Remove caps (often different plastic type)"
  ]
}
```

### 🔐 Auto-Login System

The **Login** request automatically saves:
- `{{access_token}}` - Used in all protected endpoints
- `{{refresh_token}}` - For token renewal
- `{{user_id}}` - Current user ID

You don't need to copy/paste tokens!

---

## 🔧 Environment Variables

| Variable | Purpose | Auto-Set |
|----------|---------|----------|
| `base_url` | API endpoint | ✗ |
| `access_token` | Authentication | ✅ After login |
| `refresh_token` | Token refresh | ✅ After login |
| `user_id` | User ID | ✅ After login |
| `booking_id` | Test booking | ✅ After create |
| `payment_id` | Payment ID | ✅ After initiate |
| `razorpay_order_id` | Razorpay order | ✅ After initiate |
| `test_email` | Default email | ✗ |
| `test_password` | Default password | ✗ |

---

## 📝 Test Scripts Included

### Global Tests (Run on every request)
```javascript
✅ Response time < 5000ms
✅ Status code check
✅ Console logging
```

### Specific Tests
- **Login** - Auto-saves tokens
- **Create Booking** - Auto-saves booking_id
- **Initiate Payment** - Auto-saves payment_id
- **AI Classification** - Validates response structure

---

## 🐛 Troubleshooting

### ❌ Connection Error
**Problem:** Cannot connect to server

**Fix:**
```bash
cd backend
python app.py
```
Check: `http://localhost:5000` is accessible

### ❌ 401 Unauthorized
**Problem:** Missing or expired token

**Fix:**
1. Run: **🔐 Authentication** → **Login**
2. Check: `{{access_token}}` is set in environment
3. Verify: Environment is selected (top right)

### ❌ AI Classification Failed
**Problem:** "All AI providers failed" error

**Fix:**
```bash
cd backend
python test_ai_debug.py
```
Check `.env` file for API keys

### ❌ File Upload Failed
**Problem:** Image not uploading

**Fix:**
1. File size < 16MB
2. Format: JPG, PNG, JPEG, GIF
3. Body type: **form-data** (not JSON)

---

## 🎨 Tips & Tricks

### 1. Use Console

Open Postman Console (View → Show Postman Console) to see:
- Auto-save confirmations
- Debug logs
- Error details

### 2. Organize Tests

Use folders to create test suites:
- **Smoke Tests** - Basic health checks
- **Happy Path** - Complete workflows
- **Error Cases** - Invalid inputs

### 3. Collection Runner

Run multiple tests automatically:
1. Click collection name
2. Click **Run**
3. Select requests to run
4. Set iterations
5. Click **Run Collection**

### 4. Share Environment

Export environment to share with team:
1. Click environment (⚙️)
2. Click **...** next to environment
3. Click **Export**

---

## 📊 Testing Checklist

### Basic Tests
- [ ] AI Service Health Check
- [ ] Classify Waste Image (plastic)
- [ ] Classify Waste Image (paper)
- [ ] Classify Waste Image (metal)
- [ ] Register User
- [ ] Login
- [ ] Get Profile

### Workflow Tests
- [ ] Complete booking flow
- [ ] Complete payment flow
- [ ] Redeem rewards
- [ ] Create marketplace listing
- [ ] View analytics

### Error Tests
- [ ] Invalid login
- [ ] Expired token
- [ ] Missing parameters
- [ ] Invalid file type

---

## 🎓 Learning Resources

### Request Examples

**With Auth:**
```http
GET /api/auth/profile
Authorization: Bearer {{access_token}}
```

**File Upload:**
```http
POST /api/ai/predict
Content-Type: multipart/form-data

Body:
  image: <file>
```

**JSON Body:**
```http
POST /api/bookings/create
Authorization: Bearer {{access_token}}
Content-Type: application/json

{
  "service_provider_id": 1,
  "waste_type": "plastic",
  "quantity": 10
}
```

---

## 📞 Need Help?

1. **Backend Logs** - Check Flask terminal for errors
2. **Diagnostic Script** - Run `python test_ai_debug.py`
3. **Documentation** - See `API_TESTING_GUIDE.md`
4. **Error Fix** - See `AI_ERROR_FIX_SUMMARY.md`

---

## 🚀 Next Steps

1. ✅ Import collection & environment
2. ✅ Start backend server
3. ✅ Test AI classification
4. ✅ Create user account
5. ✅ Complete booking flow
6. ✅ Explore marketplace
7. ✅ View analytics

**Ready to test? Let's go! 🎉**

---

## 📝 Notes

- Collection has **50+ pre-configured requests**
- All auth tokens **auto-save**
- Test scripts **included**
- **Works offline** (with local AI provider)
- **Production ready** - just change base_url

Happy Testing! 🧪✨
