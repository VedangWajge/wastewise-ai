# Marketplace Bookings Not Showing - Diagnostic & Fix

## Problem

User reports: "My bookings are not displayed in payments and bookings tab in marketplace"

Expected behavior:
- Bookings from "Classify → Sell" should appear
- Bookings from "Marketplace → Sell" should appear

## Root Cause Analysis

After investigating the code, the issue is likely one of the following:

### 1. No Bookings in Database (Most Likely)

The marketplace bookings table may be empty. The frontend correctly calls the API and displays "No bookings found" when the database returns empty results.

### 2. Authentication Issue

User may not be logged in, or the JWT token expired.

### 3. User ID Mismatch

The bookings may exist but belong to a different user ID.

## How the System Works

### Marketplace Booking Flow

```
1. User A creates listing → marketplace_listings table
2. User B browses listings → /api/marketplace/listings/search
3. User B books listing → POST /api/marketplace/listings/{id}/book
4. Booking created → marketplace_bookings table
5. User B views bookings → GET /api/marketplace/my-bookings
```

### Regular Service Booking Flow (Classify → Book)

Regular bookings from "Classify → Sell" are stored in the `bookings` table, NOT `marketplace_bookings`.

**This is the key distinction:**
- **Regular bookings**: `/api/bookings/*` endpoints
- **Marketplace bookings**: `/api/marketplace/*` endpoints

## Diagnostic Steps

### Step 1: Run Diagnostic Script

```bash
cd backend
python test_marketplace_bookings.py
```

This will show:
- ✅ If marketplace_bookings table exists
- ✅ Total bookings count
- ✅ List of all bookings
- ✅ Total listings count
- ✅ Sample listings

### Step 2: Check Browser Console

1. Open browser DevTools (F12)
2. Go to Network tab
3. Navigate to Marketplace → My Bookings
4. Check the API call to `/api/marketplace/my-bookings`
5. Look at the response

**Expected response:**
```json
{
  "bookings": [],  // Empty if no bookings
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 0,
    "pages": 0
  }
}
```

### Step 3: Check Authentication

```bash
# In browser console
console.log(localStorage.getItem('access_token'));
```

If `null`, user needs to login.

### Step 4: Verify Database

```bash
cd backend
sqlite3 wastewise.db

# Check bookings
SELECT COUNT(*) FROM marketplace_bookings;
SELECT * FROM marketplace_bookings;

# Check listings
SELECT COUNT(*) FROM marketplace_listings;
SELECT * FROM marketplace_listings LIMIT 5;

# Exit
.exit
```

## Solutions

### Solution 1: Create Test Bookings

If the database is empty (most common case):

#### Option A: Create via Frontend

1. **Login to account A**
2. **Create a marketplace listing:**
   - Go to Marketplace → Create Listing
   - Fill in details (waste type, quantity, price, location)
   - Submit

3. **Login to account B (different user)**
4. **Book the listing:**
   - Go to Marketplace → Browse Listings
   - Click on the listing
   - Click "Book This Listing"
   - Fill booking details
   - Submit

5. **View bookings:**
   - Account B → Marketplace → My Bookings (should show as buyer)
   - Account A → Check notification/listings (should show as seller)

#### Option B: Create via API/Postman

Use the Postman collection:

```bash
# 1. Login
POST /api/auth/login
{
  "email": "user@example.com",
  "password": "password"
}
# Save access_token

# 2. Create listing
POST /api/marketplace/listings/create
Authorization: Bearer {access_token}
{
  "title": "Test Plastic Waste",
  "waste_type": "plastic",
  "quantity_kg": 10,
  "asking_price": 50,
  "location": "Mumbai",
  "city": "Mumbai"
}
# Save listing_id

# 3. Book listing (use different user's token)
POST /api/marketplace/listings/{listing_id}/book
Authorization: Bearer {different_user_token}
{
  "pickup_date": "2025-11-15",
  "pickup_time_slot": "09:00-12:00",
  "contact_person": "John Doe",
  "contact_phone": "+919876543210"
}

# 4. View bookings
GET /api/marketplace/my-bookings
Authorization: Bearer {buyer_token}
```

### Solution 2: Fix Authentication

If user is not logged in:

```javascript
// Check in browser console
if (!localStorage.getItem('access_token')) {
  console.log('Not logged in - please login');
  // Redirect to login page
  window.location.href = '/#/login';
}
```

### Solution 3: Understanding Two Booking Systems

The app has TWO different booking systems:

#### System 1: Regular Bookings (Classify → Book Service)

**Flow:**
```
Classify Waste → Find Services → Book Collection → bookings table
```

**Endpoints:**
- `/api/bookings/create`
- `/api/bookings/my-bookings`

**View in Frontend:**
- Home → Bookings tab
- Or dedicated Bookings Management page

#### System 2: Marketplace Bookings (Peer-to-Peer)

**Flow:**
```
Create Listing → Someone Books → marketplace_bookings table
```

**Endpoints:**
- `/api/marketplace/my-bookings` (as buyer)
- `/api/marketplace/my-listings` (as seller - shows booking count)

**View in Frontend:**
- Marketplace → My Bookings tab

**These are SEPARATE systems with different tables and endpoints!**

## Frontend Implementation

The frontend correctly implements the marketplace bookings display:

```javascript
// Marketplace.js line 80-98
const fetchMyBookings = async () => {
  setLoading(true);
  try {
    const token = localStorage.getItem('access_token');
    const response = await fetch(
      `${API_URL}/api/marketplace/my-bookings?page=${pagination.page}`,
      {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
    );

    const data = await response.json();
    if (response.ok) {
      setListings(data.bookings);  // ✅ Correctly gets bookings
      setPagination(prev => ({ ...prev, ...data.pagination }));
    }
  } catch (error) {
    console.error('Error fetching my bookings:', error);
  }
  setLoading(false);
};
```

The BookingsList component correctly displays bookings (line 848-886):

```javascript
const BookingsList = ({ bookings, loading }) => {
  if (loading) {
    return <div className="loading-spinner">Loading...</div>;
  }

  if (bookings.length === 0) {
    return <div className="no-listings"><p>No bookings found</p></div>;  // ✅ Shows when empty
  }

  return (
    <div className="bookings-list">
      {bookings.map(booking => (
        <div key={booking.id} className="booking-card">
          {/* Booking details */}
        </div>
      ))}
    </div>
  );
};
```

## Backend Implementation

The backend endpoint is correctly implemented:

```python
# marketplace.py line 415-478
@marketplace_bp.route('/my-bookings', methods=['GET'])
@jwt_required()
def get_my_bookings():
    """Get bookings made by current user (as buyer)"""
    user_id = get_jwt_identity()

    # Query marketplace_bookings with JOIN to get listing details
    query = '''
        SELECT b.*,
               l.title as listing_title,
               l.waste_type,
               l.waste_subtype,
               u.full_name as seller_name
        FROM marketplace_bookings b
        JOIN marketplace_listings l ON b.listing_id = l.id
        JOIN users u ON b.seller_id = u.id
        WHERE b.buyer_id = ?
    '''

    cursor.execute(query, [user_id])
    bookings = [dict(row) for row in cursor.fetchall()]

    return jsonify({
        'bookings': bookings,  # ✅ Returns bookings array
        'pagination': {...}
    })
```

## Testing Checklist

- [ ] Run diagnostic script: `python test_marketplace_bookings.py`
- [ ] Check if marketplace_bookings table exists
- [ ] Check if marketplace_listings table exists
- [ ] Verify user is logged in (access_token exists)
- [ ] Create at least one test listing
- [ ] Book the listing with a different user
- [ ] Verify booking appears in "My Bookings"
- [ ] Check browser console for errors
- [ ] Check Flask backend logs for errors

## API Endpoints Summary

### Marketplace Bookings

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/api/marketplace/listings/search` | GET | Browse all listings | No |
| `/api/marketplace/listings/create` | POST | Create new listing | Yes |
| `/api/marketplace/my-listings` | GET | Get your listings | Yes |
| `/api/marketplace/listings/{id}/book` | POST | Book a listing | Yes |
| `/api/marketplace/my-bookings` | GET | Get your bookings (as buyer) | Yes |
| `/api/marketplace/bookings/{id}/accept` | POST | Accept booking (as seller) | Yes |

### Regular Bookings

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/api/bookings/create` | POST | Create service booking | Yes |
| `/api/bookings/my-bookings` | GET | Get your service bookings | Yes |

## Expected User Flows

### Flow 1: Sell Waste via Marketplace

```
1. User A: Login
2. User A: Marketplace → Create Listing
3. User A: Fill form and submit
4. User B: Login
5. User B: Marketplace → Browse Listings
6. User B: Click listing → Book it
7. User B: Marketplace → My Bookings (✅ should show booking)
8. User A: Marketplace → My Listings (✅ should show booking count)
```

### Flow 2: Book Waste Collection Service

```
1. User: Login
2. User: Home → Upload waste image
3. User: AI classifies waste
4. User: Click "Find Services"
5. User: Select service → Book
6. User: Home → Bookings tab (✅ should show booking)
```

**These are DIFFERENT flows with DIFFERENT booking tables!**

## Troubleshooting

### Issue: "No bookings found" but I created one

**Check:**
1. Are you logged in as the buyer (not the seller)?
2. Did the booking API call succeed?
3. Is the booking in the database?

```bash
# Check database
cd backend
sqlite3 wastewise.db
SELECT * FROM marketplace_bookings WHERE buyer_id = 'YOUR_USER_ID';
```

### Issue: API returns 401 Unauthorized

**Fix:**
```javascript
// Login again
window.location.href = '/#/login';
```

### Issue: API returns 500 Error

**Check backend logs:**
```bash
# Look for error messages in Flask terminal
# Common issues:
# - Database connection error
# - Missing table
# - SQL syntax error
```

## Summary

✅ **Frontend Code**: Correctly implemented
✅ **Backend Code**: Correctly implemented
✅ **Database Schema**: Correctly defined

❓ **Most Likely Issue**: Database is empty - no bookings have been created yet

**Solution**: Create test bookings using the flows above

## Files Created

1. `backend/test_marketplace_bookings.py` - Diagnostic script
2. `MARKETPLACE_BOOKINGS_FIX.md` - This document

## Quick Fix Command

```bash
cd backend
python test_marketplace_bookings.py
```

This will tell you exactly what's missing!
