from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from datetime import datetime, timedelta
import uuid

from middleware.auth import AuthMiddleware
from models.demo_data import demo_data

# Create blueprint
rewards_bp = Blueprint('rewards', __name__, url_prefix='/api/rewards')

class RewardsManager:
    """Manage user rewards, points, and badges"""

    def __init__(self):
        self.point_values = {
            'classification': 10,
            'booking_completed': 50,
            'review_submitted': 25,
            'referral': 100,
            'weekly_goal': 200,
            'monthly_goal': 500,
            'community_participation': 30,
            'eco_challenge': 75
        }

        self.badges = {
            'green_warrior': {
                'name': 'Green Warrior',
                'description': 'Complete 10 waste classifications',
                'icon': '🌿',
                'requirement': {'type': 'classification', 'count': 10},
                'points': 100
            },
            'recycling_hero': {
                'name': 'Recycling Hero',
                'description': 'Complete 5 successful bookings',
                'icon': '♻️',
                'requirement': {'type': 'booking', 'count': 5},
                'points': 250
            },
            'community_champion': {
                'name': 'Community Champion',
                'description': 'Refer 3 new users to the platform',
                'icon': '🏆',
                'requirement': {'type': 'referral', 'count': 3},
                'points': 300
            },
            'eco_activist': {
                'name': 'Eco Activist',
                'description': 'Save 100kg of waste from landfills',
                'icon': '🌍',
                'requirement': {'type': 'waste_saved', 'amount': 100},
                'points': 500
            },
            'review_master': {
                'name': 'Review Master',
                'description': 'Submit 10 helpful reviews',
                'icon': '⭐',
                'requirement': {'type': 'review', 'count': 10},
                'points': 150
            },
            'consistent_user': {
                'name': 'Consistent User',
                'description': 'Use the app for 30 consecutive days',
                'icon': '📅',
                'requirement': {'type': 'daily_streak', 'count': 30},
                'points': 400
            }
        }

        self.reward_catalog = [
            {
                'id': 'plant_sapling',
                'name': 'Plant a Sapling',
                'description': 'We will plant a tree sapling in your name',
                'category': 'environment',
                'points_required': 500,
                'image_url': '/images/rewards/sapling.jpg',
                'available': True,
                'limited_quantity': False
            },
            {
                'id': 'eco_bag',
                'name': 'Eco-friendly Jute Bag',
                'description': 'Premium jute bag for sustainable shopping',
                'category': 'merchandise',
                'points_required': 200,
                'image_url': '/images/rewards/jute_bag.jpg',
                'available': True,
                'limited_quantity': True,
                'remaining_quantity': 50
            },
            {
                'id': 'amazon_voucher_100',
                'name': '₹100 Amazon Voucher',
                'description': 'Amazon gift voucher worth ₹100',
                'category': 'voucher',
                'points_required': 800,
                'image_url': '/images/rewards/amazon_voucher.jpg',
                'available': True,
                'limited_quantity': False
            },
            {
                'id': 'compost_bin',
                'name': 'Home Compost Bin',
                'description': 'Small compost bin for kitchen waste',
                'category': 'utility',
                'points_required': 1000,
                'image_url': '/images/rewards/compost_bin.jpg',
                'available': True,
                'limited_quantity': True,
                'remaining_quantity': 25
            },
            {
                'id': 'steel_bottle',
                'name': 'Stainless Steel Water Bottle',
                'description': 'Eco-friendly steel water bottle',
                'category': 'merchandise',
                'points_required': 300,
                'image_url': '/images/rewards/steel_bottle.jpg',
                'available': True,
                'limited_quantity': True,
                'remaining_quantity': 100
            }
        ]

    def get_user_points(self, user_id):
        """Get user's current points"""
        if not hasattr(demo_data, 'user_points'):
            demo_data.user_points = {}
        return demo_data.user_points.get(user_id, 0)

    def add_points(self, user_id, points, reason, reference_id=None):
        """Add points to user account"""
        if not hasattr(demo_data, 'user_points'):
            demo_data.user_points = {}
        if not hasattr(demo_data, 'point_transactions'):
            demo_data.point_transactions = []

        current_points = self.get_user_points(user_id)
        new_points = current_points + points

        demo_data.user_points[user_id] = new_points

        # Create transaction record
        transaction = {
            'id': str(uuid.uuid4()),
            'user_id': user_id,
            'points': points,
            'type': 'earned',
            'reason': reason,
            'reference_id': reference_id,
            'balance_after': new_points,
            'created_at': datetime.now().isoformat()
        }
        demo_data.point_transactions.append(transaction)

        # Check for badge achievements
        self.check_badge_achievements(user_id)

        return new_points

    def deduct_points(self, user_id, points, reason, reference_id=None):
        """Deduct points from user account"""
        if not hasattr(demo_data, 'user_points'):
            demo_data.user_points = {}
        if not hasattr(demo_data, 'point_transactions'):
            demo_data.point_transactions = []

        current_points = self.get_user_points(user_id)
        if current_points < points:
            return None  # Insufficient points

        new_points = current_points - points
        demo_data.user_points[user_id] = new_points

        # Create transaction record
        transaction = {
            'id': str(uuid.uuid4()),
            'user_id': user_id,
            'points': -points,
            'type': 'spent',
            'reason': reason,
            'reference_id': reference_id,
            'balance_after': new_points,
            'created_at': datetime.now().isoformat()
        }
        demo_data.point_transactions.append(transaction)

        return new_points

    def get_user_badges(self, user_id):
        """Get user's earned badges"""
        if not hasattr(demo_data, 'user_badges'):
            demo_data.user_badges = {}
        return demo_data.user_badges.get(user_id, [])

    def award_badge(self, user_id, badge_id):
        """Award a badge to user"""
        if not hasattr(demo_data, 'user_badges'):
            demo_data.user_badges = {}

        user_badges = self.get_user_badges(user_id)
        if badge_id not in [b['id'] for b in user_badges]:
            badge_info = self.badges.get(badge_id)
            if badge_info:
                badge_record = {
                    'id': badge_id,
                    'name': badge_info['name'],
                    'description': badge_info['description'],
                    'icon': badge_info['icon'],
                    'earned_at': datetime.now().isoformat(),
                    'points_awarded': badge_info['points']
                }

                if user_id not in demo_data.user_badges:
                    demo_data.user_badges[user_id] = []
                demo_data.user_badges[user_id].append(badge_record)

                # Award points for the badge
                self.add_points(user_id, badge_info['points'], f'Badge earned: {badge_info["name"]}')

                return badge_record
        return None

    def check_badge_achievements(self, user_id):
        """Check and award badges based on user activity"""
        # Get user activity data
        user_classifications = len([c for c in demo_data.classifications if user_id in c.get('filename', '')])
        user_bookings = [b for b in demo_data.bookings if b.get('user_id') == user_id]
        completed_bookings = [b for b in user_bookings if b.get('status') == 'completed']
        user_reviews = len([b for b in user_bookings if b.get('user_rating')])

        # Check each badge requirement
        new_badges = []

        # Green Warrior badge
        if user_classifications >= 10:
            badge = self.award_badge(user_id, 'green_warrior')
            if badge:
                new_badges.append(badge)

        # Recycling Hero badge
        if len(completed_bookings) >= 5:
            badge = self.award_badge(user_id, 'recycling_hero')
            if badge:
                new_badges.append(badge)

        # Review Master badge
        if user_reviews >= 10:
            badge = self.award_badge(user_id, 'review_master')
            if badge:
                new_badges.append(badge)

        return new_badges

rewards_manager = RewardsManager()

@rewards_bp.route('/points', methods=['GET'])
@AuthMiddleware.jwt_required
def get_user_points():
    """Get user's current points and recent transactions"""
    try:
        current_user_id = get_jwt_identity()

        current_points = rewards_manager.get_user_points(current_user_id)

        # Get recent transactions
        if not hasattr(demo_data, 'point_transactions'):
            demo_data.point_transactions = []

        user_transactions = [
            t for t in demo_data.point_transactions
            if t['user_id'] == current_user_id
        ][-10:]  # Last 10 transactions

        # Calculate weekly progress
        week_start = datetime.now() - timedelta(days=7)
        weekly_points = sum(
            t['points'] for t in demo_data.point_transactions
            if t['user_id'] == current_user_id and
            datetime.fromisoformat(t['created_at']) >= week_start and
            t['points'] > 0
        )

        return jsonify({
            'success': True,
            'points': {
                'current_balance': current_points,
                'weekly_earned': weekly_points,
                'total_earned': sum(t['points'] for t in demo_data.point_transactions if t['user_id'] == current_user_id and t['points'] > 0),
                'total_spent': abs(sum(t['points'] for t in demo_data.point_transactions if t['user_id'] == current_user_id and t['points'] < 0))
            },
            'recent_transactions': user_transactions,
            'next_milestone': {
                'points_needed': 500 - (current_points % 500),
                'reward': 'Special milestone badge'
            }
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve points',
            'message': str(e)
        }), 500

@rewards_bp.route('/badges', methods=['GET'])
@AuthMiddleware.jwt_required
def get_user_badges():
    """Get user's earned badges and available badges"""
    try:
        current_user_id = get_jwt_identity()

        earned_badges = rewards_manager.get_user_badges(current_user_id)
        available_badges = []

        # Check progress for unearned badges
        for badge_id, badge_info in rewards_manager.badges.items():
            if badge_id not in [b['id'] for b in earned_badges]:
                # Calculate progress
                progress = 0
                if badge_info['requirement']['type'] == 'classification':
                    user_classifications = len([c for c in demo_data.classifications if current_user_id in c.get('filename', '')])
                    progress = min(100, (user_classifications / badge_info['requirement']['count']) * 100)
                elif badge_info['requirement']['type'] == 'booking':
                    completed_bookings = len([b for b in demo_data.bookings if b.get('user_id') == current_user_id and b.get('status') == 'completed'])
                    progress = min(100, (completed_bookings / badge_info['requirement']['count']) * 100)
                elif badge_info['requirement']['type'] == 'review':
                    user_reviews = len([b for b in demo_data.bookings if b.get('user_id') == current_user_id and b.get('user_rating')])
                    progress = min(100, (user_reviews / badge_info['requirement']['count']) * 100)

                available_badges.append({
                    'id': badge_id,
                    'name': badge_info['name'],
                    'description': badge_info['description'],
                    'icon': badge_info['icon'],
                    'points': badge_info['points'],
                    'requirement': badge_info['requirement'],
                    'progress': round(progress, 1),
                    'locked': progress < 100
                })

        return jsonify({
            'success': True,
            'earned_badges': earned_badges,
            'available_badges': available_badges,
            'total_badges': len(rewards_manager.badges),
            'earned_count': len(earned_badges)
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve badges',
            'message': str(e)
        }), 500

@rewards_bp.route('/leaderboard', methods=['GET'])
@AuthMiddleware.jwt_required
def get_leaderboard():
    """Get community leaderboard"""
    try:
        current_user_id = get_jwt_identity()

        # Query parameters
        period = request.args.get('period', 'weekly')  # weekly, monthly, all-time
        category = request.args.get('category', 'points')  # points, classifications, bookings

        if not hasattr(demo_data, 'user_points'):
            demo_data.user_points = {}

        # Calculate period-based filter
        now = datetime.now()
        if period == 'weekly':
            start_date = now - timedelta(days=7)
        elif period == 'monthly':
            start_date = now - timedelta(days=30)
        else:
            start_date = None

        # Get leaderboard data
        leaderboard = []
        for user_id, points in demo_data.user_points.items():
            if category == 'points':
                if period == 'all-time':
                    score = points
                else:
                    # Calculate points earned in period
                    period_transactions = [
                        t for t in demo_data.point_transactions
                        if t['user_id'] == user_id and
                        t['points'] > 0 and
                        (start_date is None or datetime.fromisoformat(t['created_at']) >= start_date)
                    ]
                    score = sum(t['points'] for t in period_transactions)
            elif category == 'classifications':
                user_classifications = [c for c in demo_data.classifications if user_id in c.get('filename', '')]
                if start_date:
                    user_classifications = [c for c in user_classifications if datetime.fromisoformat(c.get('created_at', now.isoformat())) >= start_date]
                score = len(user_classifications)
            elif category == 'bookings':
                user_bookings = [b for b in demo_data.bookings if b.get('user_id') == user_id and b.get('status') == 'completed']
                if start_date:
                    user_bookings = [b for b in user_bookings if datetime.fromisoformat(b.get('created_at', now.isoformat())) >= start_date]
                score = len(user_bookings)

            # Get user info (mock)
            user_badges = rewards_manager.get_user_badges(user_id)
            leaderboard.append({
                'user_id': user_id,
                'display_name': f'User {user_id[:8]}',  # Would come from user profile
                'score': score,
                'badge_count': len(user_badges),
                'avatar_url': f'/avatars/user_{hash(user_id) % 10}.png',
                'rank': 0  # Will be set after sorting
            })

        # Sort by score
        leaderboard.sort(key=lambda x: x['score'], reverse=True)

        # Assign ranks
        for i, entry in enumerate(leaderboard):
            entry['rank'] = i + 1

        # Find current user's position
        current_user_rank = next((entry for entry in leaderboard if entry['user_id'] == current_user_id), None)

        # Limit to top 50
        top_leaderboard = leaderboard[:50]

        return jsonify({
            'success': True,
            'leaderboard': top_leaderboard,
            'current_user_rank': current_user_rank,
            'period': period,
            'category': category,
            'total_participants': len(leaderboard)
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve leaderboard',
            'message': str(e)
        }), 500

@rewards_bp.route('/catalog', methods=['GET'])
def get_reward_catalog():
    """Get available rewards catalog"""
    try:
        # Query parameters
        category = request.args.get('category')
        min_points = request.args.get('min_points', type=int)
        max_points = request.args.get('max_points', type=int)

        catalog = rewards_manager.reward_catalog.copy()

        # Apply filters
        if category:
            catalog = [r for r in catalog if r['category'] == category]

        if min_points:
            catalog = [r for r in catalog if r['points_required'] >= min_points]

        if max_points:
            catalog = [r for r in catalog if r['points_required'] <= max_points]

        # Only show available items
        catalog = [r for r in catalog if r['available']]

        # Sort by points required
        catalog.sort(key=lambda x: x['points_required'])

        # Get unique categories
        categories = list(set(r['category'] for r in rewards_manager.reward_catalog))

        return jsonify({
            'success': True,
            'rewards': catalog,
            'categories': categories,
            'total_rewards': len(catalog)
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve reward catalog',
            'message': str(e)
        }), 500

@rewards_bp.route('/redeem', methods=['POST'])
@AuthMiddleware.jwt_required
def redeem_reward():
    """Redeem a reward using points"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()

        reward_id = data.get('reward_id')
        quantity = data.get('quantity', 1)

        if not reward_id:
            return jsonify({
                'error': 'Reward ID required',
                'message': 'Please specify which reward to redeem'
            }), 400

        # Find reward
        reward = next((r for r in rewards_manager.reward_catalog if r['id'] == reward_id), None)

        if not reward:
            return jsonify({
                'error': 'Reward not found',
                'message': f'No reward found with ID {reward_id}'
            }), 404

        # Check availability
        if not reward['available']:
            return jsonify({
                'error': 'Reward unavailable',
                'message': 'This reward is currently not available'
            }), 400

        # Check quantity for limited items
        if reward['limited_quantity'] and quantity > reward.get('remaining_quantity', 0):
            return jsonify({
                'error': 'Insufficient quantity',
                'message': f'Only {reward.get("remaining_quantity", 0)} items remaining'
            }), 400

        # Calculate total points needed
        total_points_needed = reward['points_required'] * quantity
        current_points = rewards_manager.get_user_points(current_user_id)

        if current_points < total_points_needed:
            return jsonify({
                'error': 'Insufficient points',
                'message': f'You need {total_points_needed} points but only have {current_points}'
            }), 400

        # Deduct points
        new_balance = rewards_manager.deduct_points(
            current_user_id,
            total_points_needed,
            f'Redeemed {quantity}x {reward["name"]}',
            reward_id
        )

        # Create redemption record
        redemption_id = str(uuid.uuid4())
        redemption = {
            'id': redemption_id,
            'user_id': current_user_id,
            'reward_id': reward_id,
            'reward_name': reward['name'],
            'quantity': quantity,
            'points_spent': total_points_needed,
            'status': 'processing',
            'redeemed_at': datetime.now().isoformat(),
            'estimated_delivery': (datetime.now() + timedelta(days=7)).isoformat() if reward['category'] in ['merchandise', 'utility'] else None,
            'tracking_info': None
        }

        if not hasattr(demo_data, 'redemptions'):
            demo_data.redemptions = []
        demo_data.redemptions.append(redemption)

        # Update reward quantity
        if reward['limited_quantity']:
            reward['remaining_quantity'] -= quantity

        return jsonify({
            'success': True,
            'message': 'Reward redeemed successfully',
            'redemption': redemption,
            'new_point_balance': new_balance,
            'next_steps': [
                'You will receive a confirmation email shortly',
                'Track your redemption status in the rewards section',
                'Contact support if you have any questions'
            ]
        }), 201

    except Exception as e:
        return jsonify({
            'error': 'Redemption failed',
            'message': str(e)
        }), 500

@rewards_bp.route('/redemptions', methods=['GET'])
@AuthMiddleware.jwt_required
def get_user_redemptions():
    """Get user's redemption history"""
    try:
        current_user_id = get_jwt_identity()

        if not hasattr(demo_data, 'redemptions'):
            demo_data.redemptions = []

        # Get user's redemptions
        user_redemptions = [
            r for r in demo_data.redemptions
            if r['user_id'] == current_user_id
        ]

        # Sort by redemption date (newest first)
        user_redemptions.sort(key=lambda x: x['redeemed_at'], reverse=True)

        # Add estimated delivery status
        for redemption in user_redemptions:
            if redemption.get('estimated_delivery'):
                delivery_date = datetime.fromisoformat(redemption['estimated_delivery'])
                if delivery_date <= datetime.now():
                    redemption['delivery_status'] = 'delivered'
                else:
                    days_remaining = (delivery_date - datetime.now()).days
                    redemption['delivery_status'] = f'arriving_in_{days_remaining}_days'

        return jsonify({
            'success': True,
            'redemptions': user_redemptions,
            'total_redemptions': len(user_redemptions),
            'total_points_spent': sum(r['points_spent'] for r in user_redemptions)
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve redemptions',
            'message': str(e)
        }), 500

@rewards_bp.route('/challenges', methods=['GET'])
@AuthMiddleware.jwt_required
def get_challenges():
    """Get available challenges"""
    try:
        current_user_id = get_jwt_identity()

        # Sample challenges
        challenges = [
            {
                'id': 'weekly_classifier',
                'title': 'Weekly Classifier',
                'description': 'Classify 20 waste items this week',
                'type': 'weekly',
                'target': 20,
                'current_progress': 8,  # Would be calculated from user data
                'points_reward': 100,
                'expires_at': (datetime.now() + timedelta(days=3)).isoformat(),
                'status': 'active'
            },
            {
                'id': 'monthly_booker',
                'title': 'Monthly Booker',
                'description': 'Complete 5 waste pickups this month',
                'type': 'monthly',
                'target': 5,
                'current_progress': 2,
                'points_reward': 300,
                'expires_at': (datetime.now() + timedelta(days=15)).isoformat(),
                'status': 'active'
            },
            {
                'id': 'community_helper',
                'title': 'Community Helper',
                'description': 'Refer 2 friends to join WasteWise',
                'type': 'social',
                'target': 2,
                'current_progress': 0,
                'points_reward': 200,
                'expires_at': (datetime.now() + timedelta(days=30)).isoformat(),
                'status': 'active'
            }
        ]

        return jsonify({
            'success': True,
            'challenges': challenges,
            'total_challenges': len(challenges),
            'active_challenges': len([c for c in challenges if c['status'] == 'active'])
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve challenges',
            'message': str(e)
        }), 500