"""
Marketplace routes for listing and booking waste
OLX-style platform where users can list waste and others can book it
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import sqlite3
import uuid
from datetime import datetime, timedelta
from utils.pricing import WastePricing
import os

marketplace_bp = Blueprint('marketplace', __name__, url_prefix='/api/marketplace')

def get_db_connection():
    """Get database connection"""
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'wastewise.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@marketplace_bp.route('/listings/create', methods=['POST'])
@jwt_required()
def create_listing():
    """Create a new marketplace listing"""
    try:
        user_id = get_jwt_identity()
        data = request.json

        # Validate required fields
        required_fields = ['title', 'waste_type', 'quantity_kg', 'location']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Calculate estimated value
        waste_type = data['waste_type']
        quantity_kg = float(data['quantity_kg'])
        waste_subtype = data.get('waste_subtype', 'mixed')

        pricing = WastePricing.calculate_waste_value(waste_type, quantity_kg, waste_subtype)

        # Create listing
        listing_id = f"listing_{uuid.uuid4().hex[:12]}"

        conn = get_db_connection()
        cursor = conn.cursor()

        # Set expiration (30 days from now)
        expires_at = (datetime.now() + timedelta(days=30)).isoformat()

        cursor.execute('''
            INSERT INTO marketplace_listings
            (id, user_id, title, description, waste_type, waste_subtype, quantity_kg,
             estimated_value, asking_price, location, latitude, longitude, city, state, pincode,
             condition, pickup_available, delivery_available, status, expires_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            listing_id,
            user_id,
            data['title'],
            data.get('description', ''),
            waste_type,
            waste_subtype,
            quantity_kg,
            pricing['total_value'],
            data.get('asking_price', pricing['total_value']),
            data['location'],
            data.get('latitude'),
            data.get('longitude'),
            data.get('city'),
            data.get('state'),
            data.get('pincode'),
            data.get('condition', 'good'),
            data.get('pickup_available', True),
            data.get('delivery_available', False),
            'active',
            expires_at
        ))

        conn.commit()
        conn.close()

        return jsonify({
            'message': 'Listing created successfully',
            'listing_id': listing_id,
            'estimated_value': pricing['total_value'],
            'pricing_details': pricing
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@marketplace_bp.route('/listings/search', methods=['GET'])
def search_listings():
    """Search marketplace listings with filters"""
    try:
        # Get query parameters
        waste_type = request.args.get('waste_type')
        city = request.args.get('city')
        min_quantity = request.args.get('min_quantity', type=float)
        max_quantity = request.args.get('max_quantity', type=float)
        max_price = request.args.get('max_price', type=float)
        condition = request.args.get('condition')
        sort_by = request.args.get('sort_by', 'created_at')
        order = request.args.get('order', 'DESC')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)

        conn = get_db_connection()
        cursor = conn.cursor()

        # Build query
        query = '''
            SELECT l.*, u.full_name as seller_name, u.phone as seller_phone
            FROM marketplace_listings l
            JOIN users u ON l.user_id = u.id
            WHERE l.status = 'active'
        '''
        params = []

        if waste_type:
            query += ' AND l.waste_type = ?'
            params.append(waste_type)

        if city:
            query += ' AND l.city LIKE ?'
            params.append(f'%{city}%')

        if min_quantity:
            query += ' AND l.quantity_kg >= ?'
            params.append(min_quantity)

        if max_quantity:
            query += ' AND l.quantity_kg <= ?'
            params.append(max_quantity)

        if max_price:
            query += ' AND l.asking_price <= ?'
            params.append(max_price)

        if condition:
            query += ' AND l.condition = ?'
            params.append(condition)

        # Add sorting
        allowed_sort_fields = ['created_at', 'asking_price', 'quantity_kg', 'views_count']
        if sort_by in allowed_sort_fields:
            query += f' ORDER BY l.{sort_by} {order}'
        else:
            query += ' ORDER BY l.created_at DESC'

        # Add pagination
        offset = (page - 1) * per_page
        query += ' LIMIT ? OFFSET ?'
        params.extend([per_page, offset])

        cursor.execute(query, params)
        listings = [dict(row) for row in cursor.fetchall()]

        # Get total count
        count_query = '''
            SELECT COUNT(*) as total
            FROM marketplace_listings l
            WHERE l.status = 'active'
        '''
        count_params = []

        if waste_type:
            count_query += ' AND l.waste_type = ?'
            count_params.append(waste_type)

        if city:
            count_query += ' AND l.city LIKE ?'
            count_params.append(f'%{city}%')

        if min_quantity:
            count_query += ' AND l.quantity_kg >= ?'
            count_params.append(min_quantity)

        if max_quantity:
            count_query += ' AND l.quantity_kg <= ?'
            count_params.append(max_quantity)

        if max_price:
            count_query += ' AND l.asking_price <= ?'
            count_params.append(max_price)

        if condition:
            count_query += ' AND l.condition = ?'
            count_params.append(condition)

        cursor.execute(count_query, count_params)
        total = cursor.fetchone()['total']

        conn.close()

        return jsonify({
            'listings': listings,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@marketplace_bp.route('/listings/<listing_id>', methods=['GET'])
def get_listing_details(listing_id):
    """Get detailed information about a listing"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Increment view count
        cursor.execute('''
            UPDATE marketplace_listings
            SET views_count = views_count + 1
            WHERE id = ?
        ''', (listing_id,))

        # Get listing details
        cursor.execute('''
            SELECT l.*, u.full_name as seller_name, u.phone as seller_phone, u.email as seller_email
            FROM marketplace_listings l
            JOIN users u ON l.user_id = u.id
            WHERE l.id = ?
        ''', (listing_id,))

        listing = cursor.fetchone()
        if not listing:
            conn.close()
            return jsonify({'error': 'Listing not found'}), 404

        listing_dict = dict(listing)

        # Get seller stats
        cursor.execute('''
            SELECT
                COUNT(*) as total_listings,
                AVG(r.rating) as average_rating,
                COUNT(DISTINCT r.id) as total_reviews
            FROM marketplace_listings l
            LEFT JOIN marketplace_bookings b ON l.id = b.listing_id
            LEFT JOIN marketplace_reviews r ON b.id = r.booking_id AND r.reviewed_user_id = l.user_id
            WHERE l.user_id = ?
        ''', (listing_dict['user_id'],))

        seller_stats = dict(cursor.fetchone())
        listing_dict['seller_stats'] = seller_stats

        conn.commit()
        conn.close()

        return jsonify(listing_dict), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@marketplace_bp.route('/listings/<listing_id>/book', methods=['POST'])
@jwt_required()
def book_listing(listing_id):
    """Book a marketplace listing"""
    try:
        buyer_id = get_jwt_identity()
        data = request.json

        conn = get_db_connection()
        cursor = conn.cursor()

        # Get listing details
        cursor.execute('''
            SELECT * FROM marketplace_listings
            WHERE id = ? AND status = 'active'
        ''', (listing_id,))

        listing = cursor.fetchone()
        if not listing:
            conn.close()
            return jsonify({'error': 'Listing not found or not available'}), 404

        listing_dict = dict(listing)
        seller_id = listing_dict['user_id']

        # Check if user is not booking their own listing
        if buyer_id == seller_id:
            conn.close()
            return jsonify({'error': 'Cannot book your own listing'}), 400

        # Create booking
        booking_id = f"mkt_book_{uuid.uuid4().hex[:12]}"

        agreed_price = data.get('agreed_price', listing_dict['asking_price'])
        quantity_kg = data.get('quantity_kg', listing_dict['quantity_kg'])

        cursor.execute('''
            INSERT INTO marketplace_bookings
            (id, listing_id, buyer_id, seller_id, agreed_price, quantity_kg,
             pickup_address, pickup_date, pickup_time_slot, contact_person, contact_phone,
             special_instructions, status, payment_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            booking_id,
            listing_id,
            buyer_id,
            seller_id,
            agreed_price,
            quantity_kg,
            data.get('pickup_address', listing_dict['location']),
            data.get('pickup_date'),
            data.get('pickup_time_slot'),
            data.get('contact_person'),
            data.get('contact_phone'),
            data.get('special_instructions'),
            'pending',
            'pending'
        ))

        # Update listing status if full quantity is booked
        if quantity_kg >= listing_dict['quantity_kg']:
            cursor.execute('''
                UPDATE marketplace_listings
                SET status = 'booked'
                WHERE id = ?
            ''', (listing_id,))

        conn.commit()
        conn.close()

        return jsonify({
            'message': 'Booking created successfully',
            'booking_id': booking_id,
            'agreed_price': agreed_price,
            'next_step': 'Complete payment to confirm booking'
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@marketplace_bp.route('/my-listings', methods=['GET'])
@jwt_required()
def get_my_listings():
    """Get current user's listings"""
    try:
        user_id = get_jwt_identity()
        status = request.args.get('status', 'active')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)

        conn = get_db_connection()
        cursor = conn.cursor()

        offset = (page - 1) * per_page

        if status:
            cursor.execute('''
                SELECT l.*,
                       COUNT(DISTINCT b.id) as booking_count
                FROM marketplace_listings l
                LEFT JOIN marketplace_bookings b ON l.id = b.listing_id
                WHERE l.user_id = ? AND l.status = ?
                GROUP BY l.id
                ORDER BY l.created_at DESC
                LIMIT ? OFFSET ?
            ''', (user_id, status, per_page, offset))
        else:
            cursor.execute('''
                SELECT l.*,
                       COUNT(DISTINCT b.id) as booking_count
                FROM marketplace_listings l
                LEFT JOIN marketplace_bookings b ON l.id = b.listing_id
                WHERE l.user_id = ?
                GROUP BY l.id
                ORDER BY l.created_at DESC
                LIMIT ? OFFSET ?
            ''', (user_id, per_page, offset))

        listings = [dict(row) for row in cursor.fetchall()]

        # Get total count
        if status:
            cursor.execute('''
                SELECT COUNT(*) as total
                FROM marketplace_listings
                WHERE user_id = ? AND status = ?
            ''', (user_id, status))
        else:
            cursor.execute('''
                SELECT COUNT(*) as total
                FROM marketplace_listings
                WHERE user_id = ?
            ''', (user_id,))

        total = cursor.fetchone()['total']

        conn.close()

        return jsonify({
            'listings': listings,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@marketplace_bp.route('/my-bookings', methods=['GET'])
@jwt_required()
def get_my_bookings():
    """Get bookings made by current user (as buyer)"""
    try:
        user_id = get_jwt_identity()
        status = request.args.get('status')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)

        conn = get_db_connection()
        cursor = conn.cursor()

        offset = (page - 1) * per_page

        query = '''
            SELECT b.*,
                   l.title as listing_title,
                   l.waste_type,
                   l.waste_subtype,
                   u.full_name as seller_name,
                   u.phone as seller_phone
            FROM marketplace_bookings b
            JOIN marketplace_listings l ON b.listing_id = l.id
            JOIN users u ON b.seller_id = u.id
            WHERE b.buyer_id = ?
        '''
        params = [user_id]

        if status:
            query += ' AND b.status = ?'
            params.append(status)

        query += ' ORDER BY b.created_at DESC LIMIT ? OFFSET ?'
        params.extend([per_page, offset])

        cursor.execute(query, params)
        bookings = [dict(row) for row in cursor.fetchall()]

        # Get total count
        count_query = 'SELECT COUNT(*) as total FROM marketplace_bookings WHERE buyer_id = ?'
        count_params = [user_id]

        if status:
            count_query += ' AND status = ?'
            count_params.append(status)

        cursor.execute(count_query, count_params)
        total = cursor.fetchone()['total']

        conn.close()

        return jsonify({
            'bookings': bookings,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@marketplace_bp.route('/bookings/<booking_id>/accept', methods=['POST'])
@jwt_required()
def accept_booking(booking_id):
    """Seller accepts a booking"""
    try:
        user_id = get_jwt_identity()

        conn = get_db_connection()
        cursor = conn.cursor()

        # Verify seller owns this booking
        cursor.execute('''
            SELECT * FROM marketplace_bookings
            WHERE id = ? AND seller_id = ?
        ''', (booking_id, user_id))

        booking = cursor.fetchone()
        if not booking:
            conn.close()
            return jsonify({'error': 'Booking not found or unauthorized'}), 404

        # Update booking status
        cursor.execute('''
            UPDATE marketplace_bookings
            SET status = 'confirmed', updated_at = ?
            WHERE id = ?
        ''', (datetime.now().isoformat(), booking_id))

        conn.commit()
        conn.close()

        return jsonify({'message': 'Booking accepted successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@marketplace_bp.route('/bookings/<booking_id>/complete', methods=['POST'])
@jwt_required()
def complete_booking(booking_id):
    """Mark booking as completed"""
    try:
        user_id = get_jwt_identity()

        conn = get_db_connection()
        cursor = conn.cursor()

        # Verify user is part of this booking (buyer or seller)
        cursor.execute('''
            SELECT * FROM marketplace_bookings
            WHERE id = ? AND (buyer_id = ? OR seller_id = ?)
        ''', (booking_id, user_id, user_id))

        booking = cursor.fetchone()
        if not booking:
            conn.close()
            return jsonify({'error': 'Booking not found or unauthorized'}), 404

        # Update booking status
        cursor.execute('''
            UPDATE marketplace_bookings
            SET status = 'completed',
                completed_at = ?,
                updated_at = ?
            WHERE id = ?
        ''', (datetime.now().isoformat(), datetime.now().isoformat(), booking_id))

        conn.commit()
        conn.close()

        return jsonify({'message': 'Booking completed successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@marketplace_bp.route('/calculate-price', methods=['POST'])
def calculate_price():
    """Calculate estimated price for waste"""
    try:
        data = request.json

        waste_type = data.get('waste_type')
        quantity_kg = data.get('quantity_kg')
        waste_subtype = data.get('waste_subtype', 'mixed')

        if not waste_type or not quantity_kg:
            return jsonify({'error': 'Missing required fields'}), 400

        # Calculate waste value
        pricing = WastePricing.calculate_waste_value(waste_type, quantity_kg, waste_subtype)

        # Also get available subtypes
        subtypes = WastePricing.get_waste_subtypes(waste_type)

        return jsonify({
            'pricing': pricing,
            'available_subtypes': subtypes
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@marketplace_bp.route('/listings/<listing_id>', methods=['PUT'])
@jwt_required()
def update_listing(listing_id):
    """Update a listing"""
    try:
        user_id = get_jwt_identity()
        data = request.json

        conn = get_db_connection()
        cursor = conn.cursor()

        # Verify ownership
        cursor.execute('''
            SELECT * FROM marketplace_listings
            WHERE id = ? AND user_id = ?
        ''', (listing_id, user_id))

        listing = cursor.fetchone()
        if not listing:
            conn.close()
            return jsonify({'error': 'Listing not found or unauthorized'}), 404

        # Update fields
        update_fields = []
        params = []

        allowed_fields = ['title', 'description', 'quantity_kg', 'asking_price',
                         'location', 'condition', 'status', 'pickup_available',
                         'delivery_available']

        for field in allowed_fields:
            if field in data:
                update_fields.append(f'{field} = ?')
                params.append(data[field])

        if update_fields:
            update_fields.append('updated_at = ?')
            params.append(datetime.now().isoformat())
            params.append(listing_id)

            query = f'''
                UPDATE marketplace_listings
                SET {', '.join(update_fields)}
                WHERE id = ?
            '''

            cursor.execute(query, params)
            conn.commit()

        conn.close()

        return jsonify({'message': 'Listing updated successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@marketplace_bp.route('/listings/<listing_id>', methods=['DELETE'])
@jwt_required()
def delete_listing(listing_id):
    """Delete a listing"""
    try:
        user_id = get_jwt_identity()

        conn = get_db_connection()
        cursor = conn.cursor()

        # Verify ownership
        cursor.execute('''
            SELECT * FROM marketplace_listings
            WHERE id = ? AND user_id = ?
        ''', (listing_id, user_id))

        listing = cursor.fetchone()
        if not listing:
            conn.close()
            return jsonify({'error': 'Listing not found or unauthorized'}), 404

        # Check if there are active bookings
        cursor.execute('''
            SELECT COUNT(*) as count FROM marketplace_bookings
            WHERE listing_id = ? AND status IN ('pending', 'confirmed')
        ''', (listing_id,))

        active_bookings = cursor.fetchone()['count']
        if active_bookings > 0:
            conn.close()
            return jsonify({'error': 'Cannot delete listing with active bookings'}), 400

        # Soft delete by changing status
        cursor.execute('''
            UPDATE marketplace_listings
            SET status = 'deleted', updated_at = ?
            WHERE id = ?
        ''', (datetime.now().isoformat(), listing_id))

        conn.commit()
        conn.close()

        return jsonify({'message': 'Listing deleted successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@marketplace_bp.route('/bookings/<booking_id>/payment', methods=['POST'])
@jwt_required()
def process_booking_payment(booking_id):
    """Process payment for a marketplace booking"""
    try:
        user_id = get_jwt_identity()
        data = request.json

        conn = get_db_connection()
        cursor = conn.cursor()

        # Get booking details
        cursor.execute('''
            SELECT b.*, l.waste_type, l.waste_subtype
            FROM marketplace_bookings b
            JOIN marketplace_listings l ON b.listing_id = l.id
            WHERE b.id = ? AND b.buyer_id = ?
        ''', (booking_id, user_id))

        booking = cursor.fetchone()
        if not booking:
            conn.close()
            return jsonify({'error': 'Booking not found or unauthorized'}), 404

        booking_dict = dict(booking)

        # Create transaction record
        transaction_id = f"mkt_txn_{uuid.uuid4().hex[:12]}"
        payment_id = data.get('payment_id', f"pay_{uuid.uuid4().hex[:12]}")

        # Platform fee (e.g., 5% of transaction value)
        platform_fee = booking_dict['agreed_price'] * 0.05
        net_amount = booking_dict['agreed_price'] - platform_fee

        cursor.execute('''
            INSERT INTO marketplace_transactions
            (id, booking_id, buyer_id, seller_id, transaction_type, amount,
             platform_fee, net_amount, payment_method, payment_id, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            transaction_id,
            booking_id,
            booking_dict['buyer_id'],
            booking_dict['seller_id'],
            'purchase',
            booking_dict['agreed_price'],
            platform_fee,
            net_amount,
            data.get('payment_method', 'online'),
            payment_id,
            'pending'
        ))

        # Update booking payment status
        cursor.execute('''
            UPDATE marketplace_bookings
            SET payment_status = 'paid',
                payment_id = ?,
                transaction_id = ?,
                updated_at = ?
            WHERE id = ?
        ''', (payment_id, transaction_id, datetime.now().isoformat(), booking_id))

        conn.commit()
        conn.close()

        return jsonify({
            'message': 'Payment processed successfully',
            'transaction_id': transaction_id,
            'amount_paid': booking_dict['agreed_price'],
            'platform_fee': platform_fee,
            'seller_receives': net_amount
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@marketplace_bp.route('/transactions', methods=['GET'])
@jwt_required()
def get_transactions():
    """Get user's marketplace transactions"""
    try:
        user_id = get_jwt_identity()
        transaction_type = request.args.get('type')  # 'purchase' or 'sale'
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)

        conn = get_db_connection()
        cursor = conn.cursor()

        offset = (page - 1) * per_page

        query = '''
            SELECT t.*,
                   b.listing_id,
                   l.title as listing_title,
                   l.waste_type,
                   buyer.full_name as buyer_name,
                   seller.full_name as seller_name
            FROM marketplace_transactions t
            JOIN marketplace_bookings b ON t.booking_id = b.id
            JOIN marketplace_listings l ON b.listing_id = l.id
            JOIN users buyer ON t.buyer_id = buyer.id
            JOIN users seller ON t.seller_id = seller.id
            WHERE (t.buyer_id = ? OR t.seller_id = ?)
        '''
        params = [user_id, user_id]

        if transaction_type == 'purchase':
            query += ' AND t.buyer_id = ?'
            params.append(user_id)
        elif transaction_type == 'sale':
            query += ' AND t.seller_id = ?'
            params.append(user_id)

        query += ' ORDER BY t.created_at DESC LIMIT ? OFFSET ?'
        params.extend([per_page, offset])

        cursor.execute(query, params)
        transactions = [dict(row) for row in cursor.fetchall()]

        # Get total count
        count_query = '''
            SELECT COUNT(*) as total
            FROM marketplace_transactions
            WHERE (buyer_id = ? OR seller_id = ?)
        '''
        count_params = [user_id, user_id]

        if transaction_type == 'purchase':
            count_query += ' AND buyer_id = ?'
            count_params.append(user_id)
        elif transaction_type == 'sale':
            count_query += ' AND seller_id = ?'
            count_params.append(user_id)

        cursor.execute(count_query, count_params)
        total = cursor.fetchone()['total']

        conn.close()

        return jsonify({
            'transactions': transactions,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
