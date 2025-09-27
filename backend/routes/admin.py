from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from datetime import datetime, timedelta
import uuid

from middleware.auth import AuthMiddleware
from models.demo_data import demo_data
from models.user_manager import UserManager

# Create blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

# Initialize user manager
user_manager = UserManager()

@admin_bp.route('/dashboard', methods=['GET'])
@AuthMiddleware.admin_required
def get_admin_dashboard():
    """Get admin dashboard overview"""
    try:
        # Calculate date ranges
        now = datetime.now()
        week_start = now - timedelta(days=7)
        month_start = now - timedelta(days=30)

        # User statistics
        if not hasattr(demo_data, 'user_points'):
            demo_data.user_points = {}

        total_users = len(demo_data.user_points)
        active_users_week = len(set(
            b.get('user_id') for b in demo_data.bookings
            if b.get('user_id') and datetime.fromisoformat(b.get('created_at', now.isoformat())) >= week_start
        ))

        # Booking statistics
        total_bookings = len(demo_data.bookings)
        pending_bookings = len([b for b in demo_data.bookings if b.get('status') == 'scheduled'])
        completed_bookings = len([b for b in demo_data.bookings if b.get('status') == 'completed'])

        # Service provider statistics
        total_providers = len(demo_data.service_providers)
        pending_approvals = len([sp for sp in demo_data.service_providers if sp.get('approval_status') == 'pending'])
        verified_providers = len([sp for sp in demo_data.service_providers if sp.get('verified', False)])

        # Classification statistics
        total_classifications = len(demo_data.classifications)
        week_classifications = len([
            c for c in demo_data.classifications
            if datetime.fromisoformat(c.get('created_at', now.isoformat())) >= week_start
        ])

        # Financial statistics (mock)
        total_revenue = sum(b.get('actual_cost', 0) for b in demo_data.bookings if b.get('status') == 'completed')
        month_revenue = sum(
            b.get('actual_cost', 0) for b in demo_data.bookings
            if b.get('status') == 'completed' and
            datetime.fromisoformat(b.get('created_at', now.isoformat())) >= month_start
        )

        # Generate growth metrics
        growth_metrics = {
            'user_growth': 12.5,  # Mock percentage
            'booking_growth': 8.3,
            'revenue_growth': 15.7,
            'provider_growth': 6.2
        }

        # Recent activities
        recent_activities = []

        # Add recent user registrations
        recent_activities.extend([
            {
                'type': 'user_registration',
                'description': f'New user registered: User {str(uuid.uuid4())[:8]}',
                'timestamp': (now - timedelta(hours=i)).isoformat(),
                'severity': 'info'
            } for i in range(1, 4)
        ])

        # Add recent service provider applications
        recent_activities.extend([
            {
                'type': 'provider_application',
                'description': f'New service provider application: {["Green Clean Co", "Eco Solutions", "Waste Warriors"][i % 3]}',
                'timestamp': (now - timedelta(hours=i*2)).isoformat(),
                'severity': 'warning'
            } for i in range(1, 3)
        ])

        recent_activities.sort(key=lambda x: x['timestamp'], reverse=True)

        dashboard_data = {
            'overview': {
                'total_users': total_users,
                'active_users_week': active_users_week,
                'total_bookings': total_bookings,
                'pending_bookings': pending_bookings,
                'completed_bookings': completed_bookings,
                'total_providers': total_providers,
                'pending_approvals': pending_approvals,
                'verified_providers': verified_providers,
                'total_classifications': total_classifications,
                'week_classifications': week_classifications,
                'total_revenue': round(total_revenue, 2),
                'month_revenue': round(month_revenue, 2)
            },
            'growth_metrics': growth_metrics,
            'recent_activities': recent_activities[:10],
            'system_health': {
                'api_status': 'healthy',
                'database_status': 'healthy',
                'payment_gateway': 'healthy',
                'storage_usage': '45%',
                'cpu_usage': '23%',
                'memory_usage': '67%'
            },
            'alerts': [
                {
                    'type': 'warning',
                    'message': f'{pending_approvals} service providers awaiting approval',
                    'action_required': pending_approvals > 0
                },
                {
                    'type': 'info',
                    'message': f'{pending_bookings} bookings need attention',
                    'action_required': pending_bookings > 10
                }
            ]
        }

        return jsonify({
            'success': True,
            'dashboard': dashboard_data,
            'generated_at': now.isoformat()
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve dashboard data',
            'message': str(e)
        }), 500

@admin_bp.route('/users', methods=['GET'])
@AuthMiddleware.admin_required
def manage_users():
    """Get and manage users"""
    try:
        # Query parameters
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        search = request.args.get('search', '')
        role_filter = request.args.get('role')
        status_filter = request.args.get('status')

        # Mock user data (in real implementation, fetch from database)
        all_users = []
        if hasattr(demo_data, 'user_points'):
            for user_id in demo_data.user_points.keys():
                user_bookings = [b for b in demo_data.bookings if b.get('user_id') == user_id]
                user_classifications = [c for c in demo_data.classifications if user_id in c.get('filename', '')]

                all_users.append({
                    'id': user_id,
                    'email': f'user{user_id[:8]}@example.com',
                    'full_name': f'User {user_id[:8]}',
                    'role': 'user',
                    'status': 'active',
                    'created_at': (datetime.now() - timedelta(days=hash(user_id) % 365)).isoformat(),
                    'last_login': (datetime.now() - timedelta(days=hash(user_id) % 30)).isoformat(),
                    'total_bookings': len(user_bookings),
                    'total_classifications': len(user_classifications),
                    'total_points': demo_data.user_points.get(user_id, 0),
                    'verified': True
                })

        # Apply filters
        if search:
            all_users = [u for u in all_users if search.lower() in u['full_name'].lower() or search.lower() in u['email'].lower()]

        if role_filter:
            all_users = [u for u in all_users if u['role'] == role_filter]

        if status_filter:
            all_users = [u for u in all_users if u['status'] == status_filter]

        # Sort by creation date (newest first)
        all_users.sort(key=lambda x: x['created_at'], reverse=True)

        # Apply pagination
        total_users = len(all_users)
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        paginated_users = all_users[start_idx:end_idx]

        return jsonify({
            'success': True,
            'users': paginated_users,
            'pagination': {
                'current_page': page,
                'total_pages': (total_users + limit - 1) // limit,
                'total_users': total_users,
                'has_next': end_idx < total_users,
                'has_prev': page > 1
            },
            'filters': {
                'search': search,
                'role': role_filter,
                'status': status_filter
            }
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve users',
            'message': str(e)
        }), 500

@admin_bp.route('/users/<user_id>/status', methods=['PUT'])
@AuthMiddleware.admin_required
def update_user_status(user_id):
    """Update user status (activate/deactivate/suspend)"""
    try:
        data = request.get_json()
        new_status = data.get('status')
        reason = data.get('reason', 'Admin action')

        if new_status not in ['active', 'suspended', 'deactivated']:
            return jsonify({
                'error': 'Invalid status',
                'message': 'Status must be one of: active, suspended, deactivated'
            }), 400

        # Log admin action
        admin_user_id = get_jwt_identity()
        action_log = {
            'id': str(uuid.uuid4()),
            'admin_id': admin_user_id,
            'action': 'user_status_change',
            'target_user_id': user_id,
            'details': {
                'new_status': new_status,
                'reason': reason
            },
            'timestamp': datetime.now().isoformat()
        }

        if not hasattr(demo_data, 'admin_actions'):
            demo_data.admin_actions = []
        demo_data.admin_actions.append(action_log)

        return jsonify({
            'success': True,
            'message': f'User status updated to {new_status}',
            'user_id': user_id,
            'new_status': new_status,
            'action_id': action_log['id']
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to update user status',
            'message': str(e)
        }), 500

@admin_bp.route('/service-providers', methods=['GET'])
@AuthMiddleware.admin_required
def manage_service_providers():
    """Get and manage service providers"""
    try:
        # Query parameters
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        status_filter = request.args.get('status')  # pending, approved, rejected
        type_filter = request.args.get('type')

        # Get service providers
        providers = demo_data.service_providers.copy()

        # Apply filters
        if status_filter:
            providers = [sp for sp in providers if sp.get('approval_status') == status_filter]

        if type_filter:
            providers = [sp for sp in providers if sp.get('type') == type_filter]

        # Sort by creation date (newest first)
        providers.sort(key=lambda x: x.get('created_at', ''), reverse=True)

        # Apply pagination
        total_providers = len(providers)
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        paginated_providers = providers[start_idx:end_idx]

        # Add booking statistics for each provider
        for provider in paginated_providers:
            provider_bookings = [b for b in demo_data.bookings if b.get('service_provider_id') == provider['id']]
            provider['stats'] = {
                'total_bookings': len(provider_bookings),
                'completed_bookings': len([b for b in provider_bookings if b.get('status') == 'completed']),
                'average_rating': provider.get('rating', 0),
                'total_reviews': len([b for b in provider_bookings if b.get('user_rating')])
            }

        return jsonify({
            'success': True,
            'providers': paginated_providers,
            'pagination': {
                'current_page': page,
                'total_pages': (total_providers + limit - 1) // limit,
                'total_providers': total_providers,
                'has_next': end_idx < total_providers,
                'has_prev': page > 1
            },
            'summary': {
                'pending_approvals': len([sp for sp in demo_data.service_providers if sp.get('approval_status') == 'pending']),
                'approved_providers': len([sp for sp in demo_data.service_providers if sp.get('approval_status') == 'approved']),
                'total_providers': len(demo_data.service_providers)
            }
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve service providers',
            'message': str(e)
        }), 500

@admin_bp.route('/service-providers/<provider_id>/approve', methods=['POST'])
@AuthMiddleware.admin_required
def approve_service_provider(provider_id):
    """Approve or reject a service provider application"""
    try:
        data = request.get_json()
        action = data.get('action', 'approve')  # approve, reject
        notes = data.get('notes', '')

        if action not in ['approve', 'reject']:
            return jsonify({
                'error': 'Invalid action',
                'message': 'Action must be either approve or reject'
            }), 400

        # Find provider
        provider = next((sp for sp in demo_data.service_providers if sp['id'] == provider_id), None)

        if not provider:
            return jsonify({
                'error': 'Service provider not found',
                'message': f'No service provider found with ID {provider_id}'
            }), 404

        # Update provider status
        admin_user_id = get_jwt_identity()
        provider['approval_status'] = 'approved' if action == 'approve' else 'rejected'
        provider['verified'] = action == 'approve'
        provider['approved_by'] = admin_user_id
        provider['approved_at'] = datetime.now().isoformat()
        provider['approval_notes'] = notes

        # Log admin action
        action_log = {
            'id': str(uuid.uuid4()),
            'admin_id': admin_user_id,
            'action': f'provider_{action}',
            'target_provider_id': provider_id,
            'details': {
                'provider_name': provider['name'],
                'notes': notes
            },
            'timestamp': datetime.now().isoformat()
        }

        if not hasattr(demo_data, 'admin_actions'):
            demo_data.admin_actions = []
        demo_data.admin_actions.append(action_log)

        # Send notification to provider (mock)
        notification_message = f"Your service provider application has been {action}d."
        if notes:
            notification_message += f" Notes: {notes}"

        return jsonify({
            'success': True,
            'message': f'Service provider {action}d successfully',
            'provider_id': provider_id,
            'new_status': provider['approval_status'],
            'action_id': action_log['id']
        }), 200

    except Exception as e:
        return jsonify({
            'error': f'Failed to {action} service provider',
            'message': str(e)
        }), 500

@admin_bp.route('/bookings', methods=['GET'])
@AuthMiddleware.admin_required
def manage_bookings():
    """Get and manage all bookings"""
    try:
        # Query parameters
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        status_filter = request.args.get('status')
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')

        # Get all bookings
        bookings = demo_data.bookings.copy()

        # Apply filters
        if status_filter:
            bookings = [b for b in bookings if b.get('status') == status_filter]

        if date_from:
            bookings = [b for b in bookings if b.get('created_at', '') >= date_from]

        if date_to:
            bookings = [b for b in bookings if b.get('created_at', '') <= date_to]

        # Sort by creation date (newest first)
        bookings.sort(key=lambda x: x.get('created_at', ''), reverse=True)

        # Apply pagination
        total_bookings = len(bookings)
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        paginated_bookings = bookings[start_idx:end_idx]

        # Enhance booking data with user and provider info
        for booking in paginated_bookings:
            # Add user info (mock)
            if booking.get('user_id'):
                booking['user_info'] = {
                    'name': f'User {booking["user_id"][:8]}',
                    'email': f'user{booking["user_id"][:8]}@example.com'
                }

            # Add provider info
            if booking.get('service_provider_id'):
                provider = next((sp for sp in demo_data.service_providers if sp['id'] == booking['service_provider_id']), None)
                if provider:
                    booking['provider_info'] = {
                        'name': provider['name'],
                        'type': provider['type'],
                        'contact': provider['contact']
                    }

        return jsonify({
            'success': True,
            'bookings': paginated_bookings,
            'pagination': {
                'current_page': page,
                'total_pages': (total_bookings + limit - 1) // limit,
                'total_bookings': total_bookings,
                'has_next': end_idx < total_bookings,
                'has_prev': page > 1
            },
            'summary': {
                'pending_bookings': len([b for b in demo_data.bookings if b.get('status') == 'scheduled']),
                'in_progress': len([b for b in demo_data.bookings if b.get('status') == 'in_progress']),
                'completed': len([b for b in demo_data.bookings if b.get('status') == 'completed']),
                'cancelled': len([b for b in demo_data.bookings if b.get('status') == 'cancelled'])
            }
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve bookings',
            'message': str(e)
        }), 500

@admin_bp.route('/reports', methods=['GET'])
@AuthMiddleware.admin_required
def generate_reports():
    """Generate various administrative reports"""
    try:
        # Query parameters
        report_type = request.args.get('type', 'overview')  # overview, financial, user_activity, environmental
        period = request.args.get('period', 'month')  # week, month, quarter, year

        # Calculate date range
        now = datetime.now()
        if period == 'week':
            start_date = now - timedelta(days=7)
        elif period == 'quarter':
            start_date = now - timedelta(days=90)
        elif period == 'year':
            start_date = now - timedelta(days=365)
        else:  # month
            start_date = now - timedelta(days=30)

        if report_type == 'financial':
            # Financial report
            period_bookings = [
                b for b in demo_data.bookings
                if datetime.fromisoformat(b.get('created_at', now.isoformat())) >= start_date
            ]

            total_revenue = sum(b.get('actual_cost', 0) for b in period_bookings if b.get('status') == 'completed')
            total_transactions = len(period_bookings)
            avg_transaction_value = total_revenue / max(total_transactions, 1)

            report_data = {
                'type': 'financial',
                'period': period,
                'metrics': {
                    'total_revenue': round(total_revenue, 2),
                    'total_transactions': total_transactions,
                    'avg_transaction_value': round(avg_transaction_value, 2),
                    'commission_earned': round(total_revenue * 0.1, 2),  # 10% commission
                    'pending_payments': len([b for b in period_bookings if b.get('payment_status') == 'pending'])
                },
                'breakdown_by_service_type': {
                    'NGO': sum(b.get('actual_cost', 0) for b in period_bookings if self._get_provider_type(b.get('service_provider_id')) == 'NGO'),
                    'Private': sum(b.get('actual_cost', 0) for b in period_bookings if self._get_provider_type(b.get('service_provider_id')) == 'Private'),
                    'Government': sum(b.get('actual_cost', 0) for b in period_bookings if self._get_provider_type(b.get('service_provider_id')) == 'Government')
                }
            }

        elif report_type == 'user_activity':
            # User activity report
            period_classifications = [
                c for c in demo_data.classifications
                if datetime.fromisoformat(c.get('created_at', now.isoformat())) >= start_date
            ]

            active_users = len(set(
                b.get('user_id') for b in demo_data.bookings
                if b.get('user_id') and datetime.fromisoformat(b.get('created_at', now.isoformat())) >= start_date
            ))

            report_data = {
                'type': 'user_activity',
                'period': period,
                'metrics': {
                    'active_users': active_users,
                    'total_classifications': len(period_classifications),
                    'avg_classifications_per_user': len(period_classifications) / max(active_users, 1),
                    'new_registrations': random.randint(10, 50),  # Mock data
                    'user_retention_rate': random.randint(70, 90)
                },
                'top_waste_types': self._get_top_waste_types(period_classifications)
            }

        elif report_type == 'environmental':
            # Environmental impact report
            total_waste_processed = sum(
                float(b.get('quantity', '0 kg').split()[0])
                for b in demo_data.bookings
                if b.get('status') == 'completed' and
                datetime.fromisoformat(b.get('created_at', now.isoformat())) >= start_date
            )

            co2_saved = total_waste_processed * 2.0  # Mock calculation
            water_saved = total_waste_processed * 8.0
            energy_saved = total_waste_processed * 4.5

            report_data = {
                'type': 'environmental',
                'period': period,
                'metrics': {
                    'total_waste_processed_kg': round(total_waste_processed, 2),
                    'co2_saved_kg': round(co2_saved, 2),
                    'water_saved_liters': round(water_saved, 2),
                    'energy_saved_kwh': round(energy_saved, 2),
                    'trees_equivalent': round(co2_saved / 22, 1),
                    'landfill_diverted_percentage': 85.0
                },
                'waste_breakdown': self._get_waste_breakdown_by_type(start_date)
            }

        else:  # overview
            # Overview report
            report_data = {
                'type': 'overview',
                'period': period,
                'metrics': {
                    'total_users': len(demo_data.user_points) if hasattr(demo_data, 'user_points') else 0,
                    'total_bookings': len(demo_data.bookings),
                    'total_providers': len(demo_data.service_providers),
                    'total_classifications': len(demo_data.classifications),
                    'system_uptime': '99.8%',
                    'avg_response_time': '250ms'
                },
                'growth_trends': {
                    'user_growth': 12.5,
                    'booking_growth': 8.3,
                    'provider_growth': 6.2
                }
            }

        report_data.update({
            'generated_at': now.isoformat(),
            'date_range': {
                'start': start_date.isoformat(),
                'end': now.isoformat()
            }
        })

        return jsonify({
            'success': True,
            'report': report_data
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to generate report',
            'message': str(e)
        }), 500

    def _get_provider_type(self, provider_id):
        """Helper method to get provider type"""
        if not provider_id:
            return 'Unknown'
        provider = next((sp for sp in demo_data.service_providers if sp['id'] == provider_id), None)
        return provider.get('type', 'Unknown') if provider else 'Unknown'

    def _get_top_waste_types(self, classifications):
        """Helper method to get top waste types"""
        waste_counts = {}
        for classification in classifications:
            waste_type = classification.get('waste_type', 'unknown')
            waste_counts[waste_type] = waste_counts.get(waste_type, 0) + 1

        return sorted(waste_counts.items(), key=lambda x: x[1], reverse=True)[:5]

    def _get_waste_breakdown_by_type(self, start_date):
        """Helper method to get waste breakdown by type"""
        breakdown = {}
        for booking in demo_data.bookings:
            if (booking.get('status') == 'completed' and
                datetime.fromisoformat(booking.get('created_at', datetime.now().isoformat())) >= start_date):

                waste_type = booking.get('waste_type', 'unknown')
                try:
                    quantity = float(booking.get('quantity', '0 kg').split()[0])
                except (ValueError, IndexError):
                    quantity = 0
                breakdown[waste_type] = breakdown.get(waste_type, 0) + quantity

        return breakdown

@admin_bp.route('/settings', methods=['GET'])
@AuthMiddleware.admin_required
def get_system_settings():
    """Get system configuration settings"""
    try:
        settings = {
            'application': {
                'maintenance_mode': False,
                'registration_enabled': True,
                'email_verification_required': True,
                'max_file_size_mb': 16,
                'supported_file_types': ['jpg', 'jpeg', 'png', 'gif']
            },
            'payments': {
                'gateway_enabled': True,
                'processing_fee_percentage': 2.5,
                'minimum_transaction_amount': 10,
                'auto_refund_enabled': True
            },
            'notifications': {
                'email_notifications': True,
                'sms_notifications': True,
                'push_notifications': True,
                'notification_rate_limit': 100
            },
            'security': {
                'jwt_expiry_hours': 24,
                'max_login_attempts': 5,
                'password_min_length': 8,
                'two_factor_auth_enabled': False
            },
            'features': {
                'rewards_system': True,
                'community_features': True,
                'analytics_dashboard': True,
                'ai_recommendations': True
            }
        }

        return jsonify({
            'success': True,
            'settings': settings
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve settings',
            'message': str(e)
        }), 500

@admin_bp.route('/settings', methods=['PUT'])
@AuthMiddleware.admin_required
def update_system_settings():
    """Update system configuration settings"""
    try:
        admin_user_id = get_jwt_identity()
        data = request.get_json()

        # Log settings change
        action_log = {
            'id': str(uuid.uuid4()),
            'admin_id': admin_user_id,
            'action': 'settings_update',
            'details': data,
            'timestamp': datetime.now().isoformat()
        }

        if not hasattr(demo_data, 'admin_actions'):
            demo_data.admin_actions = []
        demo_data.admin_actions.append(action_log)

        return jsonify({
            'success': True,
            'message': 'Settings updated successfully',
            'action_id': action_log['id']
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to update settings',
            'message': str(e)
        }), 500

@admin_bp.route('/actions', methods=['GET'])
@AuthMiddleware.admin_required
def get_admin_actions():
    """Get admin action logs"""
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 50, type=int)

        if not hasattr(demo_data, 'admin_actions'):
            demo_data.admin_actions = []

        # Sort by timestamp (newest first)
        actions = sorted(demo_data.admin_actions, key=lambda x: x['timestamp'], reverse=True)

        # Apply pagination
        total_actions = len(actions)
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        paginated_actions = actions[start_idx:end_idx]

        return jsonify({
            'success': True,
            'actions': paginated_actions,
            'pagination': {
                'current_page': page,
                'total_pages': (total_actions + limit - 1) // limit,
                'total_actions': total_actions,
                'has_next': end_idx < total_actions,
                'has_prev': page > 1
            }
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve admin actions',
            'message': str(e)
        }), 500