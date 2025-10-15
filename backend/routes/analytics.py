from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from datetime import datetime, timedelta
import random
import json

from middleware.auth import AuthMiddleware
from models.demo_data import demo_data
from models.database import DatabaseManager

# Create blueprint
analytics_bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')

class AnalyticsManager:
    """Advanced analytics and reporting manager"""

    def __init__(self):
        self.co2_factors = {
            'plastic': 2.5,  # kg CO2 saved per kg plastic recycled
            'paper': 1.8,
            'glass': 0.5,
            'metal': 3.2,
            'organic': 0.8
        }

        self.water_factors = {
            'plastic': 8.0,  # liters water saved per kg
            'paper': 15.0,
            'glass': 2.0,
            'metal': 12.0,
            'organic': 3.0
        }

        self.energy_factors = {
            'plastic': 5.5,  # kWh energy saved per kg
            'paper': 3.2,
            'glass': 1.8,
            'metal': 8.0,
            'organic': 1.0
        }

    def calculate_environmental_impact(self, waste_data, period_days=30):
        """Calculate environmental impact from waste data"""
        total_co2_saved = 0
        total_water_saved = 0
        total_energy_saved = 0
        total_weight = 0

        for waste_type, weight_kg in waste_data.items():
            total_weight += weight_kg
            total_co2_saved += weight_kg * self.co2_factors.get(waste_type, 1.0)
            total_water_saved += weight_kg * self.water_factors.get(waste_type, 5.0)
            total_energy_saved += weight_kg * self.energy_factors.get(waste_type, 3.0)

        return {
            'co2_saved_kg': round(total_co2_saved, 2),
            'water_saved_liters': round(total_water_saved, 2),
            'energy_saved_kwh': round(total_energy_saved, 2),
            'total_weight_kg': round(total_weight, 2),
            'trees_equivalent': round(total_co2_saved / 22, 1),  # 1 tree absorbs ~22kg CO2/year
            'car_miles_equivalent': round(total_co2_saved * 2.31, 1)  # 1kg CO2 = 2.31 miles
        }

    def generate_trend_data(self, data_points, base_value=100, volatility=0.2, trend=0.05):
        """Generate realistic trend data"""
        trends = [base_value]
        for i in range(1, data_points):
            change = random.gauss(trend, volatility)
            new_value = max(0, trends[-1] * (1 + change))
            trends.append(round(new_value, 1))
        return trends

    def get_waste_breakdown_by_user(self, user_id):
        """Get waste breakdown for specific user"""
        user_bookings = [b for b in demo_data.bookings if b.get('user_id') == user_id]
        breakdown = {}

        for booking in user_bookings:
            waste_type = booking.get('waste_type', 'unknown')
            # Extract numeric quantity (simplified)
            quantity_str = booking.get('quantity', '0 kg')
            try:
                quantity = float(quantity_str.split()[0])
            except (ValueError, IndexError):
                quantity = 1.0

            breakdown[waste_type] = breakdown.get(waste_type, 0) + quantity

        return breakdown

analytics_manager = AnalyticsManager()

@analytics_bp.route('/dashboard', methods=['GET'])
@AuthMiddleware.jwt_required
def get_dashboard_statistics():
    """Get dashboard statistics for current user"""
    try:
        current_user_id = get_jwt_identity()

        # Use DatabaseManager to get statistics from SQLite database
        db = DatabaseManager()
        stats = db.get_statistics()

        return jsonify({
            'success': True,
            'total_classifications': stats['total_classifications'],
            'recycling_rate': stats['recycling_rate'],
            'waste_breakdown': stats['waste_breakdown'],
            'environmental_impact': stats['environmental_impact']
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve dashboard statistics',
            'message': str(e)
        }), 500

@analytics_bp.route('/personal', methods=['GET'])
@AuthMiddleware.jwt_required
def get_personal_analytics():
    """Get personal analytics for current user"""
    try:
        current_user_id = get_jwt_identity()
        db = DatabaseManager()

        # Query parameters
        period = request.args.get('period', 'month')  # week, month, quarter, year
        include_predictions = request.args.get('predictions', 'false').lower() == 'true'

        # Calculate date range
        now = datetime.now()
        if period == 'week':
            start_date = now - timedelta(days=7)
            period_days = 7
        elif period == 'quarter':
            start_date = now - timedelta(days=90)
            period_days = 90
        elif period == 'year':
            start_date = now - timedelta(days=365)
            period_days = 365
        else:  # month
            start_date = now - timedelta(days=30)
            period_days = 30

        # Get user's classification stats from database
        user_stats = db.get_user_classification_stats(current_user_id, start_date.isoformat())
        waste_breakdown = user_stats['waste_breakdown']

        # Get user bookings from demo_data (will be moved to DB later)
        user_bookings = [
            b for b in demo_data.bookings
            if b.get('user_id') == current_user_id and
            datetime.fromisoformat(b.get('created_at', now.isoformat())) >= start_date
        ]

        completed_bookings = [b for b in user_bookings if b.get('status') == 'completed']

        # Calculate environmental impact
        environmental_impact = analytics_manager.calculate_environmental_impact(waste_breakdown, period_days)

        # Get user points from database
        points_data = db.get_user_points(current_user_id)
        total_points = points_data['total_points']

        # Get user badges from database
        user_badges = db.get_user_badges(current_user_id)

        achievements = {
            'total_classifications': user_stats['total_classifications'],
            'total_bookings': len([b for b in demo_data.bookings if b.get('user_id') == current_user_id]),
            'completed_bookings': len([b for b in demo_data.bookings if b.get('user_id') == current_user_id and b.get('status') == 'completed']),
            'total_points': total_points,
            'total_badges': len(user_badges),
            'carbon_footprint_reduction': environmental_impact['co2_saved_kg'],
            'consistency_score': min(100, user_stats['total_classifications'] / max(period_days, 1) * 100)
        }

        # Generate predictions if requested
        predictions = {}
        if include_predictions:
            predictions = {
                'next_month_classifications': max(5, user_stats['total_classifications'] * 1.1),
                'next_month_bookings': max(1, len(user_bookings) * 1.1),
                'projected_co2_savings': environmental_impact['co2_saved_kg'] * 1.2,
                'goal_achievement_probability': random.randint(65, 90)
            }

        analytics_data = {
            'period': period,
            'date_range': {
                'start': start_date.isoformat(),
                'end': now.isoformat()
            },
            'summary': {
                'classifications_count': user_stats['total_classifications'],
                'bookings_count': len(user_bookings),
                'completed_bookings': len(completed_bookings),
                'success_rate': round((len(completed_bookings) / max(len(user_bookings), 1)) * 100, 1)
            },
            'waste_breakdown': waste_breakdown,
            'environmental_impact': environmental_impact,
            'achievements': achievements,
            'predictions': predictions if include_predictions else None,
            'insights': [
                f"You've classified {user_stats['total_classifications']} items this {period}",
                f"Your environmental impact saved {environmental_impact['co2_saved_kg']} kg of CO2",
                f"You're {achievements['consistency_score']:.0f}% consistent with daily usage",
                f"You've earned {len(user_badges)} badges"
            ]
        }

        return jsonify({
            'success': True,
            'analytics': analytics_data
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve personal analytics',
            'message': str(e)
        }), 500

@analytics_bp.route('/community/<community_id>', methods=['GET'])
@AuthMiddleware.jwt_required
def get_community_analytics(community_id):
    """Get analytics for a specific community"""
    try:
        # Find community
        community = next((c for c in demo_data.communities if c['id'] == community_id), None)

        if not community:
            return jsonify({
                'error': 'Community not found',
                'message': f'No community found with ID {community_id}'
            }), 404

        # Query parameters
        period = request.args.get('period', 'month')

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

        # Get community bookings
        community_bookings = [
            b for b in demo_data.bookings
            if b.get('community_id') == community_id and
            datetime.fromisoformat(b.get('created_at', now.isoformat())) >= start_date
        ]

        # Calculate community waste breakdown
        waste_breakdown = {}
        for booking in community_bookings:
            waste_type = booking.get('waste_type', 'unknown')
            try:
                quantity = float(booking.get('quantity', '0 kg').split()[0])
            except (ValueError, IndexError):
                quantity = 1.0
            waste_breakdown[waste_type] = waste_breakdown.get(waste_type, 0) + quantity

        # Calculate environmental impact
        environmental_impact = analytics_manager.calculate_environmental_impact(waste_breakdown)

        # Generate participation metrics
        active_users = len(set(b.get('user_id') for b in community_bookings if b.get('user_id')))
        total_units = community.get('total_units', 100)
        participation_rate = round((active_users / total_units) * 100, 1)

        # Generate service provider performance
        provider_performance = {}
        for booking in community_bookings:
            provider_id = booking.get('service_provider_id')
            if provider_id:
                if provider_id not in provider_performance:
                    provider_performance[provider_id] = {
                        'total_bookings': 0,
                        'completed_bookings': 0,
                        'avg_rating': 0,
                        'response_time': random.randint(15, 60)  # Mock response time
                    }
                provider_performance[provider_id]['total_bookings'] += 1
                if booking.get('status') == 'completed':
                    provider_performance[provider_id]['completed_bookings'] += 1
                    if booking.get('user_rating'):
                        provider_performance[provider_id]['avg_rating'] = booking['user_rating']['overall_rating']

        # Calculate success rates
        for provider_id, perf in provider_performance.items():
            perf['success_rate'] = round((perf['completed_bookings'] / max(perf['total_bookings'], 1)) * 100, 1)

        # Generate monthly trends
        monthly_trends = []
        for i in range(6):  # Last 6 months
            month_start = now - timedelta(days=30 * (i + 1))
            month_end = now - timedelta(days=30 * i)
            month_bookings = [
                b for b in demo_data.bookings
                if b.get('community_id') == community_id and
                month_start <= datetime.fromisoformat(b.get('created_at', now.isoformat())) < month_end
            ]
            monthly_trends.insert(0, {
                'month': month_start.strftime('%b %Y'),
                'bookings': len(month_bookings),
                'waste_collected': sum(
                    float(b.get('quantity', '0 kg').split()[0])
                    for b in month_bookings
                    if b.get('quantity')
                ),
                'active_users': len(set(b.get('user_id') for b in month_bookings if b.get('user_id')))
            })

        analytics_data = {
            'community': community,
            'period': period,
            'summary': {
                'total_bookings': len(community_bookings),
                'active_users': active_users,
                'participation_rate': participation_rate,
                'total_waste_collected': sum(waste_breakdown.values()),
                'avg_bookings_per_user': round(len(community_bookings) / max(active_users, 1), 1)
            },
            'waste_breakdown': waste_breakdown,
            'environmental_impact': environmental_impact,
            'service_provider_performance': provider_performance,
            'monthly_trends': monthly_trends,
            'rankings': {
                'waste_reduction_rank': random.randint(1, 10),
                'participation_rank': random.randint(1, 10),
                'sustainability_score': random.randint(70, 95)
            },
            'recommendations': [
                'Increase awareness about organic waste composting',
                'Organize community cleanup drives',
                'Implement reward programs for top participants'
            ]
        }

        return jsonify({
            'success': True,
            'analytics': analytics_data
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve community analytics',
            'message': str(e)
        }), 500

@analytics_bp.route('/comparison', methods=['GET'])
@AuthMiddleware.jwt_required
def get_comparison_analytics():
    """Compare user or community performance with averages"""
    try:
        current_user_id = get_jwt_identity()

        # Query parameters
        compare_type = request.args.get('type', 'user')  # user, community
        compare_id = request.args.get('id', current_user_id)
        period = request.args.get('period', 'month')

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

        if compare_type == 'user':
            # User comparison
            user_bookings = [
                b for b in demo_data.bookings
                if b.get('user_id') == compare_id and
                datetime.fromisoformat(b.get('created_at', now.isoformat())) >= start_date
            ]

            user_classifications = [
                c for c in demo_data.classifications
                if compare_id in c.get('filename', '') and
                datetime.fromisoformat(c.get('created_at', now.isoformat())) >= start_date
            ]

            # Calculate averages across all users
            all_users = set(b.get('user_id') for b in demo_data.bookings if b.get('user_id'))
            avg_bookings = len(demo_data.bookings) / len(all_users) if all_users else 0
            avg_classifications = len(demo_data.classifications) / len(all_users) if all_users else 0

            comparison_data = {
                'subject': {
                    'id': compare_id,
                    'type': 'user',
                    'bookings': len(user_bookings),
                    'classifications': len(user_classifications),
                    'success_rate': round((len([b for b in user_bookings if b.get('status') == 'completed']) / max(len(user_bookings), 1)) * 100, 1)
                },
                'averages': {
                    'bookings': round(avg_bookings, 1),
                    'classifications': round(avg_classifications, 1),
                    'success_rate': 85.0  # Mock average
                },
                'percentile': {
                    'bookings': random.randint(60, 95),
                    'classifications': random.randint(60, 95),
                    'overall': random.randint(65, 90)
                }
            }

        else:  # community comparison
            # Community comparison logic (similar to user but for communities)
            community_bookings = [
                b for b in demo_data.bookings
                if b.get('community_id') == compare_id and
                datetime.fromisoformat(b.get('created_at', now.isoformat())) >= start_date
            ]

            all_communities = demo_data.communities
            avg_bookings_per_community = len(demo_data.bookings) / len(all_communities) if all_communities else 0

            comparison_data = {
                'subject': {
                    'id': compare_id,
                    'type': 'community',
                    'bookings': len(community_bookings),
                    'active_users': len(set(b.get('user_id') for b in community_bookings if b.get('user_id'))),
                    'participation_rate': random.randint(60, 90)
                },
                'averages': {
                    'bookings': round(avg_bookings_per_community, 1),
                    'active_users': random.randint(50, 100),
                    'participation_rate': 75.0
                },
                'percentile': {
                    'bookings': random.randint(60, 95),
                    'participation': random.randint(60, 95),
                    'overall': random.randint(65, 90)
                }
            }

        # Add insights
        insights = []
        if compare_type == 'user':
            if comparison_data['subject']['bookings'] > comparison_data['averages']['bookings']:
                insights.append("You're above average in booking frequency!")
            if comparison_data['subject']['classifications'] > comparison_data['averages']['classifications']:
                insights.append("Great job on waste classification!")
        else:
            if comparison_data['subject']['participation_rate'] > comparison_data['averages']['participation_rate']:
                insights.append("Your community has excellent participation!")

        comparison_data['insights'] = insights
        comparison_data['period'] = period

        return jsonify({
            'success': True,
            'comparison': comparison_data
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve comparison analytics',
            'message': str(e)
        }), 500

@analytics_bp.route('/export', methods=['POST'])
@AuthMiddleware.jwt_required
def export_analytics_data():
    """Export analytics data in various formats"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()

        export_type = data.get('type', 'personal')  # personal, community
        format_type = data.get('format', 'json')  # json, csv, pdf
        period = data.get('period', 'month')
        include_charts = data.get('include_charts', False)

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

        # Gather data based on export type
        if export_type == 'personal':
            user_bookings = [
                b for b in demo_data.bookings
                if b.get('user_id') == current_user_id and
                datetime.fromisoformat(b.get('created_at', now.isoformat())) >= start_date
            ]

            export_data = {
                'user_id': current_user_id,
                'period': period,
                'date_range': {
                    'start': start_date.isoformat(),
                    'end': now.isoformat()
                },
                'summary': {
                    'total_bookings': len(user_bookings),
                    'completed_bookings': len([b for b in user_bookings if b.get('status') == 'completed']),
                    'total_waste_handled': sum(
                        float(b.get('quantity', '0 kg').split()[0])
                        for b in user_bookings
                        if b.get('quantity')
                    )
                },
                'bookings': user_bookings,
                'environmental_impact': analytics_manager.calculate_environmental_impact(
                    analytics_manager.get_waste_breakdown_by_user(current_user_id)
                )
            }

        # Generate export file
        export_id = str(uuid.uuid4())
        export_filename = f"wastewise_analytics_{export_type}_{period}_{export_id[:8]}.{format_type}"

        # In a real implementation, you would generate the actual file
        # For demo, we'll simulate file generation
        export_record = {
            'id': export_id,
            'user_id': current_user_id,
            'filename': export_filename,
            'type': export_type,
            'format': format_type,
            'period': period,
            'status': 'ready',
            'created_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(days=7)).isoformat(),
            'download_url': f'/api/analytics/download/{export_id}',
            'file_size': f"{random.randint(50, 500)} KB"
        }

        if not hasattr(demo_data, 'exports'):
            demo_data.exports = []
        demo_data.exports.append(export_record)

        return jsonify({
            'success': True,
            'message': 'Export generated successfully',
            'export': export_record,
            'download_info': {
                'ready': True,
                'expires_in_hours': 168,  # 7 days
                'instructions': 'Click the download link to get your analytics report'
            }
        }), 201

    except Exception as e:
        return jsonify({
            'error': 'Export generation failed',
            'message': str(e)
        }), 500

@analytics_bp.route('/exports', methods=['GET'])
@AuthMiddleware.jwt_required
def get_user_exports():
    """Get user's export history"""
    try:
        current_user_id = get_jwt_identity()

        if not hasattr(demo_data, 'exports'):
            demo_data.exports = []

        user_exports = [
            e for e in demo_data.exports
            if e['user_id'] == current_user_id
        ]

        # Sort by creation date (newest first)
        user_exports.sort(key=lambda x: x['created_at'], reverse=True)

        # Check expiration status
        now = datetime.now()
        for export in user_exports:
            expires_at = datetime.fromisoformat(export['expires_at'])
            if expires_at <= now:
                export['status'] = 'expired'

        return jsonify({
            'success': True,
            'exports': user_exports,
            'total_exports': len(user_exports)
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve exports',
            'message': str(e)
        }), 500

@analytics_bp.route('/insights', methods=['GET'])
@AuthMiddleware.jwt_required
def get_ai_insights():
    """Get AI-generated insights and recommendations"""
    try:
        current_user_id = get_jwt_identity()

        # Query parameters
        insight_type = request.args.get('type', 'personal')  # personal, community, global

        # Generate AI-like insights (mock implementation)
        insights = []

        if insight_type == 'personal':
            user_bookings = [b for b in demo_data.bookings if b.get('user_id') == current_user_id]
            user_classifications = [c for c in demo_data.classifications if current_user_id in c.get('filename', '')]

            insights = [
                {
                    'type': 'achievement',
                    'title': 'Great Progress!',
                    'message': f'You\'ve completed {len(user_bookings)} waste pickups. Keep up the excellent work!',
                    'icon': '🎉',
                    'priority': 'high'
                },
                {
                    'type': 'recommendation',
                    'title': 'Optimize Your Schedule',
                    'message': 'Consider scheduling pickups on weekdays for faster service.',
                    'icon': '⏰',
                    'priority': 'medium'
                },
                {
                    'type': 'environmental',
                    'title': 'Environmental Impact',
                    'message': f'Your actions have saved approximately {random.randint(10, 50)} kg of CO2 this month!',
                    'icon': '🌱',
                    'priority': 'high'
                }
            ]

        elif insight_type == 'community':
            insights = [
                {
                    'type': 'community',
                    'title': 'Community Leader',
                    'message': 'Your community ranks in the top 20% for waste reduction efforts.',
                    'icon': '🏆',
                    'priority': 'high'
                },
                {
                    'type': 'trend',
                    'title': 'Increasing Participation',
                    'message': 'Community participation has increased by 15% this month.',
                    'icon': '📈',
                    'priority': 'medium'
                }
            ]

        # Add timestamp and personalization
        for insight in insights:
            insight['generated_at'] = datetime.now().isoformat()
            insight['personalized'] = True
            insight['actionable'] = True

        return jsonify({
            'success': True,
            'insights': insights,
            'generated_at': datetime.now().isoformat(),
            'insight_type': insight_type,
            'total_insights': len(insights)
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to generate insights',
            'message': str(e)
        }), 500