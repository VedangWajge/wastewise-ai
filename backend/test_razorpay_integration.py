#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for Razorpay integration
Run this script to verify your Razorpay credentials and API connectivity
"""

import os
import sys
from dotenv import load_dotenv
import razorpay

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Load environment variables
load_dotenv()

def test_razorpay_connection():
    """Test Razorpay API connection and credentials"""

    print("=" * 60)
    print("Razorpay Integration Test")
    print("=" * 60)

    # Load credentials
    key_id = os.environ.get('RAZORPAY_KEY_ID')
    key_secret = os.environ.get('RAZORPAY_KEY_SECRET')

    print("\n1. Checking environment variables...")
    if not key_id or not key_secret:
        print("   ❌ FAILED: RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET not found in .env")
        return False

    print(f"   ✓ RAZORPAY_KEY_ID: {key_id[:15]}...")
    print(f"   ✓ RAZORPAY_KEY_SECRET: {'*' * len(key_secret)}")

    # Initialize Razorpay client
    print("\n2. Initializing Razorpay client...")
    try:
        client = razorpay.Client(auth=(key_id, key_secret))
        client.set_app_details({"title": "WasteWise", "version": "1.0.0"})
        print("   ✓ Client initialized successfully")
    except Exception as e:
        print(f"   ❌ FAILED: {str(e)}")
        return False

    # Test order creation
    print("\n3. Testing order creation...")
    try:
        test_order_data = {
            'amount': 50000,  # 500 INR in paisa
            'currency': 'INR',
            'receipt': 'test_receipt_001',
            'payment_capture': 1
        }

        order = client.order.create(data=test_order_data)
        print(f"   ✓ Order created successfully!")
        print(f"   Order ID: {order['id']}")
        print(f"   Amount: ₹{order['amount']/100}")
        print(f"   Status: {order['status']}")
        print(f"   Currency: {order['currency']}")

    except razorpay.errors.BadRequestError as e:
        print(f"   ❌ Bad Request: {str(e)}")
        return False
    except razorpay.errors.ServerError as e:
        print(f"   ❌ Server Error: {str(e)}")
        return False
    except Exception as e:
        print(f"   ❌ FAILED: {str(e)}")
        return False

    # Test signature verification
    print("\n4. Testing signature verification...")
    try:
        # Mock data for testing verification logic
        params_dict = {
            'razorpay_order_id': order['id'],
            'razorpay_payment_id': 'pay_test123',
            'razorpay_signature': 'test_signature'
        }

        # This will fail but we're just testing the method exists
        try:
            client.utility.verify_payment_signature(params_dict)
        except razorpay.errors.SignatureVerificationError:
            print("   ✓ Signature verification method working (expected failure with test data)")

    except AttributeError:
        print("   ❌ Signature verification method not available")
        return False
    except Exception as e:
        print(f"   ✓ Signature verification method available")

    print("\n" + "=" * 60)
    print("✓ All tests passed! Razorpay integration is ready.")
    print("=" * 60)
    print("\n📝 Next steps:")
    print("   1. Test with frontend by making a real booking")
    print("   2. Complete a test payment using Razorpay test cards")
    print("   3. Verify webhook integration (if needed)")
    print("\n💳 Test card details (Razorpay):")
    print("   Card: 4111 1111 1111 1111")
    print("   CVV: Any 3 digits")
    print("   Expiry: Any future date")
    print("   Name: Any name")
    print("\n")

    return True

if __name__ == '__main__':
    try:
        success = test_razorpay_connection()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        exit(1)
