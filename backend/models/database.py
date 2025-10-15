import sqlite3
import os
from datetime import datetime
import json

class DatabaseManager:
    def __init__(self, db_path='wastewise.db'):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Initialize the SQLite database with required tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Create classifications table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS classifications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    original_filename TEXT,
                    waste_type TEXT NOT NULL,
                    confidence REAL NOT NULL,
                    all_predictions TEXT,
                    image_path TEXT,
                    recommendations TEXT,
                    environmental_impact TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Create waste_categories table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS waste_categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_name TEXT UNIQUE NOT NULL,
                    icon TEXT,
                    color_code TEXT,
                    description TEXT,
                    disposal_instructions TEXT,
                    environmental_impact TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Create user_sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT UNIQUE NOT NULL,
                    ip_address TEXT,
                    user_agent TEXT,
                    first_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    classification_count INTEGER DEFAULT 0
                )
            ''')

            # Insert default waste categories if not exists
            categories = [
                ('plastic', '♻️', '#2196f3', 'Synthetic materials that can be recycled',
                 'Place in recycling bin, clean before disposal, remove labels',
                 'High recyclability - can be processed into new products'),
                ('organic', '🌱', '#4caf50', 'Biodegradable waste from living organisms',
                 'Compost this waste, use for organic fertilizer, dispose in green bin',
                 'Can be composted to create nutrient-rich soil'),
                ('paper', '📄', '#ff9800', 'Paper-based materials and cardboard',
                 'Place in paper recycling, remove plastic coating, ensure clean and dry',
                 'Easily recyclable - saves trees and reduces landfill waste'),
                ('glass', '🗞️', '#00bcd4', 'Glass containers and materials',
                 'Place in glass recycling bin, remove caps and lids, handle with care',
                 '100% recyclable without quality loss'),
                ('metal', '🔧', '#607d8b', 'Metallic materials and containers',
                 'Place in metal recycling, clean any food residue, infinitely recyclable',
                 'Infinitely recyclable - high environmental value')
            ]

            for category in categories:
                cursor.execute('''
                    INSERT OR IGNORE INTO waste_categories
                    (category_name, icon, color_code, description, disposal_instructions, environmental_impact)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', category)

            # Create user_points table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_points (
                    user_id TEXT PRIMARY KEY,
                    total_points INTEGER DEFAULT 0,
                    points_earned INTEGER DEFAULT 0,
                    points_spent INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Create point_transactions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS point_transactions (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    points INTEGER NOT NULL,
                    transaction_type TEXT NOT NULL,
                    reason TEXT,
                    reference_id TEXT,
                    balance_after INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

            # Create user_badges table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_badges (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    badge_id TEXT NOT NULL,
                    badge_name TEXT NOT NULL,
                    badge_description TEXT,
                    icon TEXT,
                    points_awarded INTEGER DEFAULT 0,
                    earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(user_id, badge_id)
                )
            ''')

            # Create reward_redemptions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS reward_redemptions (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    reward_id TEXT NOT NULL,
                    reward_name TEXT NOT NULL,
                    quantity INTEGER DEFAULT 1,
                    points_spent INTEGER NOT NULL,
                    status TEXT DEFAULT 'processing',
                    redeemed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    estimated_delivery TIMESTAMP,
                    tracking_info TEXT
                )
            ''')

            conn.commit()
            conn.close()
            print("Database initialized successfully")

        except Exception as e:
            print(f"Error initializing database: {str(e)}")

    def save_classification(self, filename, original_filename, waste_type, confidence,
                          all_predictions=None, image_path=None, recommendations=None,
                          environmental_impact=None):
        """Save a classification result to the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO classifications
                (filename, original_filename, waste_type, confidence, all_predictions,
                 image_path, recommendations, environmental_impact)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (filename, original_filename, waste_type, confidence,
                  json.dumps(all_predictions) if all_predictions else None,
                  image_path,
                  json.dumps(recommendations) if recommendations else None,
                  environmental_impact))

            conn.commit()
            classification_id = cursor.lastrowid
            conn.close()

            return classification_id

        except Exception as e:
            print(f"Error saving classification: {str(e)}")
            return None

    def get_statistics(self):
        """Get waste classification statistics for dashboard"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Get total classifications
            cursor.execute('SELECT COUNT(*) FROM classifications')
            total_classifications = cursor.fetchone()[0]

            # Get waste breakdown
            cursor.execute('''
                SELECT waste_type, COUNT(*) as count
                FROM classifications
                GROUP BY waste_type
                ORDER BY count DESC
            ''')
            waste_breakdown = dict(cursor.fetchall())

            # Calculate recycling rate (assuming plastic, paper, glass, metal are recyclable)
            recyclable_types = ['plastic', 'paper', 'glass', 'metal']
            recyclable_count = sum(waste_breakdown.get(wtype, 0) for wtype in recyclable_types)
            recycling_rate = (recyclable_count / max(total_classifications, 1)) * 100

            # Mock environmental impact calculations
            environmental_impact = {
                'co2_saved': f"{int(recyclable_count * 1.5)} kg",
                'water_saved': f"{int(recyclable_count * 8)} liters",
                'energy_saved': f"{int(recyclable_count * 2.2)} kWh"
            }

            conn.close()

            return {
                'total_classifications': total_classifications,
                'waste_breakdown': waste_breakdown,
                'recycling_rate': round(recycling_rate, 1),
                'environmental_impact': environmental_impact
            }

        except Exception as e:
            print(f"Error getting statistics: {str(e)}")
            return {
                'total_classifications': 0,
                'waste_breakdown': {},
                'recycling_rate': 0.0,
                'environmental_impact': {
                    'co2_saved': '0 kg',
                    'water_saved': '0 liters',
                    'energy_saved': '0 kWh'
                }
            }

    def get_recent_classifications(self, limit=10):
        """Get recent classifications"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                SELECT filename, waste_type, confidence, created_at
                FROM classifications
                ORDER BY created_at DESC
                LIMIT ?
            ''', (limit,))

            results = cursor.fetchall()
            conn.close()

            return [
                {
                    'filename': row[0],
                    'waste_type': row[1],
                    'confidence': row[2],
                    'created_at': row[3]
                }
                for row in results
            ]

        except Exception as e:
            print(f"Error getting recent classifications: {str(e)}")
            return []

    def update_session_activity(self, session_id, ip_address=None, user_agent=None):
        """Update or create user session activity"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Check if session exists
            cursor.execute('SELECT id FROM user_sessions WHERE session_id = ?', (session_id,))
            session_exists = cursor.fetchone()

            if session_exists:
                # Update existing session
                cursor.execute('''
                    UPDATE user_sessions
                    SET last_activity = CURRENT_TIMESTAMP,
                        classification_count = classification_count + 1
                    WHERE session_id = ?
                ''', (session_id,))
            else:
                # Create new session
                cursor.execute('''
                    INSERT INTO user_sessions (session_id, ip_address, user_agent, classification_count)
                    VALUES (?, ?, ?, 1)
                ''', (session_id, ip_address, user_agent))

            conn.commit()
            conn.close()

        except Exception as e:
            print(f"Error updating session activity: {str(e)}")

    def cleanup_old_data(self, days=30):
        """Clean up old classification data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                DELETE FROM classifications
                WHERE created_at < datetime('now', '-{} days')
            '''.format(days))

            deleted_count = cursor.rowcount
            conn.commit()
            conn.close()

            print(f"Cleaned up {deleted_count} old classification records")
            return deleted_count

        except Exception as e:
            print(f"Error cleaning up old data: {str(e)}")
            return 0

    # ========== REWARDS SYSTEM METHODS ==========

    def get_user_points(self, user_id):
        """Get user's current points balance"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('SELECT total_points, points_earned, points_spent FROM user_points WHERE user_id = ?', (user_id,))
            result = cursor.fetchone()
            conn.close()

            if result:
                return {
                    'total_points': result[0],
                    'points_earned': result[1],
                    'points_spent': result[2]
                }
            return {'total_points': 0, 'points_earned': 0, 'points_spent': 0}

        except Exception as e:
            print(f"Error getting user points: {str(e)}")
            return {'total_points': 0, 'points_earned': 0, 'points_spent': 0}

    def add_points(self, user_id, points, transaction_type, reason, reference_id=None):
        """Add points to user's account"""
        try:
            import uuid
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Get or create user points record
            cursor.execute('SELECT total_points, points_earned FROM user_points WHERE user_id = ?', (user_id,))
            result = cursor.fetchone()

            if result:
                new_total = result[0] + points
                new_earned = result[1] + points
                cursor.execute('''
                    UPDATE user_points
                    SET total_points = ?, points_earned = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE user_id = ?
                ''', (new_total, new_earned, user_id))
            else:
                new_total = points
                new_earned = points
                cursor.execute('''
                    INSERT INTO user_points (user_id, total_points, points_earned, points_spent)
                    VALUES (?, ?, ?, 0)
                ''', (user_id, new_total, new_earned))

            # Create transaction record
            transaction_id = str(uuid.uuid4())
            cursor.execute('''
                INSERT INTO point_transactions (id, user_id, points, transaction_type, reason, reference_id, balance_after)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (transaction_id, user_id, points, transaction_type, reason, reference_id, new_total))

            conn.commit()
            conn.close()
            return new_total

        except Exception as e:
            print(f"Error adding points: {str(e)}")
            return None

    def deduct_points(self, user_id, points, transaction_type, reason, reference_id=None):
        """Deduct points from user's account"""
        try:
            import uuid
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('SELECT total_points, points_spent FROM user_points WHERE user_id = ?', (user_id,))
            result = cursor.fetchone()

            if not result or result[0] < points:
                conn.close()
                return None  # Insufficient points

            new_total = result[0] - points
            new_spent = result[1] + points

            cursor.execute('''
                UPDATE user_points
                SET total_points = ?, points_spent = ?, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
            ''', (new_total, new_spent, user_id))

            # Create transaction record
            transaction_id = str(uuid.uuid4())
            cursor.execute('''
                INSERT INTO point_transactions (id, user_id, points, transaction_type, reason, reference_id, balance_after)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (transaction_id, user_id, -points, transaction_type, reason, reference_id, new_total))

            conn.commit()
            conn.close()
            return new_total

        except Exception as e:
            print(f"Error deducting points: {str(e)}")
            return None

    def get_point_transactions(self, user_id, limit=10):
        """Get user's recent point transactions"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                SELECT id, points, transaction_type, reason, reference_id, balance_after, created_at
                FROM point_transactions
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT ?
            ''', (user_id, limit))

            results = cursor.fetchall()
            conn.close()

            return [
                {
                    'id': row[0],
                    'points': row[1],
                    'type': row[2],
                    'reason': row[3],
                    'reference_id': row[4],
                    'balance_after': row[5],
                    'created_at': row[6]
                }
                for row in results
            ]

        except Exception as e:
            print(f"Error getting point transactions: {str(e)}")
            return []

    def add_user_badge(self, user_id, badge_id, badge_name, badge_description, icon, points_awarded):
        """Award a badge to a user"""
        try:
            import uuid
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            badge_record_id = str(uuid.uuid4())
            cursor.execute('''
                INSERT INTO user_badges (id, user_id, badge_id, badge_name, badge_description, icon, points_awarded)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (badge_record_id, user_id, badge_id, badge_name, badge_description, icon, points_awarded))

            conn.commit()
            conn.close()
            return badge_record_id

        except sqlite3.IntegrityError:
            # Badge already awarded
            return None
        except Exception as e:
            print(f"Error adding badge: {str(e)}")
            return None

    def get_user_badges(self, user_id):
        """Get all badges earned by a user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                SELECT id, badge_id, badge_name, badge_description, icon, points_awarded, earned_at
                FROM user_badges
                WHERE user_id = ?
                ORDER BY earned_at DESC
            ''', (user_id,))

            results = cursor.fetchall()
            conn.close()

            return [
                {
                    'id': row[0],
                    'badge_id': row[1],
                    'name': row[2],
                    'description': row[3],
                    'icon': row[4],
                    'points_awarded': row[5],
                    'earned_at': row[6]
                }
                for row in results
            ]

        except Exception as e:
            print(f"Error getting user badges: {str(e)}")
            return []

    def create_redemption(self, user_id, reward_id, reward_name, quantity, points_spent, estimated_delivery=None):
        """Create a reward redemption record"""
        try:
            import uuid
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            redemption_id = str(uuid.uuid4())
            cursor.execute('''
                INSERT INTO reward_redemptions
                (id, user_id, reward_id, reward_name, quantity, points_spent, estimated_delivery)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (redemption_id, user_id, reward_id, reward_name, quantity, points_spent, estimated_delivery))

            conn.commit()
            conn.close()
            return redemption_id

        except Exception as e:
            print(f"Error creating redemption: {str(e)}")
            return None

    def get_user_redemptions(self, user_id):
        """Get all redemptions for a user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                SELECT id, reward_id, reward_name, quantity, points_spent, status, redeemed_at, estimated_delivery, tracking_info
                FROM reward_redemptions
                WHERE user_id = ?
                ORDER BY redeemed_at DESC
            ''', (user_id,))

            results = cursor.fetchall()
            conn.close()

            return [
                {
                    'id': row[0],
                    'reward_id': row[1],
                    'reward_name': row[2],
                    'quantity': row[3],
                    'points_spent': row[4],
                    'status': row[5],
                    'redeemed_at': row[6],
                    'estimated_delivery': row[7],
                    'tracking_info': row[8]
                }
                for row in results
            ]

        except Exception as e:
            print(f"Error getting redemptions: {str(e)}")
            return []

    # ========== ANALYTICS METHODS ==========

    def get_user_classification_stats(self, user_id, start_date=None):
        """Get classification statistics for a specific user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Get user's classifications with optional date filter
            if start_date:
                cursor.execute('''
                    SELECT waste_type, COUNT(*) as count
                    FROM classifications
                    WHERE filename LIKE ? AND created_at >= ?
                    GROUP BY waste_type
                ''', (f'%{user_id}%', start_date))
            else:
                cursor.execute('''
                    SELECT waste_type, COUNT(*) as count
                    FROM classifications
                    WHERE filename LIKE ?
                    GROUP BY waste_type
                ''', (f'%{user_id}%',))

            waste_breakdown = dict(cursor.fetchall())

            # Get total count
            total = sum(waste_breakdown.values())

            conn.close()

            return {
                'total_classifications': total,
                'waste_breakdown': waste_breakdown
            }

        except Exception as e:
            print(f"Error getting user classification stats: {str(e)}")
            return {'total_classifications': 0, 'waste_breakdown': {}}

    def get_leaderboard_data(self, metric='points', limit=50):
        """Get leaderboard data based on specified metric"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            if metric == 'points':
                cursor.execute('''
                    SELECT user_id, total_points
                    FROM user_points
                    ORDER BY total_points DESC
                    LIMIT ?
                ''', (limit,))

            results = cursor.fetchall()
            conn.close()

            return [
                {'user_id': row[0], 'score': row[1], 'rank': i+1}
                for i, row in enumerate(results)
            ]

        except Exception as e:
            print(f"Error getting leaderboard data: {str(e)}")
            return []