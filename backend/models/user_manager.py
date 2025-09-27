import sqlite3
import bcrypt
import uuid
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, List

class UserManager:
    def __init__(self, db_path='wastewise.db'):
        self.db_path = db_path
        self.init_user_tables()

    def init_user_tables(self):
        """Initialize user-related database tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Create users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    full_name TEXT NOT NULL,
                    phone TEXT,
                    role TEXT DEFAULT 'user',
                    is_verified BOOLEAN DEFAULT FALSE,
                    is_active BOOLEAN DEFAULT TRUE,
                    avatar_url TEXT,
                    address TEXT,
                    city TEXT,
                    state TEXT,
                    pincode TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    login_attempts INTEGER DEFAULT 0,
                    locked_until TIMESTAMP
                )
            ''')

            # Create user_profiles table for additional information
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_profiles (
                    user_id TEXT PRIMARY KEY,
                    bio TEXT,
                    preferences TEXT,
                    notification_settings TEXT,
                    language TEXT DEFAULT 'en',
                    timezone TEXT DEFAULT 'Asia/Kolkata',
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')

            # Create password_reset_tokens table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS password_reset_tokens (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    token TEXT UNIQUE NOT NULL,
                    expires_at TIMESTAMP NOT NULL,
                    used_at TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')

            # Create email_verification_tokens table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS email_verification_tokens (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    token TEXT UNIQUE NOT NULL,
                    expires_at TIMESTAMP NOT NULL,
                    verified_at TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')

            # Create revoked_tokens table for JWT blacklisting
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS revoked_tokens (
                    id TEXT PRIMARY KEY,
                    jti TEXT UNIQUE NOT NULL,
                    user_id TEXT,
                    revoked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP NOT NULL
                )
            ''')

            # Create user_activity_logs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_activity_logs (
                    id TEXT PRIMARY KEY,
                    user_id TEXT,
                    action TEXT NOT NULL,
                    details TEXT,
                    ip_address TEXT,
                    user_agent TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')

            # Create indexes for better performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_email ON users (email)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_phone ON users (phone)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_users_role ON users (role)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_revoked_tokens_jti ON revoked_tokens (jti)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_activity_logs_user_id ON user_activity_logs (user_id)')

            conn.commit()
            conn.close()
            print("User tables initialized successfully")

        except Exception as e:
            print(f"Error initializing user tables: {str(e)}")

    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

    def create_user(self, user_data: Dict) -> Optional[str]:
        """Create a new user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            user_id = str(uuid.uuid4())
            password_hash = self.hash_password(user_data['password'])

            cursor.execute('''
                INSERT INTO users (id, email, password_hash, full_name, phone, role, address, city, state, pincode)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id,
                user_data['email'],
                password_hash,
                user_data['full_name'],
                user_data.get('phone'),
                user_data.get('role', 'user'),
                user_data.get('address'),
                user_data.get('city'),
                user_data.get('state'),
                user_data.get('pincode')
            ))

            # Create user profile
            cursor.execute('''
                INSERT INTO user_profiles (user_id, preferences, notification_settings)
                VALUES (?, ?, ?)
            ''', (
                user_id,
                json.dumps({}),
                json.dumps({
                    'email_notifications': True,
                    'sms_notifications': True,
                    'push_notifications': True
                })
            ))

            conn.commit()
            conn.close()

            self.log_user_activity(user_id, 'user_registered', {'email': user_data['email']})
            return user_id

        except sqlite3.IntegrityError as e:
            if 'email' in str(e):
                raise Exception("Email already exists")
            elif 'phone' in str(e):
                raise Exception("Phone number already exists")
            else:
                raise Exception("User creation failed")
        except Exception as e:
            raise Exception(f"Error creating user: {str(e)}")

    def authenticate_user(self, email: str, password: str, ip_address: str = None) -> Optional[Dict]:
        """Authenticate user with email and password"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Check if account is locked
            cursor.execute('''
                SELECT id, password_hash, full_name, role, is_active, login_attempts, locked_until
                FROM users WHERE email = ?
            ''', (email,))

            user = cursor.fetchone()
            if not user:
                return None

            user_id, password_hash, full_name, role, is_active, login_attempts, locked_until = user

            # Check if account is locked
            if locked_until and datetime.fromisoformat(locked_until) > datetime.now():
                raise Exception("Account is temporarily locked due to multiple failed login attempts")

            if not is_active:
                raise Exception("Account is deactivated")

            # Verify password
            if not self.verify_password(password, password_hash):
                # Increment login attempts
                new_attempts = login_attempts + 1
                locked_until_time = None

                if new_attempts >= 5:  # Lock account after 5 failed attempts
                    locked_until_time = datetime.now() + timedelta(minutes=30)

                cursor.execute('''
                    UPDATE users SET login_attempts = ?, locked_until = ?
                    WHERE id = ?
                ''', (new_attempts, locked_until_time, user_id))
                conn.commit()
                conn.close()

                self.log_user_activity(user_id, 'login_failed', {'ip_address': ip_address})
                return None

            # Reset login attempts on successful login
            cursor.execute('''
                UPDATE users SET login_attempts = 0, locked_until = NULL, last_login = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (user_id,))

            conn.commit()
            conn.close()

            self.log_user_activity(user_id, 'login_success', {'ip_address': ip_address})

            return {
                'id': user_id,
                'email': email,
                'full_name': full_name,
                'role': role
            }

        except Exception as e:
            raise Exception(f"Authentication failed: {str(e)}")

    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                SELECT u.id, u.email, u.full_name, u.phone, u.role, u.is_verified,
                       u.avatar_url, u.address, u.city, u.state, u.pincode, u.created_at,
                       p.bio, p.preferences, p.notification_settings, p.language, p.timezone
                FROM users u
                LEFT JOIN user_profiles p ON u.id = p.user_id
                WHERE u.id = ? AND u.is_active = TRUE
            ''', (user_id,))

            row = cursor.fetchone()
            conn.close()

            if not row:
                return None

            return {
                'id': row[0],
                'email': row[1],
                'full_name': row[2],
                'phone': row[3],
                'role': row[4],
                'is_verified': row[5],
                'avatar_url': row[6],
                'address': row[7],
                'city': row[8],
                'state': row[9],
                'pincode': row[10],
                'created_at': row[11],
                'bio': row[12],
                'preferences': json.loads(row[13] or '{}'),
                'notification_settings': json.loads(row[14] or '{}'),
                'language': row[15],
                'timezone': row[16]
            }

        except Exception as e:
            print(f"Error getting user: {str(e)}")
            return None

    def update_user_profile(self, user_id: str, update_data: Dict) -> bool:
        """Update user profile"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Prepare user table updates
            user_fields = ['full_name', 'phone', 'avatar_url', 'address', 'city', 'state', 'pincode']
            user_updates = []
            user_values = []

            for field in user_fields:
                if field in update_data:
                    user_updates.append(f"{field} = ?")
                    user_values.append(update_data[field])

            if user_updates:
                user_values.append(user_id)
                cursor.execute(f'''
                    UPDATE users SET {', '.join(user_updates)}, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', user_values)

            # Prepare profile table updates
            profile_fields = ['bio', 'language', 'timezone']
            profile_updates = []
            profile_values = []

            for field in profile_fields:
                if field in update_data:
                    profile_updates.append(f"{field} = ?")
                    profile_values.append(update_data[field])

            # Handle preferences and notification_settings
            if 'preferences' in update_data:
                profile_updates.append("preferences = ?")
                profile_values.append(json.dumps(update_data['preferences']))

            if 'notification_settings' in update_data:
                profile_updates.append("notification_settings = ?")
                profile_values.append(json.dumps(update_data['notification_settings']))

            if profile_updates:
                profile_values.append(user_id)
                cursor.execute(f'''
                    UPDATE user_profiles SET {', '.join(profile_updates)}
                    WHERE user_id = ?
                ''', profile_values)

            conn.commit()
            conn.close()

            self.log_user_activity(user_id, 'profile_updated', update_data)
            return True

        except Exception as e:
            print(f"Error updating user profile: {str(e)}")
            return False

    def change_password(self, user_id: str, current_password: str, new_password: str) -> bool:
        """Change user password"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Verify current password
            cursor.execute('SELECT password_hash FROM users WHERE id = ?', (user_id,))
            row = cursor.fetchone()

            if not row or not self.verify_password(current_password, row[0]):
                return False

            # Update password
            new_password_hash = self.hash_password(new_password)
            cursor.execute('''
                UPDATE users SET password_hash = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (new_password_hash, user_id))

            conn.commit()
            conn.close()

            self.log_user_activity(user_id, 'password_changed')
            return True

        except Exception as e:
            print(f"Error changing password: {str(e)}")
            return False

    def revoke_token(self, jti: str, user_id: str = None, expires_at: datetime = None):
        """Add token to blacklist"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO revoked_tokens (id, jti, user_id, expires_at)
                VALUES (?, ?, ?, ?)
            ''', (str(uuid.uuid4()), jti, user_id, expires_at))

            conn.commit()
            conn.close()

        except Exception as e:
            print(f"Error revoking token: {str(e)}")

    def is_token_revoked(self, jti: str) -> bool:
        """Check if token is revoked"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('SELECT id FROM revoked_tokens WHERE jti = ?', (jti,))
            result = cursor.fetchone()
            conn.close()

            return result is not None

        except Exception as e:
            print(f"Error checking token: {str(e)}")
            return False

    def log_user_activity(self, user_id: str, action: str, details: Dict = None, ip_address: str = None, user_agent: str = None):
        """Log user activity"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO user_activity_logs (id, user_id, action, details, ip_address, user_agent)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                str(uuid.uuid4()),
                user_id,
                action,
                json.dumps(details) if details else None,
                ip_address,
                user_agent
            ))

            conn.commit()
            conn.close()

        except Exception as e:
            print(f"Error logging user activity: {str(e)}")

    def get_user_stats(self, user_id: str) -> Dict:
        """Get user statistics"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Get classification count
            cursor.execute('''
                SELECT COUNT(*) FROM classifications
                WHERE filename LIKE ?
            ''', (f"%{user_id}%",))
            classifications_count = cursor.fetchone()[0]

            # Get recent activity
            cursor.execute('''
                SELECT action, created_at FROM user_activity_logs
                WHERE user_id = ?
                ORDER BY created_at DESC LIMIT 10
            ''', (user_id,))
            recent_activities = cursor.fetchall()

            conn.close()

            return {
                'classifications_count': classifications_count,
                'recent_activities': [
                    {'action': row[0], 'timestamp': row[1]}
                    for row in recent_activities
                ]
            }

        except Exception as e:
            print(f"Error getting user stats: {str(e)}")
            return {'classifications_count': 0, 'recent_activities': []}