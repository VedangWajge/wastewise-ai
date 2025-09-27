# WasteWise Backend API Documentation v2.0

## Overview

The WasteWise Backend API is a comprehensive REST API for waste management, classification, and recycling services. It provides endpoints for user management, booking services, payments, rewards, analytics, and administration.

**Base URL:** `http://localhost:5000/api`
**Version:** 2.0.0
**Authentication:** JWT Bearer Token

## Table of Contents

1. [Authentication](#authentication)
2. [User Management](#user-management)
3. [Waste Classification](#waste-classification)
4. [Booking Management](#booking-management)
5. [Service Providers](#service-providers)
6. [Payments](#payments)
7. [Rewards & Gamification](#rewards--gamification)
8. [Analytics](#analytics)
9. [Admin Panel](#admin-panel)
10. [Error Handling](#error-handling)

## Authentication

### Register User
```http
POST /api/auth/register
```

**Request Body:**
```json
{
  "full_name": "John Doe",
  "email": "john@example.com",
  "phone": "+919876543210",
  "password": "SecurePass123!",
  "confirm_password": "SecurePass123!",
  "address": "123 Main St",
  "city": "Mumbai",
  "state": "Maharashtra",
  "pincode": "400001",
  "role": "user",
  "terms_accepted": true
}
```

**Response:**
```json
{
  "success": true,
  "message": "Registration successful",
  "user_id": "uuid-string",
  "next_step": "Please verify your email address"
}
```

### Login User
```http
POST /api/auth/login
```

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "SecurePass123!",
  "remember_me": false
}
```

**Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "user": {
    "id": "uuid-string",
    "email": "john@example.com",
    "full_name": "John Doe",
    "role": "user"
  },
  "tokens": {
    "access_token": "jwt-token-string",
    "refresh_token": "jwt-refresh-token",
    "token_type": "Bearer"
  }
}
```

### Get Profile
```http
GET /api/auth/profile
Authorization: Bearer {access_token}
```

### Update Profile
```http
PUT /api/auth/profile
Authorization: Bearer {access_token}
```

### Change Password
```http
POST /api/auth/change-password
Authorization: Bearer {access_token}
```

### Logout
```http
POST /api/auth/logout
Authorization: Bearer {access_token}
```

## User Management

### Get Current User Info
```http
GET /api/auth/me
Authorization: Bearer {access_token}
```

### Get User Activity
```http
GET /api/auth/activity
Authorization: Bearer {access_token}
```

## Waste Classification

### Classify Waste Image
```http
POST /api/classify
Content-Type: multipart/form-data
```

**Request:**
- `image`: Image file (JPG, PNG, GIF - max 16MB)

**Response:**
```json
{
  "success": true,
  "filename": "uuid_filename.jpg",
  "classification": {
    "waste_type": "plastic",
    "confidence": 0.95,
    "recommendations": [
      "Place in recycling bin",
      "Clean before disposal",
      "Remove any labels if possible"
    ],
    "environmental_impact": "High recyclability - can be processed into new products",
    "all_predictions": {
      "plastic": 0.95,
      "paper": 0.03,
      "glass": 0.01,
      "metal": 0.01,
      "organic": 0.00
    }
  },
  "classification_id": "uuid-string",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### Get Waste Type Information
```http
GET /api/waste-info/{waste_type}
```

## Booking Management

### Create Booking
```http
POST /api/bookings/create
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "service_provider_id": "sp_001",
  "waste_type": "plastic",
  "quantity": "5 kg",
  "pickup_address": "123 Main St, Mumbai",
  "scheduled_date": "2024-01-15T10:00:00Z",
  "scheduled_time_slot": "10:00 AM - 12:00 PM",
  "special_instructions": "Please call before arrival",
  "contact_person": "John Doe",
  "contact_phone": "+919876543210"
}
```

### Get User Bookings
```http
GET /api/bookings/my-bookings
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `status`: Filter by booking status
- `limit`: Number of results (default: 20)
- `offset`: Pagination offset

### Get Booking Details
```http
GET /api/bookings/{booking_id}
Authorization: Bearer {access_token}
```

### Cancel Booking
```http
POST /api/bookings/{booking_id}/cancel
Authorization: Bearer {access_token}
```

### Reschedule Booking
```http
POST /api/bookings/{booking_id}/reschedule
Authorization: Bearer {access_token}
```

### Rate Booking
```http
POST /api/bookings/{booking_id}/rate
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "rating": 5,
  "title": "Excellent service",
  "comment": "Very professional and timely pickup",
  "service_quality": 5,
  "punctuality": 5,
  "cleanliness": 5,
  "communication": 5
}
```

### Track Booking
```http
GET /api/bookings/{booking_id}/track
Authorization: Bearer {access_token}
```

### Create Bulk Booking
```http
POST /api/bookings/bulk
Authorization: Bearer {access_token}
```

## Service Providers

### Search Service Providers
```http
GET /api/services/search
```

**Query Parameters:**
- `waste_type`: Filter by waste type
- `city`: Filter by city
- `service_type`: Filter by service type
- `min_rating`: Minimum rating filter
- `lat`, `lng`: GPS coordinates for location-based search
- `radius`: Search radius in km
- `sort_by`: Sort by rating, distance, or price

### Get Service Provider Details
```http
GET /api/services/{provider_id}
```

### Get Service Provider Reviews
```http
GET /api/services/{provider_id}/reviews
```

### Register as Service Provider
```http
POST /api/services/register
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "business_name": "Green Clean Services",
  "business_type": "Private",
  "specialities": ["plastic", "paper", "glass"],
  "license_number": "WM2024001",
  "address": "456 Business Ave",
  "city": "Mumbai",
  "state": "Maharashtra",
  "pincode": "400001",
  "contact_email": "contact@greenclean.com",
  "contact_phone": "+919876543210",
  "operating_hours": "9:00 AM - 6:00 PM",
  "capacity_per_day": "500 kg",
  "website_url": "https://greenclean.com",
  "description": "Professional waste management services"
}
```

### Get My Provider Profile
```http
GET /api/services/my-profile
Authorization: Bearer {access_token}
```

### Update Provider Profile
```http
PUT /api/services/my-profile
Authorization: Bearer {access_token}
```

### Get Provider Bookings
```http
GET /api/services/my-bookings
Authorization: Bearer {access_token}
```

### Accept Booking
```http
POST /api/services/booking/{booking_id}/accept
Authorization: Bearer {access_token}
```

### Complete Booking
```http
POST /api/services/booking/{booking_id}/complete
Authorization: Bearer {access_token}
```

## Payments

### Initiate Payment
```http
POST /api/payments/initiate
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "booking_id": "book_001",
  "amount": 150.00,
  "payment_method": "card",
  "currency": "INR"
}
```

### Verify Payment
```http
POST /api/payments/verify
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "payment_id": "uuid-string",
  "razorpay_order_id": "order_id",
  "razorpay_payment_id": "payment_id",
  "razorpay_signature": "signature"
}
```

### Get Payment History
```http
GET /api/payments/history
Authorization: Bearer {access_token}
```

### Request Refund
```http
POST /api/payments/{payment_id}/refund
Authorization: Bearer {access_token}
```

### Get Payment Methods
```http
GET /api/payments/methods
```

## Rewards & Gamification

### Get User Points
```http
GET /api/rewards/points
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "success": true,
  "points": {
    "current_balance": 250,
    "weekly_earned": 50,
    "total_earned": 1200,
    "total_spent": 950
  },
  "recent_transactions": [
    {
      "id": "uuid",
      "points": 10,
      "type": "earned",
      "reason": "Waste classification",
      "created_at": "2024-01-01T12:00:00Z"
    }
  ]
}
```

### Get User Badges
```http
GET /api/rewards/badges
Authorization: Bearer {access_token}
```

### Get Leaderboard
```http
GET /api/rewards/leaderboard
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `period`: weekly, monthly, all-time
- `category`: points, classifications, bookings

### Get Reward Catalog
```http
GET /api/rewards/catalog
```

### Redeem Reward
```http
POST /api/rewards/redeem
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "reward_id": "plant_sapling",
  "quantity": 1
}
```

### Get Redemption History
```http
GET /api/rewards/redemptions
Authorization: Bearer {access_token}
```

### Get Challenges
```http
GET /api/rewards/challenges
Authorization: Bearer {access_token}
```

## Analytics

### Get Personal Analytics
```http
GET /api/analytics/personal
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `period`: week, month, quarter, year
- `predictions`: true/false (include AI predictions)

### Get Community Analytics
```http
GET /api/analytics/community/{community_id}
Authorization: Bearer {access_token}
```

### Get Comparison Analytics
```http
GET /api/analytics/comparison
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `type`: user, community
- `id`: ID to compare
- `period`: comparison period

### Export Analytics Data
```http
POST /api/analytics/export
Authorization: Bearer {access_token}
```

**Request Body:**
```json
{
  "type": "personal",
  "format": "json",
  "period": "month",
  "include_charts": false
}
```

### Get AI Insights
```http
GET /api/analytics/insights
Authorization: Bearer {access_token}
```

## Admin Panel

### Get Admin Dashboard
```http
GET /api/admin/dashboard
Authorization: Bearer {admin_access_token}
```

### Manage Users
```http
GET /api/admin/users
Authorization: Bearer {admin_access_token}
```

**Query Parameters:**
- `page`: Page number
- `limit`: Results per page
- `search`: Search query
- `role`: Role filter
- `status`: Status filter

### Update User Status
```http
PUT /api/admin/users/{user_id}/status
Authorization: Bearer {admin_access_token}
```

### Manage Service Providers
```http
GET /api/admin/service-providers
Authorization: Bearer {admin_access_token}
```

### Approve Service Provider
```http
POST /api/admin/service-providers/{provider_id}/approve
Authorization: Bearer {admin_access_token}
```

**Request Body:**
```json
{
  "action": "approve",
  "notes": "All documents verified"
}
```

### Manage Bookings
```http
GET /api/admin/bookings
Authorization: Bearer {admin_access_token}
```

### Generate Reports
```http
GET /api/admin/reports
Authorization: Bearer {admin_access_token}
```

**Query Parameters:**
- `type`: overview, financial, user_activity, environmental
- `period`: week, month, quarter, year

### Get System Settings
```http
GET /api/admin/settings
Authorization: Bearer {admin_access_token}
```

### Update System Settings
```http
PUT /api/admin/settings
Authorization: Bearer {admin_access_token}
```

### Get Admin Actions Log
```http
GET /api/admin/actions
Authorization: Bearer {admin_access_token}
```

## System Endpoints

### Health Check
```http
GET /api/health
```

### Network Test
```http
GET /api/network-test
```

### CORS Test
```http
GET /api/cors-test
OPTIONS /api/cors-test
```

### Global Search
```http
GET /api/search
```

**Query Parameters:**
- `q`: Search query
- `category`: all, services, waste_types, communities
- `limit`: Results limit

### Get Statistics
```http
GET /api/statistics
```

### Get Recent Classifications
```http
GET /api/recent
```

## Error Handling

### Standard Error Response Format
```json
{
  "error": "Error Type",
  "message": "Detailed error message",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### Common HTTP Status Codes
- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `413`: Payload Too Large
- `429`: Rate Limit Exceeded
- `500`: Internal Server Error
- `503`: Service Unavailable

### Authentication Errors
- Invalid credentials
- Token expired
- Token revoked
- Insufficient permissions

### Validation Errors
```json
{
  "error": "Validation failed",
  "messages": {
    "email": ["Invalid email format"],
    "password": ["Password must be at least 8 characters"]
  }
}
```

## Rate Limiting

- **Default**: 100 requests per hour per IP
- **Authenticated**: 1000 requests per hour per user
- **File uploads**: 10 requests per minute per user

## Security Features

- JWT token authentication
- Password encryption with bcrypt
- Input validation and sanitization
- CORS enabled for cross-origin requests
- Rate limiting
- SQL injection prevention
- XSS protection headers

## Environment Variables

```env
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URL=sqlite:///wastewise.db
RAZORPAY_KEY_ID=your-razorpay-key
RAZORPAY_KEY_SECRET=your-razorpay-secret
MAIL_USERNAME=your-email
MAIL_PASSWORD=your-email-password
```

## Getting Started

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**:
   Create a `.env` file with the required variables

3. **Run the Application**:
   ```bash
   python app_complete.py
   ```

4. **Test the API**:
   Visit `http://localhost:5000/api/health` to verify the API is running

## Support

For API support or questions:
- Email: support@wastewise.com
- Documentation: https://docs.wastewise.com
- GitHub: https://github.com/wastewise/backend-api

## Changelog

### Version 2.0.0
- Complete rewrite with modular architecture
- Added JWT authentication
- Implemented comprehensive booking management
- Added payment processing
- Introduced rewards and gamification
- Enhanced analytics and reporting
- Added admin management panel
- Improved error handling and validation
- Added real-time tracking capabilities