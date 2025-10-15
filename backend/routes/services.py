from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from datetime import datetime, timedelta
import uuid

from middleware.auth import AuthMiddleware
from utils.validators import ServiceProviderSchema, validate_json_request
from models.demo_data import demo_data

# Create blueprint
services_bp = Blueprint('services', __name__, url_prefix='/api/services')

@services_bp.route('/register', methods=['POST'])
@AuthMiddleware.jwt_required
@validate_json_request(ServiceProviderSchema)
def register_service_provider():
    """Register a new service provider"""
    try:
        current_user_id = get_jwt_identity()
        provider_data = request.validated_data

        # Generate provider ID
        provider_id = f"sp_{uuid.uuid4().hex[:8]}"

        new_provider = {
            'id': provider_id,
            'user_id': current_user_id,
            'name': provider_data['business_name'],
            'type': provider_data['business_type'],
            'speciality': provider_data['specialities'],
            'license_number': provider_data['license_number'],
            'location': {
                'address': provider_data['address'],
                'city': provider_data['city'],
                'state': provider_data['state'],
                'pincode': provider_data['pincode'],
                'lat': None,  # Would be geocoded in real implementation
                'lng': None
            },
            'contact': {
                'email': provider_data['contact_email'],
                'phone': provider_data['contact_phone']
            },
            'operating_hours': provider_data['operating_hours'],
            'capacity': provider_data['capacity_per_day'],
            'website_url': provider_data.get('website_url'),
            'description': provider_data.get('description', ''),
            'rating': 0.0,
            'total_reviews': 0,
            'verified': False,
            'approval_status': 'pending',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'documents': [],
            'service_areas': [],
            'pricing': {},
            'availability': {
                'monday': True,
                'tuesday': True,
                'wednesday': True,
                'thursday': True,
                'friday': True,
                'saturday': True,
                'sunday': False
            },
            'stats': {
                'total_bookings': 0,
                'completed_bookings': 0,
                'average_response_time': 0,
                'success_rate': 100
            }
        }

        # Add to demo data
        demo_data.service_providers.append(new_provider)

        return jsonify({
            'success': True,
            'message': 'Service provider registration submitted successfully',
            'provider': new_provider,
            'next_steps': [
                'Upload required documents for verification',
                'Wait for admin approval',
                'Complete profile setup',
                'Start receiving bookings'
            ]
        }), 201

    except Exception as e:
        return jsonify({
            'error': 'Registration failed',
            'message': str(e)
        }), 500

@services_bp.route('/my-profile', methods=['GET'])
@AuthMiddleware.service_provider_required
def get_my_provider_profile():
    """Get current user's service provider profile"""
    try:
        current_user_id = get_jwt_identity()

        # Find provider profile
        provider = next(
            (sp for sp in demo_data.service_providers if sp.get('user_id') == current_user_id),
            None
        )

        if not provider:
            return jsonify({
                'error': 'Provider profile not found',
                'message': 'No service provider profile associated with this account'
            }), 404

        # Add recent bookings
        recent_bookings = [
            b for b in demo_data.bookings
            if b.get('service_provider_id') == provider['id']
        ][-10:]  # Last 10 bookings

        provider_with_bookings = {
            **provider,
            'recent_bookings': recent_bookings,
            'pending_bookings': len([b for b in recent_bookings if b.get('status') == 'scheduled']),
            'earnings_this_month': sum(b.get('actual_cost', 0) for b in recent_bookings if b.get('status') == 'completed')
        }

        return jsonify({
            'success': True,
            'provider': provider_with_bookings
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve profile',
            'message': str(e)
        }), 500

@services_bp.route('/my-profile', methods=['PUT'])
@AuthMiddleware.service_provider_required
def update_my_provider_profile():
    """Update current user's service provider profile"""
    try:
        current_user_id = get_jwt_identity()
        update_data = request.get_json()

        # Find provider
        provider = next(
            (sp for sp in demo_data.service_providers if sp.get('user_id') == current_user_id),
            None
        )

        if not provider:
            return jsonify({
                'error': 'Provider profile not found'
            }), 404

        # Update allowed fields
        updatable_fields = [
            'description', 'operating_hours', 'capacity', 'website_url',
            'availability', 'pricing', 'service_areas'
        ]

        for field in updatable_fields:
            if field in update_data:
                provider[field] = update_data[field]

        # Update contact information
        if 'contact' in update_data:
            provider['contact'].update(update_data['contact'])

        # Update location information
        if 'location' in update_data:
            provider['location'].update(update_data['location'])

        provider['updated_at'] = datetime.now().isoformat()

        return jsonify({
            'success': True,
            'message': 'Profile updated successfully',
            'provider': provider
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Profile update failed',
            'message': str(e)
        }), 500

@services_bp.route('/<provider_id>', methods=['GET'])
def get_service_provider_details(provider_id):
    """Get detailed information about a specific service provider"""
    try:
        # Find provider
        provider = next(
            (sp for sp in demo_data.service_providers if sp['id'] == provider_id),
            None
        )

        if not provider:
            return jsonify({
                'error': 'Service provider not found'
            }), 404

        # Get reviews for this provider
        provider_bookings = [
            b for b in demo_data.bookings
            if b.get('service_provider_id') == provider_id and b.get('user_rating')
        ]

        reviews = [
            {
                'booking_id': b['id'],
                'rating': b['user_rating']['overall_rating'],
                'title': b['user_rating']['title'],
                'comment': b['user_rating']['comment'],
                'rated_at': b['user_rating']['rated_at'],
                'service_details': {
                    'waste_type': b['waste_type'],
                    'quantity': b['quantity']
                }
            }
            for b in provider_bookings
        ]

        # Calculate statistics
        total_bookings = len([b for b in demo_data.bookings if b.get('service_provider_id') == provider_id])
        completed_bookings = len([b for b in demo_data.bookings if b.get('service_provider_id') == provider_id and b.get('status') == 'completed'])

        enhanced_provider = {
            **provider,
            'reviews': reviews,
            'total_reviews': len(reviews),
            'stats': {
                'total_bookings': total_bookings,
                'completed_bookings': completed_bookings,
                'success_rate': round((completed_bookings / max(total_bookings, 1)) * 100, 1),
                'average_rating': round(sum(r['rating'] for r in reviews) / max(len(reviews), 1), 1) if reviews else 0
            },
            'availability_today': True,  # Simulate availability
            'next_available_slot': (datetime.now() + timedelta(hours=2)).isoformat(),
            'pricing_info': {
                'base_rate': '₹50 per pickup',
                'per_kg_rate': '₹5 per kg',
                'minimum_charge': '₹100'
            }
        }

        return jsonify({
            'success': True,
            'provider': enhanced_provider
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve provider details',
            'message': str(e)
        }), 500

@services_bp.route('/<provider_id>/reviews', methods=['GET'])
def get_provider_reviews(provider_id):
    """Get reviews for a specific service provider"""
    try:
        # Find provider to ensure it exists
        provider = next(
            (sp for sp in demo_data.service_providers if sp['id'] == provider_id),
            None
        )

        if not provider:
            return jsonify({
                'error': 'Service provider not found'
            }), 404

        # Get reviews
        provider_bookings = [
            b for b in demo_data.bookings
            if b.get('service_provider_id') == provider_id and b.get('user_rating')
        ]

        # Query parameters
        limit = request.args.get('limit', 10, type=int)
        offset = request.args.get('offset', 0, type=int)
        rating_filter = request.args.get('rating', type=int)

        reviews = []
        for b in provider_bookings:
            rating_data = b['user_rating']
            if rating_filter and rating_data['overall_rating'] != rating_filter:
                continue

            reviews.append({
                'id': f"review_{b['id']}",
                'booking_id': b['id'],
                'overall_rating': rating_data['overall_rating'],
                'title': rating_data['title'],
                'comment': rating_data['comment'],
                'service_quality': rating_data.get('service_quality'),
                'punctuality': rating_data.get('punctuality'),
                'cleanliness': rating_data.get('cleanliness'),
                'communication': rating_data.get('communication'),
                'rated_at': rating_data['rated_at'],
                'service_details': {
                    'waste_type': b['waste_type'],
                    'quantity': b['quantity'],
                    'booking_date': b['created_at']
                },
                'verified_booking': True
            })

        # Sort by date (newest first)
        reviews.sort(key=lambda x: x['rated_at'], reverse=True)

        # Apply pagination
        total_reviews = len(reviews)
        paginated_reviews = reviews[offset:offset + limit]

        # Calculate rating distribution
        rating_distribution = {str(i): 0 for i in range(1, 6)}
        for review in reviews:
            rating_distribution[str(review['overall_rating'])] += 1

        return jsonify({
            'success': True,
            'reviews': paginated_reviews,
            'pagination': {
                'total': total_reviews,
                'limit': limit,
                'offset': offset,
                'has_more': offset + limit < total_reviews
            },
            'rating_distribution': rating_distribution,
            'average_rating': round(sum(r['overall_rating'] for r in reviews) / max(len(reviews), 1), 1) if reviews else 0
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve reviews',
            'message': str(e)
        }), 500

@services_bp.route('/search', methods=['GET'])
def search_service_providers():
    """Search service providers with filters"""
    try:
        # Query parameters
        waste_type = request.args.get('waste_type')
        city = request.args.get('city')
        service_type = request.args.get('service_type')  # NGO, Private, etc.
        min_rating = request.args.get('min_rating', type=float)
        lat = request.args.get('lat', type=float)
        lng = request.args.get('lng', type=float)
        radius = request.args.get('radius', 10, type=int)  # km
        sort_by = request.args.get('sort_by', 'rating')  # rating, distance, price
        limit = request.args.get('limit', 20, type=int)
        offset = request.args.get('offset', 0, type=int)

        # Start with all verified providers
        providers = [sp for sp in demo_data.service_providers if sp.get('verified', False)]

        # Apply filters
        if waste_type:
            providers = [sp for sp in providers if waste_type.lower() in [s.lower() for s in sp.get('speciality', [])]]

        if city:
            providers = [sp for sp in providers if sp.get('location', {}).get('city', '').lower() == city.lower()]

        if service_type:
            providers = [sp for sp in providers if sp.get('type', '').lower() == service_type.lower()]

        if min_rating:
            providers = [sp for sp in providers if sp.get('rating', 0) >= min_rating]

        # Simulate distance calculation if coordinates provided
        if lat and lng:
            import random
            for provider in providers:
                provider['distance'] = round(random.uniform(0.5, radius), 1)
                provider['estimated_time'] = f"{random.randint(15, 60)} min"

            # Filter by radius
            providers = [sp for sp in providers if sp.get('distance', 0) <= radius]

        # Sort providers
        if sort_by == 'rating':
            providers.sort(key=lambda x: x.get('rating', 0), reverse=True)
        elif sort_by == 'distance' and lat and lng:
            providers.sort(key=lambda x: x.get('distance', float('inf')))
        elif sort_by == 'price':
            # Sort by estimated cost (simulated)
            providers.sort(key=lambda x: hash(x['id']) % 100)  # Simulate price sorting

        # Apply pagination
        total_providers = len(providers)
        paginated_providers = providers[offset:offset + limit]

        # Add available time slots for each provider
        for provider in paginated_providers:
            provider['available_slots'] = [
                'Today 2:00 PM - 4:00 PM',
                'Tomorrow 10:00 AM - 12:00 PM',
                'Tomorrow 3:00 PM - 5:00 PM'
            ]

        return jsonify({
            'success': True,
            'providers': paginated_providers,
            'pagination': {
                'total': total_providers,
                'limit': limit,
                'offset': offset,
                'has_more': offset + limit < total_providers
            },
            'filters_applied': {
                'waste_type': waste_type,
                'city': city,
                'service_type': service_type,
                'min_rating': min_rating,
                'location': {'lat': lat, 'lng': lng, 'radius': radius} if lat and lng else None
            }
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Search failed',
            'message': str(e)
        }), 500

@services_bp.route('/my-bookings', methods=['GET'])
@AuthMiddleware.service_provider_required
def get_provider_bookings():
    """Get bookings assigned to current service provider"""
    try:
        current_user_id = get_jwt_identity()

        # Find provider
        provider = next(
            (sp for sp in demo_data.service_providers if sp.get('user_id') == current_user_id),
            None
        )

        if not provider:
            return jsonify({
                'error': 'Provider profile not found'
            }), 404

        # Query parameters
        status = request.args.get('status')
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        limit = request.args.get('limit', 20, type=int)
        offset = request.args.get('offset', 0, type=int)

        # Get provider's bookings
        provider_bookings = [
            b for b in demo_data.bookings
            if b.get('service_provider_id') == provider['id']
        ]

        # Apply filters
        if status:
            provider_bookings = [b for b in provider_bookings if b.get('status') == status]

        if date_from:
            provider_bookings = [b for b in provider_bookings if b.get('scheduled_date', '') >= date_from]

        if date_to:
            provider_bookings = [b for b in provider_bookings if b.get('scheduled_date', '') <= date_to]

        # Sort by scheduled date
        provider_bookings.sort(key=lambda x: x.get('scheduled_date', ''), reverse=True)

        # Apply pagination
        total_bookings = len(provider_bookings)
        paginated_bookings = provider_bookings[offset:offset + limit]

        # Add customer contact info for confirmed bookings
        for booking in paginated_bookings:
            if booking.get('status') in ['confirmed', 'in_progress']:
                booking['customer_contact'] = {
                    'name': booking.get('contact_person', 'Customer'),
                    'phone': booking.get('contact_phone', 'N/A')
                }

        return jsonify({
            'success': True,
            'bookings': paginated_bookings,
            'pagination': {
                'total': total_bookings,
                'limit': limit,
                'offset': offset,
                'has_more': offset + limit < total_bookings
            },
            'summary': {
                'pending': len([b for b in provider_bookings if b.get('status') == 'scheduled']),
                'in_progress': len([b for b in provider_bookings if b.get('status') == 'in_progress']),
                'completed': len([b for b in provider_bookings if b.get('status') == 'completed']),
                'total_earnings': sum(b.get('actual_cost', 0) for b in provider_bookings if b.get('status') == 'completed')
            }
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve bookings',
            'message': str(e)
        }), 500

@services_bp.route('/booking/<booking_id>/accept', methods=['POST'])
@AuthMiddleware.service_provider_required
def accept_booking(booking_id):
    """Accept a booking request"""
    try:
        current_user_id = get_jwt_identity()

        # Find provider
        provider = next(
            (sp for sp in demo_data.service_providers if sp.get('user_id') == current_user_id),
            None
        )

        if not provider:
            return jsonify({'error': 'Provider profile not found'}), 404

        # Find booking
        booking = next((b for b in demo_data.bookings if b['id'] == booking_id), None)

        if not booking:
            return jsonify({'error': 'Booking not found'}), 404

        # Check if this booking belongs to current provider
        if booking.get('service_provider_id') != provider['id']:
            return jsonify({'error': 'Access denied'}), 403

        # Update booking status
        booking['status'] = 'confirmed'
        booking['confirmed_at'] = datetime.now().isoformat()
        booking['updated_at'] = datetime.now().isoformat()

        # Update tracking steps
        if 'tracking_steps' in booking:
            for step in booking['tracking_steps']:
                if step['step'] == 'Pickup Scheduled' and step['status'] == 'pending':
                    step['status'] = 'completed'
                    step['timestamp'] = datetime.now().isoformat()
                    break

        return jsonify({
            'success': True,
            'message': 'Booking accepted successfully',
            'booking': booking
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to accept booking',
            'message': str(e)
        }), 500

@services_bp.route('/booking/<booking_id>/complete', methods=['POST'])
@AuthMiddleware.service_provider_required
def complete_booking(booking_id):
    """Mark a booking as completed"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json() or {}

        # Find provider
        provider = next(
            (sp for sp in demo_data.service_providers if sp.get('user_id') == current_user_id),
            None
        )

        if not provider:
            return jsonify({'error': 'Provider profile not found'}), 404

        # Find booking
        booking = next((b for b in demo_data.bookings if b['id'] == booking_id), None)

        if not booking:
            return jsonify({'error': 'Booking not found'}), 404

        # Check ownership
        if booking.get('service_provider_id') != provider['id']:
            return jsonify({'error': 'Access denied'}), 403

        # Update booking
        booking['status'] = 'completed'
        booking['completed_at'] = datetime.now().isoformat()
        booking['updated_at'] = datetime.now().isoformat()
        booking['actual_cost'] = data.get('actual_cost', booking.get('estimated_cost'))
        booking['completion_notes'] = data.get('completion_notes', '')
        booking['waste_processed'] = data.get('waste_processed', booking.get('quantity'))

        # Update all tracking steps to completed
        if 'tracking_steps' in booking:
            for step in booking['tracking_steps']:
                if step['status'] != 'completed':
                    step['status'] = 'completed'
                    step['timestamp'] = datetime.now().isoformat()

        # Update provider stats
        provider['stats']['completed_bookings'] += 1
        provider['stats']['total_bookings'] += 1

        return jsonify({
            'success': True,
            'message': 'Booking completed successfully',
            'booking': booking,
            'earnings': booking['actual_cost']
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to complete booking',
            'message': str(e)
        }), 500