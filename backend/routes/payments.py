from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from datetime import datetime, timedelta
import uuid
import hashlib
import hmac
import os
import razorpay

from middleware.auth import AuthMiddleware
from utils.validators import PaymentSchema, validate_json_request
from models.demo_data import demo_data

# Create blueprint
payments_bp = Blueprint('payments', __name__, url_prefix='/api/payments')

# Load Razorpay credentials from environment variables
RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID')
RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET')

# Validate that keys are present
if not RAZORPAY_KEY_ID or not RAZORPAY_KEY_SECRET:
    raise ValueError("RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET must be set in environment variables")

class PaymentManager:
    """Real Razorpay payment manager"""

    def __init__(self):
        """Initialize Razorpay client"""
        self.client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        # Enable auto-capture for payments
        self.client.set_app_details({"title": "WasteWise", "version": "1.0.0"})

    def create_order(self, amount, currency='INR', receipt=None):
        """Create a payment order using Razorpay API"""
        try:
            order_data = {
                'amount': int(amount * 100),  # Amount in paisa (smallest currency unit)
                'currency': currency,
                'receipt': receipt or f"rcpt_{uuid.uuid4().hex[:12]}",
                'payment_capture': 1  # Auto-capture payment
            }

            # Create order via Razorpay API
            order = self.client.order.create(data=order_data)
            return order

        except razorpay.errors.BadRequestError as e:
            raise Exception(f"Razorpay order creation failed: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to create payment order: {str(e)}")

    def verify_payment_signature(self, order_id, payment_id, signature):
        """Verify payment signature using Razorpay's verification"""
        try:
            # Razorpay's utility method for signature verification
            params_dict = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # This will raise SignatureVerificationError if verification fails
            self.client.utility.verify_payment_signature(params_dict)
            return True

        except razorpay.errors.SignatureVerificationError:
            return False
        except Exception as e:
            print(f"Signature verification error: {str(e)}")
            return False

    def fetch_payment(self, payment_id):
        """Fetch payment details from Razorpay"""
        try:
            payment = self.client.payment.fetch(payment_id)
            return payment
        except Exception as e:
            raise Exception(f"Failed to fetch payment: {str(e)}")

    def capture_payment(self, payment_id, amount):
        """Capture payment (if not auto-captured)"""
        try:
            # Amount in paisa
            capture_data = {'amount': int(amount * 100)}
            payment = self.client.payment.capture(payment_id, capture_data['amount'])
            return payment
        except Exception as e:
            raise Exception(f"Failed to capture payment: {str(e)}")

    def create_refund(self, payment_id, amount, reason='requested_by_customer'):
        """Create refund using Razorpay API"""
        try:
            refund_data = {
                'amount': int(amount),  # Amount already in paisa
                'speed': 'normal',  # 'normal' or 'optimum'
                'notes': {
                    'reason': reason
                }
            }

            # Create refund via Razorpay API
            refund = self.client.payment.refund(payment_id, refund_data)
            return refund

        except razorpay.errors.BadRequestError as e:
            raise Exception(f"Razorpay refund failed: {str(e)}")
        except Exception as e:
            raise Exception(f"Failed to create refund: {str(e)}")

    def fetch_order(self, order_id):
        """Fetch order details from Razorpay"""
        try:
            order = self.client.order.fetch(order_id)
            return order
        except Exception as e:
            raise Exception(f"Failed to fetch order: {str(e)}")

# Initialize payment manager
payment_manager = PaymentManager()

@payments_bp.route('/initiate', methods=['POST'])
@AuthMiddleware.jwt_required
@validate_json_request(PaymentSchema)
def initiate_payment():
    """Initiate payment for a booking"""
    try:
        current_user_id = get_jwt_identity()
        payment_data = request.validated_data

        booking_id = payment_data['booking_id']
        amount = payment_data['amount']
        payment_method = payment_data['payment_method']

        # Find booking
        booking = next((b for b in demo_data.bookings if b['id'] == booking_id), None)

        if not booking:
            return jsonify({
                'error': 'Booking not found',
                'message': f'No booking found with ID {booking_id}'
            }), 404

        # Check if user owns this booking
        if booking.get('user_id') != current_user_id:
            return jsonify({
                'error': 'Access denied',
                'message': 'You can only pay for your own bookings'
            }), 403

        # Check if payment is already made
        if booking.get('payment_status') == 'paid':
            return jsonify({
                'error': 'Payment already completed',
                'message': 'This booking has already been paid for'
            }), 400

        # Validate amount
        estimated_cost = booking.get('estimated_cost', 0)

        # Check if this is a payment (negative amount) or earning (positive amount)
        is_earning = estimated_cost > 0

        if is_earning:
            # User should receive money, not pay
            return jsonify({
                'error': 'Payment not required',
                'message': f'This booking generates earnings of ₹{abs(estimated_cost):.2f} for you. No payment needed.',
                'earning_amount': abs(estimated_cost),
                'transaction_type': 'earning'
            }), 400

        # For payment scenarios, validate amount matches
        if amount != abs(estimated_cost):
            return jsonify({
                'error': 'Invalid amount',
                'message': f'Payment amount does not match booking cost of ₹{abs(estimated_cost):.2f}'
            }), 400

        # Create payment order
        order = payment_manager.create_order(
            amount=amount,
            receipt=f"booking_{booking_id}"
        )

        # Create payment record
        payment_id = str(uuid.uuid4())
        payment_record = {
            'id': payment_id,
            'booking_id': booking_id,
            'user_id': current_user_id,
            'order_id': order['id'],
            'amount': amount,
            'currency': 'INR',
            'payment_method': payment_method,
            'status': 'initiated',
            'gateway': 'razorpay',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'gateway_order': order
        }

        # Store payment record (in real app, this would be in database)
        if not hasattr(demo_data, 'payments'):
            demo_data.payments = []
        demo_data.payments.append(payment_record)

        # Update booking payment status
        booking['payment_status'] = 'initiated'
        booking['payment_id'] = payment_id

        # Prepare response based on payment method
        response_data = {
            'success': True,
            'payment_id': payment_id,
            'order_id': order['id'],
            'amount': amount,
            'currency': 'INR',
            'booking_id': booking_id
        }

        if payment_method == 'card':
            response_data.update({
                'gateway_key': RAZORPAY_KEY_ID,
                'checkout_url': f"https://checkout.razorpay.com/v1/checkout.js",
                'options': {
                    'order_id': order['id'],
                    'amount': order['amount'],
                    'currency': 'INR',
                    'name': 'WasteWise',
                    'description': f'Payment for booking {booking_id}',
                    'prefill': {
                        'email': 'user@example.com',  # Would come from user profile
                        'contact': '9999999999'
                    },
                    'theme': {
                        'color': '#4CAF50'
                    }
                }
            })
        elif payment_method == 'upi':
            response_data.update({
                'upi_link': f"upi://pay?pa=merchant@razorpay&pn=WasteWise&am={amount}&tn=Payment for booking {booking_id}&cu=INR",
                'qr_code': f"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="  # Mock QR code
            })

        return jsonify(response_data), 201

    except Exception as e:
        return jsonify({
            'error': 'Payment initiation failed',
            'message': str(e)
        }), 500

@payments_bp.route('/verify', methods=['POST'])
@AuthMiddleware.jwt_required
def verify_payment():
    """Verify payment completion"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()

        payment_id = data.get('payment_id')
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_signature = data.get('razorpay_signature')

        if not all([payment_id, razorpay_order_id, razorpay_payment_id, razorpay_signature]):
            return jsonify({
                'error': 'Missing payment details',
                'message': 'All payment verification parameters are required'
            }), 400

        # Find payment record
        if not hasattr(demo_data, 'payments'):
            demo_data.payments = []

        payment = next((p for p in demo_data.payments if p['id'] == payment_id), None)

        if not payment:
            return jsonify({
                'error': 'Payment not found',
                'message': f'No payment found with ID {payment_id}'
            }), 404

        # Check ownership
        if payment['user_id'] != current_user_id:
            return jsonify({
                'error': 'Access denied',
                'message': 'You can only verify your own payments'
            }), 403

        # Verify payment signature
        # Check if this is a test/simulated payment (payment_id starts with 'pay_')
        is_simulated = razorpay_payment_id.startswith('pay_') and len(razorpay_payment_id) < 20

        if is_simulated:
            # For simulated payments (testing), skip Razorpay verification
            # This allows testing without actual Razorpay transactions
            print(f"Simulated payment detected, skipping signature verification")
            is_valid = True
        else:
            # For real Razorpay payments, verify the signature
            is_valid = payment_manager.verify_payment_signature(
                razorpay_order_id, razorpay_payment_id, razorpay_signature
            )

        if not is_valid:
            return jsonify({
                'error': 'Payment verification failed',
                'message': 'Invalid payment signature'
            }), 400

        # Update payment record
        payment['status'] = 'completed'
        payment['razorpay_payment_id'] = razorpay_payment_id
        payment['razorpay_signature'] = razorpay_signature
        payment['completed_at'] = datetime.now().isoformat()
        payment['updated_at'] = datetime.now().isoformat()

        # Update booking
        booking = next((b for b in demo_data.bookings if b['id'] == payment['booking_id']), None)
        if booking:
            booking['payment_status'] = 'paid'
            booking['paid_at'] = datetime.now().isoformat()
            booking['actual_cost'] = payment['amount']

        # Create transaction record
        transaction = {
            'id': str(uuid.uuid4()),
            'payment_id': payment_id,
            'booking_id': payment['booking_id'],
            'user_id': current_user_id,
            'type': 'payment',
            'amount': payment['amount'],
            'status': 'success',
            'gateway_transaction_id': razorpay_payment_id,
            'created_at': datetime.now().isoformat()
        }

        if not hasattr(demo_data, 'transactions'):
            demo_data.transactions = []
        demo_data.transactions.append(transaction)

        return jsonify({
            'success': True,
            'message': 'Payment verified successfully',
            'payment': payment,
            'transaction_id': transaction['id'],
            'booking_status': 'confirmed'
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Payment verification failed',
            'message': str(e)
        }), 500

@payments_bp.route('/history', methods=['GET'])
@AuthMiddleware.jwt_required
def get_payment_history():
    """Get user's payment history"""
    try:
        current_user_id = get_jwt_identity()

        # Query parameters
        limit = request.args.get('limit', 20, type=int)
        offset = request.args.get('offset', 0, type=int)
        status = request.args.get('status')  # initiated, completed, failed, refunded

        if not hasattr(demo_data, 'payments'):
            demo_data.payments = []

        # Filter payments for current user
        user_payments = [p for p in demo_data.payments if p['user_id'] == current_user_id]

        # Apply status filter
        if status:
            user_payments = [p for p in user_payments if p['status'] == status]

        # Sort by creation date (newest first)
        user_payments.sort(key=lambda x: x['created_at'], reverse=True)

        # Apply pagination
        total_payments = len(user_payments)
        paginated_payments = user_payments[offset:offset + limit]

        # Enhance payments with booking details
        enhanced_payments = []
        for payment in paginated_payments:
            booking = next((b for b in demo_data.bookings if b['id'] == payment['booking_id']), None)
            enhanced_payment = {
                **payment,
                'booking_details': {
                    'waste_type': booking.get('waste_type', 'N/A'),
                    'quantity': booking.get('quantity', 'N/A'),
                    'pickup_address': booking.get('pickup_address', 'N/A'),
                    'scheduled_date': booking.get('scheduled_date', 'N/A')
                } if booking else None
            }
            enhanced_payments.append(enhanced_payment)

        return jsonify({
            'success': True,
            'payments': enhanced_payments,
            'pagination': {
                'total': total_payments,
                'limit': limit,
                'offset': offset,
                'has_more': offset + limit < total_payments
            },
            'summary': {
                'total_paid': sum(p['amount'] for p in user_payments if p['status'] == 'completed'),
                'pending_payments': len([p for p in user_payments if p['status'] == 'initiated']),
                'completed_payments': len([p for p in user_payments if p['status'] == 'completed'])
            }
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve payment history',
            'message': str(e)
        }), 500

@payments_bp.route('/<payment_id>/refund', methods=['POST'])
@AuthMiddleware.jwt_required
def request_refund(payment_id):
    """Request refund for a payment"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json() or {}
        refund_reason = data.get('reason', 'Customer requested refund')

        if not hasattr(demo_data, 'payments'):
            return jsonify({'error': 'Payment not found'}), 404

        # Find payment
        payment = next((p for p in demo_data.payments if p['id'] == payment_id), None)

        if not payment:
            return jsonify({'error': 'Payment not found'}), 404

        # Check ownership
        if payment['user_id'] != current_user_id:
            return jsonify({'error': 'Access denied'}), 403

        # Check if payment can be refunded
        if payment['status'] != 'completed':
            return jsonify({
                'error': 'Refund not allowed',
                'message': 'Only completed payments can be refunded'
            }), 400

        # Check if already refunded
        if payment.get('refund_status') == 'refunded':
            return jsonify({
                'error': 'Already refunded',
                'message': 'This payment has already been refunded'
            }), 400

        # Find associated booking
        booking = next((b for b in demo_data.bookings if b['id'] == payment['booking_id']), None)

        # Check refund eligibility based on booking status
        if booking and booking.get('status') in ['in_progress', 'completed']:
            return jsonify({
                'error': 'Refund not allowed',
                'message': 'Cannot refund payment for bookings that are in progress or completed'
            }), 400

        # Calculate refund amount
        refund_amount = payment['amount']
        processing_fee = 0

        # Apply processing fee if booking is scheduled soon
        if booking:
            scheduled_time = datetime.fromisoformat(booking['scheduled_date'])
            hours_until_pickup = (scheduled_time - datetime.now()).total_seconds() / 3600
            if hours_until_pickup < 24:
                processing_fee = payment['amount'] * 0.1  # 10% processing fee

        final_refund_amount = refund_amount - processing_fee

        # Create refund via payment gateway
        gateway_refund = payment_manager.create_refund(
            payment.get('razorpay_payment_id', 'mock_payment_id'),
            int(final_refund_amount * 100),  # Amount in paisa
            refund_reason
        )

        # Update payment record
        payment['refund_status'] = 'refunded'
        payment['refund_amount'] = final_refund_amount
        payment['processing_fee'] = processing_fee
        payment['refund_reason'] = refund_reason
        payment['refunded_at'] = datetime.now().isoformat()
        payment['gateway_refund_id'] = gateway_refund['id']
        payment['updated_at'] = datetime.now().isoformat()

        # Update booking if exists
        if booking:
            booking['payment_status'] = 'refunded'
            booking['status'] = 'cancelled'
            booking['refunded_at'] = datetime.now().isoformat()

        # Create refund transaction
        refund_transaction = {
            'id': str(uuid.uuid4()),
            'payment_id': payment_id,
            'booking_id': payment['booking_id'],
            'user_id': current_user_id,
            'type': 'refund',
            'amount': -final_refund_amount,  # Negative for refund
            'status': 'success',
            'gateway_transaction_id': gateway_refund['id'],
            'reason': refund_reason,
            'created_at': datetime.now().isoformat()
        }

        if not hasattr(demo_data, 'transactions'):
            demo_data.transactions = []
        demo_data.transactions.append(refund_transaction)

        return jsonify({
            'success': True,
            'message': 'Refund processed successfully',
            'refund': {
                'refund_id': gateway_refund['id'],
                'amount': final_refund_amount,
                'processing_fee': processing_fee,
                'reason': refund_reason,
                'estimated_credit_time': '3-5 business days'
            },
            'transaction_id': refund_transaction['id']
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Refund processing failed',
            'message': str(e)
        }), 500

@payments_bp.route('/complete-earning', methods=['POST'])
@AuthMiddleware.jwt_required
def complete_earning():
    """Complete earning transaction for waste collection (user gets paid)"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()

        booking_id = data.get('booking_id')

        if not booking_id:
            return jsonify({
                'error': 'Missing booking_id',
                'message': 'booking_id is required'
            }), 400

        # Find booking
        booking = next((b for b in demo_data.bookings if b['id'] == booking_id), None)

        if not booking:
            return jsonify({
                'error': 'Booking not found',
                'message': f'No booking found with ID {booking_id}'
            }), 404

        # Check if user owns this booking
        if booking.get('user_id') != current_user_id:
            return jsonify({
                'error': 'Access denied',
                'message': 'You can only complete your own bookings'
            }), 403

        # Check if earning is already completed
        if booking.get('payment_status') == 'paid':
            return jsonify({
                'error': 'Already completed',
                'message': 'This earning has already been processed'
            }), 400

        # Get estimated earning (should be positive)
        estimated_earning = booking.get('estimated_cost', 0)

        if estimated_earning <= 0:
            return jsonify({
                'error': 'No earnings',
                'message': 'This booking does not generate earnings. You need to pay for collection.'
            }), 400

        # Create earning record
        earning_id = str(uuid.uuid4())
        earning_record = {
            'id': earning_id,
            'booking_id': booking_id,
            'user_id': current_user_id,
            'amount': estimated_earning,
            'currency': 'INR',
            'status': 'completed',
            'type': 'earning',
            'created_at': datetime.now().isoformat(),
            'completed_at': datetime.now().isoformat(),
            'payment_method': 'bank_transfer',  # Can be UPI, bank transfer, etc.
            'description': f'Earnings from waste collection - {booking["waste_type"]} waste'
        }

        # Store earning record
        if not hasattr(demo_data, 'payments'):
            demo_data.payments = []
        demo_data.payments.append(earning_record)

        # Update booking
        booking['payment_status'] = 'paid'
        booking['paid_at'] = datetime.now().isoformat()
        booking['actual_cost'] = estimated_earning
        booking['payment_id'] = earning_id

        # Create transaction record
        transaction = {
            'id': str(uuid.uuid4()),
            'payment_id': earning_id,
            'booking_id': booking_id,
            'user_id': current_user_id,
            'type': 'earning',
            'amount': estimated_earning,
            'status': 'success',
            'created_at': datetime.now().isoformat()
        }

        if not hasattr(demo_data, 'transactions'):
            demo_data.transactions = []
        demo_data.transactions.append(transaction)

        return jsonify({
            'success': True,
            'message': f'Congratulations! You earned ₹{estimated_earning:.2f}',
            'earning': earning_record,
            'transaction_id': transaction['id'],
            'booking_status': 'confirmed',
            'payout_info': {
                'amount': estimated_earning,
                'currency': 'INR',
                'estimated_credit_time': '2-3 business days',
                'payout_method': 'Bank Transfer / UPI'
            }
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Earning processing failed',
            'message': str(e)
        }), 500

@payments_bp.route('/methods', methods=['GET'])
def get_payment_methods():
    """Get available payment methods"""
    try:
        payment_methods = [
            {
                'id': 'card',
                'name': 'Credit/Debit Card',
                'description': 'Pay using your credit or debit card',
                'icon': 'credit-card',
                'processing_fee': 2.5,  # percentage
                'supported_networks': ['Visa', 'MasterCard', 'RuPay', 'American Express'],
                'available': True
            },
            {
                'id': 'upi',
                'name': 'UPI',
                'description': 'Pay using UPI apps like GPay, PhonePe, Paytm',
                'icon': 'smartphone',
                'processing_fee': 0,
                'supported_apps': ['Google Pay', 'PhonePe', 'Paytm', 'BHIM'],
                'available': True
            },
            {
                'id': 'netbanking',
                'name': 'Net Banking',
                'description': 'Pay directly from your bank account',
                'icon': 'bank',
                'processing_fee': 0,
                'supported_banks': ['SBI', 'HDFC', 'ICICI', 'Axis', 'PNB'],
                'available': True
            },
            {
                'id': 'wallet',
                'name': 'Digital Wallet',
                'description': 'Pay using digital wallets',
                'icon': 'wallet',
                'processing_fee': 1.5,
                'supported_wallets': ['Paytm', 'PhonePe', 'Amazon Pay', 'Mobikwik'],
                'available': True
            }
        ]

        return jsonify({
            'success': True,
            'payment_methods': payment_methods,
            'currency': 'INR',
            'gateway_info': {
                'provider': 'Razorpay',
                'security_features': ['256-bit SSL', 'PCI DSS Compliant', '3D Secure'],
                'supported_currencies': ['INR']
            }
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve payment methods',
            'message': str(e)
        }), 500

@payments_bp.route('/webhook', methods=['POST'])
def payment_webhook():
    """Handle payment gateway webhooks"""
    try:
        # This would handle actual webhook events from payment gateway
        # For demo purposes, we'll simulate webhook processing

        webhook_data = request.get_json()
        event_type = webhook_data.get('event', 'payment.captured')

        if event_type == 'payment.captured':
            # Handle successful payment
            payment_id = webhook_data.get('payload', {}).get('payment', {}).get('entity', {}).get('id')

            # Process payment confirmation
            # Update database, send notifications, etc.

            return jsonify({'status': 'ok'}), 200

        elif event_type == 'payment.failed':
            # Handle failed payment
            payment_id = webhook_data.get('payload', {}).get('payment', {}).get('entity', {}).get('id')

            # Update payment status, notify user, etc.

            return jsonify({'status': 'ok'}), 200

        return jsonify({'status': 'ignored'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500