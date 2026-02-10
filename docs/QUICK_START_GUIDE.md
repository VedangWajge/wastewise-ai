# WasteWise - Quick Start Guide
## New Features: Marketplace & Dynamic Pricing

---

## 🚀 Getting Started

### 1. Start the Backend Server

```bash
cd backend
python app.py
```

The server will:
- Initialize the database with new marketplace tables
- Start on `http://localhost:5000`
- Create all necessary tables automatically

### 2. Start the Frontend

```bash
cd frontend
npm install  # If first time
npm start
```

The React app will:
- Start on `http://localhost:3000`
- Open automatically in your browser

---

## 📱 Using the New Features

### Feature 1: Dynamic Price Estimation in Booking

**Steps:**
1. Navigate to Home and classify waste using camera
2. Click "Find Collection Services"
3. Select a service provider
4. In the booking form:
   - Enter quantity (e.g., 50 kg)
   - Select waste subtype if available
   - **See real-time price calculation**:
     - Your waste value (what you earn)
     - Collection charges
     - Net amount (+ earn or - pay)

**Example Output:**
```
Waste Value: + ₹750 (₹15/kg × 50kg)
Collection Cost: ₹330
Net Amount: + ₹420 (You earn!)
```

---

### Feature 2: Marketplace - List Your Waste

**Steps:**
1. Click "Marketplace" in the navigation bar (🛒 icon)
2. Click "+ Create Listing" button
3. Fill in the form:
   - **Title**: e.g., "Clean PET Bottles - 50kg"
   - **Description**: Additional details
   - **Waste Type**: Select from dropdown
   - **Subtype**: Automatically populated with rates
   - **Quantity**: Enter in kg
   - **Condition**: Excellent/Good/Fair
   - **Location**: Full address
   - **City, State, Pincode**: For search filters
4. See estimated value calculated automatically
5. Adjust asking price if needed
6. Submit listing

**Result:**
- Your listing appears in the marketplace
- Other users can search and find it
- You'll receive bookings from interested buyers

---

### Feature 3: Marketplace - Buy Waste

**Steps:**
1. Go to "Marketplace" → "Browse Listings"
2. Use filters to find waste:
   - Waste Type (plastic, paper, metal, etc.)
   - City
   - Max Price
   - Condition
3. Click on a listing to view details:
   - Full waste information
   - Seller details and ratings
   - Location and availability
4. Click "Book This Listing"
5. Fill in booking details:
   - Pickup date and time slot
   - Contact person and phone
   - Special instructions
6. Confirm booking
7. Complete payment

**Result:**
- Booking created with status "pending"
- Seller receives notification (future feature)
- Payment processed with 5% platform fee
- You can track booking in "My Bookings"

---

## 🎯 Key Features to Try

### 1. Price Calculator
**URL**: Available in booking form
**Try**: Enter different quantities and see prices update in real-time

### 2. Subtype Pricing
**Try**: Select different waste subtypes to see different rates:
- PET bottles: ₹15/kg
- HDPE: ₹12/kg
- Aluminum: ₹80/kg
- Copper: ₹400/kg

### 3. Marketplace Filters
**Try**: Filter listings by:
- Waste type
- Location (city)
- Price range
- Condition

### 4. Transaction History
**URL**: `/api/marketplace/transactions` (with JWT token)
**View**: All your purchases and sales with platform fees

---

## 📊 Sample Data for Testing

### Create Test Listing 1: High-Value Metal
```
Title: "Copper Wires - 10kg"
Waste Type: Metal
Subtype: Copper
Quantity: 10 kg
Estimated Value: ₹4,000
Asking Price: ₹3,800
City: Mumbai
```

### Create Test Listing 2: Plastic Bottles
```
Title: "Mixed PET Bottles - 100kg"
Waste Type: Plastic
Subtype: PET bottles
Quantity: 100 kg
Estimated Value: ₹1,500
Asking Price: ₹1,400
City: Delhi
```

### Test Booking with Price Calculation
```
Waste Type: Metal
Subtype: Aluminum
Quantity: 20 kg
Expected Value: ₹1,600
Collection Cost: ₹177
Net Earning: ₹1,423
```

---

## 🔐 Authentication Required

All marketplace operations require login:
1. Click "Login" in the top-right corner
2. Use existing account or register new
3. Once logged in, you can:
   - Create listings
   - Book waste
   - View your listings
   - View your bookings
   - See transaction history

---

## 📱 Navigation Quick Reference

| Link | URL Hash | Description |
|------|----------|-------------|
| Home | `#home` | Classify waste with camera |
| Dashboard | `#dashboard` | User dashboard |
| Bookings | `#bookings` | Collection bookings |
| **Marketplace** | `#marketplace` | **NEW: Buy/sell waste** |
| Services | `#services` | Find collection services |
| Rewards | `#rewards` | Points and badges |
| Analytics | `#analytics` | Statistics and insights |

---

## 🛠️ API Endpoints Quick Reference

### Pricing
```bash
POST /api/marketplace/calculate-price
Body: { waste_type, quantity_kg, waste_subtype }
```

### Listings
```bash
GET  /api/marketplace/listings/search?waste_type=plastic&city=Mumbai
POST /api/marketplace/listings/create
GET  /api/marketplace/listings/{id}
PUT  /api/marketplace/listings/{id}
DELETE /api/marketplace/listings/{id}
GET  /api/marketplace/my-listings
```

### Bookings
```bash
POST /api/marketplace/listings/{id}/book
GET  /api/marketplace/my-bookings
POST /api/marketplace/bookings/{id}/accept
POST /api/marketplace/bookings/{id}/complete
POST /api/marketplace/bookings/{id}/payment
```

### Transactions
```bash
GET  /api/marketplace/transactions?type=purchase
GET  /api/marketplace/transactions?type=sale
```

All endpoints require:
```
Authorization: Bearer <your_jwt_token>
Content-Type: application/json
```

---

## 💡 Pro Tips

### 1. Maximize Your Earnings
- **Separate waste by subtype**: Higher rates for pure materials
- **Clean your waste**: Better condition = better price
- **Bulk listings**: Larger quantities attract more buyers
- **Accurate descriptions**: Include photos (future feature)

### 2. Find Best Deals
- **Use filters**: Narrow down by location to reduce transport
- **Check seller ratings**: Higher-rated sellers = reliable
- **Compare prices**: Browse multiple listings before booking
- **Contact sellers**: Use special instructions for questions

### 3. Understanding Net Amount
```
If Net Amount is POSITIVE (+): You earn money
If Net Amount is NEGATIVE (-): You pay for collection

Example 1: High-value metal
Value: ₹1000, Cost: ₹200 → You earn ₹800 ✓

Example 2: Low-value organic
Value: ₹0, Cost: ₹150 → You pay ₹150 ✗
```

---

## 🐛 Troubleshooting

### "Cannot create listing"
- **Check**: Are you logged in?
- **Check**: Are all required fields filled?
- **Try**: Refresh the page and try again

### "Price not calculating"
- **Check**: Is quantity entered?
- **Check**: Is quantity greater than 0?
- **Try**: Change waste type and change back

### "Listing not appearing"
- **Check**: Status should be "active"
- **Check**: Expiry date (30 days from creation)
- **Try**: Refresh the marketplace page

### "Cannot book listing"
- **Check**: Are you logged in?
- **Check**: Are you trying to book your own listing? (Not allowed)
- **Check**: Is listing still "active"?

---

## 📞 Testing Checklist

Before deployment, test:

- [ ] Create a listing with all fields
- [ ] Search listings with filters
- [ ] View listing details
- [ ] Book a listing (not your own)
- [ ] View "My Listings"
- [ ] View "My Bookings"
- [ ] Update a listing
- [ ] Delete a listing (with no active bookings)
- [ ] Test price calculation in booking form
- [ ] Test with different waste types and subtypes
- [ ] Test on mobile device
- [ ] Test authentication flow

---

## 🎨 UI Elements

### Status Badges
- **Active** (Green): Available for booking
- **Booked** (Orange): Someone booked it
- **Pending** (Yellow): Awaiting confirmation
- **Confirmed** (Green): Booking confirmed
- **Completed** (Teal): Transaction done

### Price Display
- **Green (+)**: Earning money
- **Red (-)**: Paying money
- **Bold**: Total/Net amount

---

## 📈 What's Next?

Try these workflows:

1. **As a Waste Generator (Seller)**:
   - Classify waste → Create marketplace listing → Wait for bookings → Accept booking → Complete transaction

2. **As a Waste Collector (Buyer)**:
   - Browse marketplace → Filter by location/type → Book listing → Complete payment → Arrange pickup

3. **As a Regular User**:
   - Classify waste → Book collection service → See if you earn or pay → Schedule pickup

---

## 🎉 Success Indicators

You'll know it's working when:
- ✓ Listings appear in the marketplace grid
- ✓ Price calculations update in real-time
- ✓ Filters modify the displayed listings
- ✓ Bookings show in "My Bookings" section
- ✓ Net amount shows positive for valuable waste
- ✓ Transactions are recorded in the database

---

## 📚 Additional Resources

- **Full Documentation**: See `IMPLEMENTATION_SUMMARY.md`
- **Database Schema**: Check `backend/models/database.py`
- **Pricing Logic**: Review `backend/utils/pricing.py`
- **API Code**: See `backend/routes/marketplace.py`
- **UI Components**: Check `frontend/src/components/Marketplace/`

---

## ⚠️ Important Notes

1. **Demo Mode**: Payment gateway is currently mocked (Razorpay test mode)
2. **Platform Fee**: 5% deducted on all marketplace transactions
3. **Minimum Booking**: ₹50 minimum for collection services
4. **Listing Expiry**: Listings expire after 30 days
5. **Authentication**: JWT tokens required for all marketplace operations

---

## 🎯 Ready to Start?

1. **Start both servers** (backend & frontend)
2. **Login or register** an account
3. **Navigate to Marketplace** (🛒 icon)
4. **Create your first listing** or browse existing ones
5. **Test the price calculator** in the booking form

Enjoy your new WasteWise features! 🌱♻️

---

**Last Updated**: 2025-10-29
**Version**: 1.0.0
