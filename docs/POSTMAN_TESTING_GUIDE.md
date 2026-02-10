# Postman API Testing Guide
## WasteWise Complete API Collection

---

## 📦 What's Included

This package includes:
1. **`WasteWise_API_Collection.postman_collection.json`** - Complete API collection with 50+ endpoints
2. **`WasteWise_Environment.postman_environment.json`** - Environment variables for testing
3. **`POSTMAN_TESTING_GUIDE.md`** (this file) - Complete testing guide

---

## 🚀 Quick Start

### Step 1: Import Collection

1. Open **Postman**
2. Click **Import** button (top left)
3. Select **`WasteWise_API_Collection.postman_collection.json`**
4. Click **Import**

### Step 2: Import Environment

1. Click **Import** again
2. Select **`WasteWise_Environment.postman_environment.json`**
3. Click **Import**

### Step 3: Select Environment

1. Click environment dropdown (top right)
2. Select **"WasteWise - Development"**

### Step 4: Start Backend Server

```bash
cd backend
python app.py
```

Server should start on: `http://localhost:5000`

### Step 5: Start Testing!

You're ready to test all APIs! 🎉

---

## 📋 Collection Structure

### 1. Authentication (5 endpoints)
- Register User
- Login User
- Get Current User
- Refresh Token
- Logout

### 2. Waste Classification (2 endpoints)
- Classify Waste Image
- Get Waste Info by Type

### 3. Bookings (7 endpoints)
- Create Booking
- Get My Bookings
- Get Booking Details
- Cancel Booking
- Reschedule Booking
- Rate Booking
- Track Booking

### 4. Payments (5 endpoints)
- Initiate Payment
- Verify Payment
- Get Payment History
- Get Payment Methods
- Request Refund

### 5. Marketplace (14 endpoints) **NEW!**
- Calculate Waste Price
- Create Marketplace Listing
- Search Marketplace Listings
- Get Listing Details
- Get My Listings
- Update Listing
- Delete Listing
- Book Marketplace Listing
- Get My Marketplace Bookings
- Accept Marketplace Booking
- Complete Marketplace Booking
- Process Marketplace Payment
- Get Marketplace Transactions

### 6. Service Providers (4 endpoints)
- Search Service Providers
- Get Provider Details
- Get Provider Reviews
- Register as Service Provider

### 7. Rewards (5 endpoints)
- Get User Points
- Get User Badges
- Get Rewards Catalog
- Redeem Reward
- Get Leaderboard

### 8. Analytics (3 endpoints)
- Get Dashboard Stats
- Get User Statistics
- Get Environmental Impact

---

## 🔑 Authentication Flow

### Method 1: Automatic (Recommended)

The collection includes **test scripts** that automatically save tokens:

1. **Run "Login User"** request
2. Token automatically saved to `{{access_token}}`
3. All authenticated requests now work automatically!

### Method 2: Manual

1. Run "Login User" request
2. Copy `access_token` from response
3. Go to Environment variables
4. Paste into `access_token` variable

### Token Auto-Refresh

The collection bearer token is set to: `{{access_token}}`

This means once you login, ALL requests automatically use your token!

---

## 🧪 Testing Workflows

### Workflow 1: Complete User Journey

```
1. Register User
   └─> Saves: access_token, user_id

2. Login User (if already registered)
   └─> Updates: access_token

3. Classify Waste Image
   └─> Upload waste image

4. Search Service Providers
   └─> Find providers for waste type

5. Create Booking
   └─> Saves: booking_id

6. Initiate Payment
   └─> Pay for booking

7. Verify Payment
   └─> Confirm payment

8. Get My Bookings
   └─> See all bookings

9. Rate Booking
   └─> After completion
```

### Workflow 2: Marketplace Seller Journey

```
1. Login User
   └─> Get authenticated

2. Calculate Waste Price
   └─> Check estimated value

3. Create Marketplace Listing
   └─> Saves: listing_id

4. Get My Listings
   └─> View all your listings

5. Wait for bookings...

6. Accept Marketplace Booking
   └─> Confirm buyer's request

7. Complete Marketplace Booking
   └─> Mark as done

8. Get Marketplace Transactions
   └─> Check earnings
```

### Workflow 3: Marketplace Buyer Journey

```
1. Login User
   └─> Get authenticated

2. Search Marketplace Listings
   └─> Find waste to buy

3. Get Listing Details
   └─> View full info

4. Calculate Waste Price
   └─> Verify pricing

5. Book Marketplace Listing
   └─> Reserve the waste

6. Process Marketplace Payment
   └─> Pay for purchase

7. Get My Marketplace Bookings
   └─> Track your bookings
```

---

## 📝 Environment Variables

Variables automatically set by test scripts:

| Variable | Description | Set By |
|----------|-------------|--------|
| `base_url` | API base URL | Manual (default: localhost:5000) |
| `access_token` | JWT access token | Login/Register |
| `refresh_token` | JWT refresh token | Login/Register |
| `user_id` | Current user ID | Login/Register |
| `booking_id` | Last created booking | Create Booking |
| `listing_id` | Last created listing | Create Listing |
| `payment_id` | Last payment ID | Initiate Payment |
| `provider_id` | Service provider ID | Manual |

---

## 🎯 Testing Each Feature

### Testing Authentication

**1. Register New User:**
```json
POST /auth/register
{
  "email": "newuser@example.com",
  "password": "SecurePass123!",
  "full_name": "New User",
  "phone": "+1234567890",
  "role": "user"
}
```

**Expected Response:** 201 Created
```json
{
  "message": "User registered successfully",
  "user": { ... },
  "tokens": {
    "access_token": "...",
    "refresh_token": "..."
  }
}
```

**2. Login Existing User:**
```json
POST /auth/login
{
  "email": "newuser@example.com",
  "password": "SecurePass123!"
}
```

**Expected Response:** 200 OK with tokens

---

### Testing Marketplace (NEW)

**1. Calculate Price:**
```json
POST /marketplace/calculate-price
{
  "waste_type": "plastic",
  "quantity_kg": 50,
  "waste_subtype": "PET bottles"
}
```

**Expected Response:** 200 OK
```json
{
  "pricing": {
    "waste_type": "plastic",
    "quantity_kg": 50,
    "subtype": "PET bottles",
    "rate_per_kg": 15,
    "total_value": 750,
    "currency": "INR"
  },
  "available_subtypes": [...]
}
```

**2. Create Listing:**
```json
POST /marketplace/listings/create
{
  "title": "Clean PET Bottles - 50kg",
  "waste_type": "plastic",
  "waste_subtype": "PET bottles",
  "quantity_kg": 50,
  "asking_price": 750,
  "location": "123 Green St, Mumbai",
  "city": "Mumbai",
  "condition": "good"
}
```

**Expected Response:** 201 Created with listing_id

**3. Search Listings:**
```
GET /marketplace/listings/search?waste_type=plastic&city=Mumbai&max_price=1000
```

**Expected Response:** 200 OK with array of listings

**4. Book a Listing:**
```json
POST /marketplace/listings/{listing_id}/book
{
  "agreed_price": 750,
  "quantity_kg": 50,
  "pickup_date": "2025-11-20",
  "pickup_time_slot": "09:00-12:00",
  "contact_person": "John Doe",
  "contact_phone": "+919876543210"
}
```

**Expected Response:** 201 Created with booking details

---

### Testing Bookings

**1. Create Booking:**
```json
POST /bookings/create
{
  "service_provider_id": "sp_001",
  "waste_type": "plastic",
  "quantity": "50 kg",
  "pickup_address": "123 Green Street, Mumbai",
  "scheduled_date": "2025-11-15T10:00:00Z",
  "scheduled_time_slot": "10:00 AM - 12:00 PM",
  "contact_person": "John Doe",
  "contact_phone": "+919876543210"
}
```

**Expected Response:** 201 Created with booking_id

**2. Get My Bookings:**
```
GET /bookings/my-bookings?page=1&per_page=20&status=pending
```

**Expected Response:** 200 OK with bookings array

---

### Testing Payments

**1. Initiate Payment:**
```json
POST /payments/initiate
{
  "booking_id": "{{booking_id}}",
  "amount": 420.50,
  "payment_method": "card"
}
```

**Expected Response:** 200 OK with order details

**2. Get Payment History:**
```
GET /payments/history?page=1&per_page=20
```

**Expected Response:** 200 OK with payment history

---

## 🔍 Query Parameter Guide

### Pagination
All list endpoints support pagination:
- `page` - Page number (default: 1)
- `per_page` - Items per page (default: 20)

Example: `?page=2&per_page=10`

### Filtering

**Bookings:**
- `status` - pending, confirmed, in_progress, completed, cancelled

**Marketplace Listings:**
- `waste_type` - plastic, paper, metal, glass, e-waste, organic
- `city` - City name
- `min_quantity` - Minimum quantity in kg
- `max_quantity` - Maximum quantity in kg
- `max_price` - Maximum price
- `condition` - excellent, good, fair

**Sorting:**
- `sort_by` - Field to sort by
- `order` - ASC or DESC

Example: `?sort_by=created_at&order=DESC`

---

## 🎨 Response Status Codes

| Code | Meaning | When You'll See It |
|------|---------|-------------------|
| 200 | OK | Successful GET/PUT request |
| 201 | Created | Successful POST (created resource) |
| 400 | Bad Request | Invalid data sent |
| 401 | Unauthorized | Missing/invalid token |
| 403 | Forbidden | No permission for action |
| 404 | Not Found | Resource doesn't exist |
| 500 | Server Error | Backend error |

---

## 🐛 Troubleshooting

### Issue: "Unauthorized" (401)

**Solution:**
1. Run "Login User" request first
2. Check if `{{access_token}}` variable is set
3. Token expires after some time - login again

### Issue: "Not Found" (404)

**Solution:**
1. Check if resource ID exists
2. Verify the endpoint URL
3. Ensure you used the correct HTTP method

### Issue: "Booking not found"

**Solution:**
1. Run "Create Booking" first
2. Check if `{{booking_id}}` variable is set
3. Make sure you're using your own bookings

### Issue: "Cannot book your own listing"

**Solution:**
This is expected! You need a different user account to book your own marketplace listings.

### Issue: Token expired

**Solution:**
1. Run "Refresh Token" request
2. Or login again with "Login User"

---

## 📊 Test Data Examples

### Sample Users
```json
{
  "email": "seller@example.com",
  "password": "Seller123!",
  "role": "user"
}

{
  "email": "buyer@example.com",
  "password": "Buyer123!",
  "role": "user"
}

{
  "email": "provider@example.com",
  "password": "Provider123!",
  "role": "service_provider"
}
```

### Sample Waste Types
- `plastic` - PET bottles, HDPE, PVC, LDPE, PP, PS
- `paper` - Newspaper, cardboard, office paper
- `metal` - Aluminum, steel, copper, brass
- `glass` - Clear, colored
- `e-waste` - Mobile phones, laptops, batteries
- `organic` - Compost, food waste

### Sample Locations
- Mumbai, Maharashtra 400001
- Delhi, Delhi 110001
- Bangalore, Karnataka 560001
- Chennai, Tamil Nadu 600001
- Pune, Maharashtra 411001

---

## 🧪 Advanced Testing

### Testing with Multiple Users

1. **Create two users:**
   - User A (Seller)
   - User B (Buyer)

2. **As User A:**
   - Login
   - Create marketplace listing
   - Copy `listing_id`

3. **As User B:**
   - Login (tokens will update)
   - Book User A's listing
   - Process payment

4. **As User A again:**
   - Login again
   - Accept the booking
   - Complete the booking

### Testing Filters

**Search with all filters:**
```
GET /marketplace/listings/search?
  waste_type=plastic&
  city=Mumbai&
  min_quantity=10&
  max_quantity=100&
  max_price=1000&
  condition=good&
  sort_by=asking_price&
  order=ASC&
  page=1&
  per_page=20
```

### Testing Pagination

1. Create 25 listings
2. Search with `per_page=10`
3. You should see 3 pages
4. Test: `page=1`, `page=2`, `page=3`

---

## 📈 Performance Testing

### Load Testing Endpoints

Test these endpoints for performance:
- `GET /marketplace/listings/search`
- `GET /bookings/my-bookings`
- `GET /services/search`

### Concurrent Requests

Use Postman's **Collection Runner**:
1. Select collection or folder
2. Set iterations (e.g., 10)
3. Click "Run"
4. Check response times

---

## 🔐 Security Testing

### Test Authentication

1. **Test without token:**
   - Remove `{{access_token}}`
   - Try creating booking
   - Should get 401 Unauthorized

2. **Test with expired token:**
   - Wait for token to expire
   - Should get 401
   - Use refresh token

3. **Test accessing other user's data:**
   - Login as User A
   - Try to cancel User B's booking
   - Should get 403 Forbidden

---

## 💡 Pro Tips

### 1. Use Collection Variables

Variables like `{{booking_id}}` are automatically set by test scripts!

### 2. Use Folders for Organization

The collection is organized in folders:
- Test one folder at a time
- Use "Run Folder" for sequential tests

### 3. Check Test Scripts

Some requests have test scripts that:
- Save response data to variables
- Validate response structure
- Check status codes

### 4. Use Pre-request Scripts

Add authentication checks:
```javascript
if (!pm.collectionVariables.get("access_token")) {
    throw new Error("Please login first!");
}
```

### 5. Export Results

After testing:
1. Click "Runner Results"
2. Export as JSON/HTML
3. Share with team

---

## 📚 Additional Resources

### API Documentation
- Main Docs: `IMPLEMENTATION_SUMMARY.md`
- Payment UI: `PAYMENT_UI_IMPLEMENTATION.md`
- Quick Start: `QUICK_START_GUIDE.md`

### Backend Code
- Routes: `backend/routes/`
- Models: `backend/models/`
- Pricing: `backend/utils/pricing.py`

### Frontend Code
- Components: `frontend/src/components/`
- API Service: `frontend/src/services/api.js`

---

## 🎯 Testing Checklist

Before deploying, test:

### Authentication
- [ ] Register new user
- [ ] Login with correct credentials
- [ ] Login with wrong credentials (should fail)
- [ ] Access protected endpoint without token (should fail)
- [ ] Refresh token
- [ ] Logout

### Bookings
- [ ] Create booking
- [ ] Get all bookings
- [ ] Get booking details
- [ ] Cancel booking
- [ ] Reschedule booking
- [ ] Rate completed booking

### Marketplace
- [ ] Calculate waste price
- [ ] Create listing
- [ ] Search listings with filters
- [ ] Get listing details
- [ ] Update listing
- [ ] Book listing
- [ ] Accept booking (as seller)
- [ ] Complete booking
- [ ] Process payment
- [ ] Get transactions

### Payments
- [ ] Initiate payment
- [ ] Verify payment
- [ ] Get payment history
- [ ] Request refund

### Service Providers
- [ ] Search providers
- [ ] Get provider details
- [ ] Get provider reviews

### Rewards
- [ ] Get user points
- [ ] Get badges
- [ ] Redeem reward
- [ ] Check leaderboard

---

## 🆘 Support

### Common Questions

**Q: How do I test file upload (waste classification)?**
A: Use the "Classify Waste Image" request:
1. Click "Body" tab
2. Select "form-data"
3. Key: `image`, Type: `File`
4. Select an image file
5. Send request

**Q: Can I test without backend running?**
A: No, you need the Flask backend running on `http://localhost:5000`

**Q: How do I test with different users?**
A: Login as different users - tokens will automatically update in variables

**Q: Where are my variables saved?**
A: In the environment. Click the eye icon (👁️) to view all variables.

---

## 📞 Quick Reference

### Base URL
```
http://localhost:5000/api
```

### Auth Header
```
Authorization: Bearer {{access_token}}
```

### Content Type
```
Content-Type: application/json
```

### Common Endpoints
- Login: `POST /auth/login`
- Bookings: `GET /bookings/my-bookings`
- Marketplace: `GET /marketplace/listings/search`
- Payments: `POST /payments/initiate`

---

## ✅ Summary

You now have:
- ✓ Complete API collection with 50+ endpoints
- ✓ Environment with auto-updating variables
- ✓ Test scripts for authentication
- ✓ Organized folder structure
- ✓ Comprehensive testing guide

**Ready to test!** 🚀

Import the collection, start your backend, and begin testing all APIs!

---

**Collection Version:** 2.0.0
**Last Updated:** 2025-10-29
**Total Endpoints:** 50+
**New Endpoints:** 14 (Marketplace)
