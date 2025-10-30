from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from datetime import datetime, timedelta
import uuid
import random

from middleware.auth import AuthMiddleware
from utils.validators import BookingCreateSchema, ReviewSchema, validate_json_request
from models.demo_data import demo_data

# Create blueprint
bookings_bp = Blueprint('bookings', __name__, url_prefix='/api/bookings')

@bookings_bp.route('/create', methods=['POST'])
@AuthMiddleware.jwt_required
@validate_json_request(BookingCreateSchema)
def create_booking():
    """Create a new booking"""
    try:
        current_user_id = get_jwt_identity()
        booking_data = request.validated_data

        # Add user information
        booking_data['user_id'] = current_user_id

        # Generate booking ID
        booking_id = f"book_{len(demo_data.bookings)+1:03d}"

        # Calculate estimated cost using the proper pricing utility
        # Import at the top of this function to avoid circular imports
        from utils.pricing import WastePricing

        # Extract quantity in kg
        quantity_str = booking_data['quantity'].split()[0]
        quantity_kg = float(quantity_str) if quantity_str.replace('.', '', 1).isdigit() else 1.0

        # Calculate net transaction (waste value - collection cost)
        # Users should GET PAID for valuable waste, not charged
        pricing = WastePricing.calculate_net_transaction(
            waste_type=booking_data['waste_type'],
            quantity_kg=quantity_kg,
            subtype='mixed',  # Default to mixed, can be enhanced later
            distance_km=0  # Can be calculated based on user location
        )

        # Negative net_amount means user pays, positive means user earns
        estimated_cost = pricing['net_amount']

        new_booking = {
            'id': booking_id,
            'user_id': current_user_id,
            'service_provider_id': booking_data['service_provider_id'],
            'waste_type': booking_data['waste_type'],
            'quantity': booking_data['quantity'],
            'pickup_address': booking_data['pickup_address'],
            'scheduled_date': booking_data['scheduled_date'].isoformat(),
            'scheduled_time_slot': booking_data['scheduled_time_slot'],
            'special_instructions': booking_data.get('special_instructions', ''),
            'contact_person': booking_data.get('contact_person', ''),
            'contact_phone': booking_data.get('contact_phone', ''),
            'status': 'scheduled',
            'estimated_cost': round(estimated_cost, 2),
            'actual_cost': None,
            'payment_status': 'pending',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'tracking_steps': [
                {
                    'step': 'Booking Confirmed',
                    'status': 'completed',
                    'timestamp': datetime.now().isoformat(),
                    'description': 'Your booking has been confirmed and assigned a tracking ID'
                },
                {
                    'step': 'Service Provider Notified',
                    'status': 'completed',
                    'timestamp': (datetime.now() + timedelta(minutes=2)).isoformat(),
                    'description': 'Service provider has been notified of your booking'
                },
                {
                    'step': 'Pickup Scheduled',
                    'status': 'pending',
                    'timestamp': None,
                    'description': 'Pickup will be scheduled based on your preferred time slot'
                },
                {
                    'step': 'On Route',
                    'status': 'pending',
                    'timestamp': None,
                    'description': 'Service provider is on the way to pickup location'
                },
                {
                    'step': 'Waste Collected',
                    'status': 'pending',
                    'timestamp': None,
                    'description': 'Waste has been collected from your location'
                },
                {
                    'step': 'Processing Complete',
                    'status': 'pending',
                    'timestamp': None,
                    'description': 'Waste has been processed and recycled'
                }
            ]
        }

        # Add to demo data
        demo_data.bookings.append(new_booking)

        return jsonify({
            'success': True,
            'message': 'Booking created successfully',
            'booking': new_booking,
            'next_steps': [
                'Track your booking status in real-time',
                'Prepare waste for pickup at scheduled time',
                'Keep your phone available for service provider contact'
            ]
        }), 201

    except Exception as e:
        return jsonify({
            'error': 'Booking creation failed',
            'message': str(e)
        }), 500

@bookings_bp.route('/my-bookings', methods=['GET'])
@AuthMiddleware.jwt_required
def get_user_bookings():
    """Get current user's bookings"""
    try:
        current_user_id = get_jwt_identity()

        # Query parameters
        status = request.args.get('status')  # scheduled, in_progress, completed, cancelled
        limit = request.args.get('limit', 20, type=int)
        offset = request.args.get('offset', 0, type=int)

        # Filter bookings for current user
        user_bookings = [b for b in demo_data.bookings if b.get('user_id') == current_user_id]

        # Apply status filter
        if status:
            user_bookings = [b for b in user_bookings if b.get('status') == status]

        # Sort by creation date (newest first)
        user_bookings.sort(key=lambda x: x.get('created_at', ''), reverse=True)

        # Apply pagination
        total_bookings = len(user_bookings)
        paginated_bookings = user_bookings[offset:offset + limit]

        return jsonify({
            'success': True,
            'bookings': paginated_bookings,
            'pagination': {
                'total': total_bookings,
                'limit': limit,
                'offset': offset,
                'has_more': offset + limit < total_bookings
            }
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve bookings',
            'message': str(e)
        }), 500

@bookings_bp.route('/<booking_id>', methods=['GET'])
@AuthMiddleware.jwt_required
def get_booking_details(booking_id):
    """Get detailed information about a specific booking"""
    try:
        current_user_id = get_jwt_identity()

        # Find booking
        booking = next((b for b in demo_data.bookings if b['id'] == booking_id), None)

        if not booking:
            return jsonify({
                'error': 'Booking not found',
                'message': f'No booking found with ID {booking_id}'
            }), 404

        # Check if user owns this booking (or is admin)
        if booking.get('user_id') != current_user_id:
            return jsonify({
                'error': 'Access denied',
                'message': 'You can only view your own bookings'
            }), 403

        # Get service provider details
        service_provider = next(
            (sp for sp in demo_data.service_providers if sp['id'] == booking['service_provider_id']),
            None
        )

        # Simulate real-time tracking updates based on booking age
        booking_age = datetime.now() - datetime.fromisoformat(booking['created_at'])

        if booking_age.total_seconds() > 3600:  # More than 1 hour old
            # Update tracking steps
            for i, step in enumerate(booking['tracking_steps']):
                if i < 3 and step['status'] == 'pending':
                    step['status'] = 'completed'
                    step['timestamp'] = (datetime.now() - timedelta(minutes=30*i)).isoformat()

        enhanced_booking = {
            **booking,
            'service_provider': service_provider,
            'estimated_arrival': booking['scheduled_date'],
            'can_cancel': booking['status'] in ['scheduled', 'confirmed'],
            'can_reschedule': booking['status'] in ['scheduled', 'confirmed'],
            'can_rate': booking['status'] == 'completed' and not booking.get('user_rating')
        }

        return jsonify({
            'success': True,
            'booking': enhanced_booking
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve booking details',
            'message': str(e)
        }), 500

@bookings_bp.route('/<booking_id>/cancel', methods=['POST'])
@AuthMiddleware.jwt_required
def cancel_booking(booking_id):
    """Cancel a booking"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json() or {}
        cancellation_reason = data.get('reason', 'User requested cancellation')

        # Find booking
        booking = next((b for b in demo_data.bookings if b['id'] == booking_id), None)

        if not booking:
            return jsonify({
                'error': 'Booking not found',
                'message': f'No booking found with ID {booking_id}'
            }), 404

        # Check ownership
        if booking.get('user_id') != current_user_id:
            return jsonify({
                'error': 'Access denied',
                'message': 'You can only cancel your own bookings'
            }), 403

        # Check if cancellation is allowed
        if booking['status'] not in ['scheduled', 'confirmed']:
            return jsonify({
                'error': 'Cancellation not allowed',
                'message': f'Cannot cancel booking with status: {booking["status"]}'
            }), 400

        # Update booking status
        booking['status'] = 'cancelled'
        booking['cancelled_at'] = datetime.now().isoformat()
        booking['cancellation_reason'] = cancellation_reason
        booking['updated_at'] = datetime.now().isoformat()

        # Calculate cancellation fee (if applicable)
        scheduled_time = datetime.fromisoformat(booking['scheduled_date'])
        hours_until_pickup = (scheduled_time - datetime.now()).total_seconds() / 3600

        cancellation_fee = 0
        if hours_until_pickup < 24:
            cancellation_fee = booking['estimated_cost'] * 0.1  # 10% fee for late cancellation

        booking['cancellation_fee'] = round(cancellation_fee, 2)

        return jsonify({
            'success': True,
            'message': 'Booking cancelled successfully',
            'booking': booking,
            'cancellation_fee': cancellation_fee,
            'refund_amount': booking['estimated_cost'] - cancellation_fee if booking.get('payment_status') == 'paid' else 0
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Cancellation failed',
            'message': str(e)
        }), 500

@bookings_bp.route('/<booking_id>/reschedule', methods=['POST'])
@AuthMiddleware.jwt_required
def reschedule_booking(booking_id):
    """Reschedule a booking"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()

        new_date = data.get('new_scheduled_date')
        new_time_slot = data.get('new_time_slot')

        if not new_date or not new_time_slot:
            return jsonify({
                'error': 'Missing required fields',
                'message': 'new_scheduled_date and new_time_slot are required'
            }), 400

        # Find booking
        booking = next((b for b in demo_data.bookings if b['id'] == booking_id), None)

        if not booking:
            return jsonify({
                'error': 'Booking not found'
            }), 404

        # Check ownership
        if booking.get('user_id') != current_user_id:
            return jsonify({
                'error': 'Access denied'
            }), 403

        # Check if rescheduling is allowed
        if booking['status'] not in ['scheduled', 'confirmed']:
            return jsonify({
                'error': 'Rescheduling not allowed',
                'message': f'Cannot reschedule booking with status: {booking["status"]}'
            }), 400

        # Validate new date is in future
        try:
            new_datetime = datetime.fromisoformat(new_date)
            if new_datetime <= datetime.now():
                return jsonify({
                    'error': 'Invalid date',
                    'message': 'New scheduled date must be in the future'
                }), 400
        except ValueError:
            return jsonify({
                'error': 'Invalid date format',
                'message': 'Please provide date in ISO format'
            }), 400

        # Update booking
        old_date = booking['scheduled_date']
        old_time_slot = booking['scheduled_time_slot']

        booking['scheduled_date'] = new_date
        booking['scheduled_time_slot'] = new_time_slot
        booking['updated_at'] = datetime.now().isoformat()
        booking['rescheduled'] = True
        booking['reschedule_history'] = booking.get('reschedule_history', [])
        booking['reschedule_history'].append({
            'old_date': old_date,
            'old_time_slot': old_time_slot,
            'new_date': new_date,
            'new_time_slot': new_time_slot,
            'rescheduled_at': datetime.now().isoformat()
        })

        return jsonify({
            'success': True,
            'message': 'Booking rescheduled successfully',
            'booking': booking
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Rescheduling failed',
            'message': str(e)
        }), 500

@bookings_bp.route('/<booking_id>/rate', methods=['POST'])
@AuthMiddleware.jwt_required
@validate_json_request(ReviewSchema)
def rate_booking(booking_id):
    """Rate and review a completed booking"""
    try:
        current_user_id = get_jwt_identity()
        review_data = request.validated_data

        # Find booking
        booking = next((b for b in demo_data.bookings if b['id'] == booking_id), None)

        if not booking:
            return jsonify({
                'error': 'Booking not found'
            }), 404

        # Check ownership
        if booking.get('user_id') != current_user_id:
            return jsonify({
                'error': 'Access denied'
            }), 403

        # Check if booking is completed
        if booking['status'] != 'completed':
            return jsonify({
                'error': 'Rating not allowed',
                'message': 'Can only rate completed bookings'
            }), 400

        # Check if already rated
        if booking.get('user_rating'):
            return jsonify({
                'error': 'Already rated',
                'message': 'This booking has already been rated'
            }), 400

        # Add rating to booking
        booking['user_rating'] = {
            'overall_rating': review_data['rating'],
            'title': review_data['title'],
            'comment': review_data['comment'],
            'service_quality': review_data.get('service_quality'),
            'punctuality': review_data.get('punctuality'),
            'cleanliness': review_data.get('cleanliness'),
            'communication': review_data.get('communication'),
            'rated_at': datetime.now().isoformat()
        }

        booking['updated_at'] = datetime.now().isoformat()

        # Update service provider rating (simulate)
        service_provider = next(
            (sp for sp in demo_data.service_providers if sp['id'] == booking['service_provider_id']),
            None
        )

        if service_provider:
            # Simple rating update simulation
            current_rating = service_provider.get('rating', 4.5)
            new_rating = (current_rating + review_data['rating']) / 2
            service_provider['rating'] = round(new_rating, 1)

        return jsonify({
            'success': True,
            'message': 'Rating submitted successfully',
            'booking': booking,
            'points_earned': 50  # Reward points for rating
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Rating submission failed',
            'message': str(e)
        }), 500

@bookings_bp.route('/<booking_id>/track', methods=['GET'])
@AuthMiddleware.jwt_required
def track_booking(booking_id):
    """Get real-time tracking information for a booking"""
    try:
        current_user_id = get_jwt_identity()

        # Find booking
        booking = next((b for b in demo_data.bookings if b['id'] == booking_id), None)

        if not booking:
            return jsonify({
                'error': 'Booking not found'
            }), 404

        # Check ownership
        if booking.get('user_id') != current_user_id:
            return jsonify({
                'error': 'Access denied'
            }), 403

        # Simulate dynamic tracking updates
        tracking_info = {
            'booking_id': booking_id,
            'current_status': booking['status'],
            'tracking_steps': booking.get('tracking_steps', []),
            'estimated_arrival': booking.get('scheduled_date'),
            'live_location': None,  # Would be actual GPS coordinates in real implementation
            'service_provider_contact': None,
            'last_updated': datetime.now().isoformat()
        }

        # Add live updates based on booking status
        if booking['status'] == 'in_progress':
            tracking_info['live_location'] = {
                'lat': 19.0760 + random.uniform(-0.01, 0.01),
                'lng': 72.8777 + random.uniform(-0.01, 0.01),
                'heading': random.randint(0, 360),
                'speed': random.randint(20, 60)
            }
            tracking_info['estimated_arrival'] = (datetime.now() + timedelta(minutes=random.randint(15, 45))).isoformat()

        # Get service provider contact if pickup is scheduled
        if booking['status'] in ['confirmed', 'in_progress']:
            service_provider = next(
                (sp for sp in demo_data.service_providers if sp['id'] == booking['service_provider_id']),
                None
            )
            if service_provider:
                tracking_info['service_provider_contact'] = {
                    'name': service_provider['name'],
                    'phone': service_provider['contact']['phone']
                }

        return jsonify({
            'success': True,
            'tracking': tracking_info
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Tracking failed',
            'message': str(e)
        }), 500

@bookings_bp.route('/bulk', methods=['POST'])
@AuthMiddleware.jwt_required
def create_bulk_booking():
    """Create multiple bookings at once (for communities/organizations)"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()

        bookings_data = data.get('bookings', [])
        community_id = data.get('community_id')

        if not bookings_data:
            return jsonify({
                'error': 'No bookings provided',
                'message': 'Please provide at least one booking'
            }), 400

        created_bookings = []
        failed_bookings = []

        for idx, booking_data in enumerate(bookings_data):
            try:
                # Validate each booking
                schema = BookingCreateSchema()
                validated_data = schema.load(booking_data)

                # Create booking
                booking_id = f"bulk_{uuid.uuid4().hex[:8]}"
                new_booking = {
                    'id': booking_id,
                    'user_id': current_user_id,
                    'community_id': community_id,
                    'bulk_booking': True,
                    'bulk_index': idx + 1,
                    **validated_data,
                    'status': 'scheduled',
                    'created_at': datetime.now().isoformat()
                }

                demo_data.bookings.append(new_booking)
                created_bookings.append(new_booking)

            except Exception as e:
                failed_bookings.append({
                    'index': idx + 1,
                    'data': booking_data,
                    'error': str(e)
                })

        return jsonify({
            'success': True,
            'message': f'Bulk booking created: {len(created_bookings)} successful, {len(failed_bookings)} failed',
            'created_bookings': created_bookings,
            'failed_bookings': failed_bookings,
            'summary': {
                'total_requested': len(bookings_data),
                'successful': len(created_bookings),
                'failed': len(failed_bookings)
            }
        }), 201 if created_bookings else 400

    except Exception as e:
        return jsonify({
            'error': 'Bulk booking failed',
            'message': str(e)
        }), 500