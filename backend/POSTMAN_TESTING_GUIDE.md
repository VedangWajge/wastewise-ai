# 🚀 WasteWise API Postman Testing Guide

## 📁 Files to Import

You have 2 files to drag and drop into Postman:

1. **`WasteWise_API_Collection.postman_collection.json`** - Complete API collection
2. **`WasteWise_Environment.postman_environment.json`** - Environment variables

## 🔧 Setup Instructions

### Step 1: Import Files
1. Open Postman
2. Drag and drop both JSON files into Postman
3. Select the "WasteWise API Environment" from the environment dropdown (top right)

### Step 2: Start the Backend Server
```bash
cd /path/to/wastewise/backend
python app_complete.py
```

### Step 3: Verify Server is Running
1. In Postman, go to "🏥 System Health" folder
2. Run "Health Check" request
3. You should get a successful response with API info

## 🧪 Testing Workflow

### 🔐 Authentication Flow
1. **Register User** - Create a new account
2. **Login User** - Get access tokens (automatically saved to environment)
3. **Get Profile** - Verify authentication works

### 🗂️ Waste Classification
1. **Classify Waste Image** - Upload an image file for classification
2. **Get Waste Type Info** - Learn about specific waste types
3. **Get Recent Classifications** - View recent classification results

### 📋 Booking Management
1. **Create Booking** - Book a waste pickup service
2. **Get My Bookings** - View your bookings
3. **Track Booking** - Get real-time tracking info
4. **Rate Booking** - Submit a review
5. **Cancel/Reschedule** - Modify existing bookings

### 🏢 Service Providers
1. **Search Service Providers** - Find services near you
2. **Get Provider Details** - View provider information
3. **Register as Service Provider** - Apply to become a provider

### 💳 Payments
1. **Get Payment Methods** - View available payment options
2. **Initiate Payment** - Start payment process
3. **Verify Payment** - Confirm payment completion
4. **Get Payment History** - View transaction history

### 🎯 Rewards & Gamification
1. **Get User Points** - Check your point balance
2. **Get User Badges** - View earned badges
3. **Get Leaderboard** - See your ranking
4. **Redeem Reward** - Use points for rewards

### 📊 Analytics
1. **Get Personal Analytics** - View your environmental impact
2. **Get Community Analytics** - Community-level statistics
3. **Export Analytics Data** - Download reports

### 🛠️ Admin Panel (Requires Admin Token)
1. **Get Admin Dashboard** - System overview
2. **Manage Users** - User administration
3. **Approve Service Providers** - Provider verification
4. **Generate Reports** - System reports

## 🔑 Environment Variables

The following variables are automatically set during testing:

| Variable | Description | Set By |
|----------|-------------|---------|
| `access_token` | JWT authentication token | Login request |
| `user_id` | Current user ID | Login/Register |
| `booking_id` | Created booking ID | Create Booking |
| `payment_id` | Payment transaction ID | Initiate Payment |
| `classification_id` | Waste classification ID | Classify Waste |

## 📝 Sample Test Data

### User Registration
```json
{
  "full_name": "John Doe",
  "email": "john.doe@example.com",
  "phone": "+919876543210",
  "password": "SecurePass123!",
  "confirm_password": "SecurePass123!",
  "address": "123 Main Street",
  "city": "Mumbai",
  "state": "Maharashtra",
  "pincode": "400001",
  "role": "user",
  "terms_accepted": true
}
```

### Booking Creation
```json
{
  "service_provider_id": "sp_001",
  "waste_type": "plastic",
  "quantity": "5 kg",
  "pickup_address": "123 Main Street, Mumbai, 400001",
  "scheduled_date": "2024-02-15T10:00:00Z",
  "scheduled_time_slot": "10:00 AM - 12:00 PM",
  "special_instructions": "Please call before arrival",
  "contact_person": "John Doe",
  "contact_phone": "+919876543210"
}
```

## 🔍 Pre-configured Searches

The collection includes pre-configured requests for:

- **Service Provider Search**: Filters by waste type, location, rating
- **Global Search**: Search across services, waste types, communities
- **Analytics Queries**: Different time periods and data types
- **Admin Queries**: User management, provider approval, system reports

## 📋 Testing Checklist

### ✅ Basic Functionality
- [ ] Health check passes
- [ ] User registration works
- [ ] User login gets tokens
- [ ] Profile retrieval works
- [ ] Image classification works
- [ ] Booking creation succeeds

### ✅ Authentication
- [ ] Protected routes require tokens
- [ ] Invalid tokens are rejected
- [ ] Token refresh works
- [ ] Logout invalidates tokens

### ✅ Data Persistence
- [ ] Created bookings appear in user's list
- [ ] Points are awarded for actions
- [ ] Payment records are saved
- [ ] Classification history is maintained

### ✅ Error Handling
- [ ] Invalid data returns proper errors
- [ ] Missing fields are validated
- [ ] File upload size limits work
- [ ] Rate limiting functions

### ✅ Advanced Features
- [ ] Real-time booking tracking
- [ ] Payment flow completion
- [ ] Reward redemption
- [ ] Analytics data generation
- [ ] Admin functions (with admin token)

## 🐛 Troubleshooting

### Common Issues

1. **Server Connection Failed**
   - Check if backend server is running on port 5000
   - Verify base_url in environment is correct

2. **Authentication Errors**
   - Login first to get access tokens
   - Check if token is properly set in environment

3. **File Upload Issues**
   - Ensure image file is selected in form-data
   - Check file size is under 16MB

4. **Admin Endpoints Fail**
   - Create an admin user manually in database
   - Get admin token and set as `admin_token` variable

### Debug Tips

1. **Check Response Headers**
   - Look for `X-API-Version` header
   - Verify CORS headers are present

2. **Monitor Environment Variables**
   - Ensure tokens are being set automatically
   - Check if IDs are being captured from responses

3. **Use Console Logs**
   - Postman console shows request/response details
   - Check for any JavaScript errors in test scripts

## 📞 Support

If you encounter issues:

1. Check the API documentation in `API_DOCUMENTATION.md`
2. Verify environment variables are set correctly
3. Look at the response body for specific error messages
4. Check server logs for backend errors

## 🎯 Next Steps

After successful testing:

1. **Mobile Integration**: Use these endpoints in your mobile app
2. **Frontend Development**: Build a web dashboard
3. **Production Deployment**: Deploy to cloud services
4. **Real AI Model**: Replace mock classifier with actual ML model
5. **Payment Gateway**: Integrate real Razorpay credentials

## 📊 Collection Statistics

- **Total Requests**: 60+ endpoints
- **Test Categories**: 8 major features
- **Authentication**: JWT Bearer token
- **File Uploads**: Multipart form data
- **Auto Variables**: 12 environment variables
- **Error Handling**: Comprehensive validation

Happy Testing! 🎉