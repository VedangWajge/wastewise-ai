# Razorpay Quick Reference

## Test the Integration
```bash
cd backend
./venv/Scripts/python test_razorpay_integration.py
```

## Test Payment Cards

### Success Card:
```
Card: 4111 1111 1111 1111
CVV: 123
Expiry: 12/25
Name: Test User
```

### Decline Card:
```
Card: 4000 0000 0000 0002
```

## Test UPI:
```
success@razorpay  → Payment succeeds
failure@razorpay  → Payment fails
```

## Environment Setup

### .env file (backend/.env):
```bash
RAZORPAY_KEY_ID=rzp_test_RZVRElVZ45KgXB
RAZORPAY_KEY_SECRET=qioPSGjqZmepkMi8GBpkpkKw
```

## Payment Flow

1. **User**: Clicks "Pay Now" on booking
2. **Backend**: Creates Razorpay order
3. **Frontend**: Opens Razorpay checkout
4. **User**: Completes payment
5. **Backend**: Verifies signature
6. **Success**: Booking confirmed

## Key API Endpoints

### Initiate Payment
```http
POST /api/payments/initiate
Authorization: Bearer <token>
Content-Type: application/json

{
  "booking_id": "book_123",
  "amount": 420.50,
  "payment_method": "card"
}
```

### Verify Payment
```http
POST /api/payments/verify
Authorization: Bearer <token>
Content-Type: application/json

{
  "payment_id": "payment_internal_id",
  "razorpay_order_id": "order_xxx",
  "razorpay_payment_id": "pay_yyy",
  "razorpay_signature": "signature..."
}
```

## Check Payment Status

### Test Dashboard:
https://dashboard.razorpay.com/test/payments

### Live Dashboard:
https://dashboard.razorpay.com/live/payments

## Going Live

1. Get live keys from Razorpay dashboard
2. Update `.env`:
   ```bash
   RAZORPAY_KEY_ID=rzp_live_YOUR_KEY
   RAZORPAY_KEY_SECRET=your_secret
   ```
3. Complete KYC verification
4. Test with small real transactions
5. Set up webhooks

## Common Issues

### "Module not found: razorpay"
```bash
pip install razorpay
```

### "Invalid credentials"
- Check `.env` file exists
- Verify keys are correct
- Ensure `load_dotenv()` is called

### "Signature verification failed"
- Check using correct key_secret
- Verify order_id matches
- Check signature format

## Support

- Docs: https://razorpay.com/docs/
- Dashboard: https://dashboard.razorpay.com
- Email: support@razorpay.com
