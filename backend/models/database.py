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