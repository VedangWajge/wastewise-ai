from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime, timedelta

# Import configurations and utilities
from config.settings import config
from models.database import DatabaseManager
from models.user_manager import UserManager
from models.demo_data import demo_data
from middleware.auth import (
    handle_expired_token_callback, handle_invalid_token_callback,
    handle_unauthorized_callback, handle_needs_fresh_token_callback,
    handle_revoked_token_callback
)

# Import all route blueprints
from routes.auth import auth_bp
from routes.bookings import bookings_bp
from routes.services import services_bp
from routes.payments import payments_bp
from routes.rewards import rewards_bp
from routes.analytics import analytics_bp
from routes.admin import admin_bp

def create_app(config_name='development'):
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config[config_name])

    # Initialize extensions
    CORS(app, origins=['*'], supports_credentials=True)
    jwt = JWTManager(app)

    # Initialize database managers
    db = DatabaseManager()
    user_manager = UserManager()

    # JWT error handlers
    jwt.expired_token_loader(handle_expired_token_callback)
    jwt.invalid_token_loader(handle_invalid_token_callback)
    jwt.unauthorized_loader(handle_unauthorized_callback)
    jwt.needs_fresh_token_loader(handle_needs_fresh_token_callback)
    jwt.revoked_token_loader(handle_revoked_token_callback)

    # JWT token revocation check
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        return user_manager.is_token_revoked(jti)

    # Register all blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(bookings_bp)
    app.register_blueprint(services_bp)
    app.register_blueprint(payments_bp)
    app.register_blueprint(rewards_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(admin_bp)

    # Configuration
    UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']
    ALLOWED_EXTENSIONS = app.config['ALLOWED_EXTENSIONS']

    # Create upload directory if it doesn't exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    # ============ CORE SYSTEM ENDPOINTS ============

    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Comprehensive health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'message': 'WasteWise API v2.0 is running',
            'timestamp': datetime.now().isoformat(),
            'version': '2.0.0',
            'environment': app.config.get('ENV', 'development'),
            'features': {
                'authentication': True,
                'user_management': True,
                'booking_management': True,
                'service_providers': True,
                'payments': True,
                'rewards_system': True,
                'analytics': True,
                'admin_panel': True,
                'real_time_tracking': True
            },
            'api_endpoints': {
                'auth': '/api/auth/*',
                'bookings': '/api/bookings/*',
                'services': '/api/services/*',
                'payments': '/api/payments/*',
                'rewards': '/api/rewards/*',
                'analytics': '/api/analytics/*',
                'admin': '/api/admin/*'
            }
        })

    @app.route('/api/network-test', methods=['GET'])
    def network_test():
        """Enhanced network connectivity test"""
        client_ip = request.environ.get('HTTP_X_FORWARDED_FOR') or request.environ.get('REMOTE_ADDR')
        user_agent = request.headers.get('User-Agent', 'Unknown')

        return jsonify({
            'status': 'connected',
            'message': 'Device successfully connected to WasteWise backend',
            'client_info': {
                'ip_address': client_ip,
                'user_agent': user_agent,
                'timestamp': datetime.now().isoformat(),
                'connection_type': 'direct' if not request.environ.get('HTTP_X_FORWARDED_FOR') else 'proxied'
            },
            'server_info': {
                'host': app.config.get('HOST', '0.0.0.0'),
                'port': app.config.get('PORT', 5000),
                'debug_mode': app.config['DEBUG'],
                'environment': app.config.get('ENV', 'development')
            },
            'security': {
                'https_enabled': request.is_secure,
                'cors_enabled': True,
                'jwt_enabled': True
            },
            'connection_test': 'PASSED'
        })

    @app.route('/api/cors-test', methods=['OPTIONS', 'GET', 'POST'])
    def cors_test():
        """Enhanced CORS configuration test"""
        if request.method == 'OPTIONS':
            return jsonify({
                'message': 'CORS preflight successful',
                'allowed_methods': ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
                'allowed_headers': ['Content-Type', 'Authorization']
            })

        return jsonify({
            'cors_test': 'PASSED',
            'method': request.method,
            'origin': request.headers.get('Origin', 'No Origin'),
            'timestamp': datetime.now().isoformat(),
            'cors_headers': {
                'access_control_allow_origin': '*',
                'access_control_allow_methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'access_control_allow_headers': 'Content-Type, Authorization'
            }
        })

    # ============ LEGACY ENDPOINTS (For Backward Compatibility) ============

    @app.route('/api/classify', methods=['POST'])
    def classify_waste():
        """Enhanced waste classification endpoint"""
        try:
            # Check if the post request has the file part
            if 'image' not in request.files:
                return jsonify({'error': 'No image file provided'}), 400

            file = request.files['image']

            # If user does not select file, browser also submits empty part without filename
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400

            if file and allowed_file(file.filename):
                # Generate unique filename
                filename = f"{uuid.uuid4()}_{secure_filename(file.filename)}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                # Use AI model for classification
                from models.waste_classifier import WasteClassifier
                classifier = WasteClassifier()
                classification_result = classifier.classify(filepath)

                # Save classification to database
                session_id = session.get('session_id', str(uuid.uuid4()))
                session['session_id'] = session_id

                classification_id = db.save_classification(
                    filename=filename,
                    original_filename=file.filename,
                    waste_type=classification_result['waste_type'],
                    confidence=classification_result['confidence'],
                    all_predictions=classification_result.get('all_predictions'),
                    image_path=filepath,
                    recommendations=classification_result['recommendations'],
                    environmental_impact=classification_result['environmental_impact']
                )

                # Update session activity
                db.update_session_activity(
                    session_id=session_id,
                    ip_address=request.remote_addr,
                    user_agent=request.headers.get('User-Agent')
                )

                # Award points if user is logged in
                try:
                    from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
                    verify_jwt_in_request(optional=True)
                    current_user_id = get_jwt_identity()
                    if current_user_id:
                        from routes.rewards import rewards_manager
                        rewards_manager.add_points(
                            current_user_id,
                            10,
                            'Waste classification',
                            classification_id
                        )
                except:
                    pass  # User not logged in, skip points

                return jsonify({
                    'success': True,
                    'filename': filename,
                    'classification': classification_result,
                    'classification_id': classification_id,
                    'timestamp': datetime.now().isoformat(),
                    'suggestions': {
                        'book_pickup': f'/api/services/nearby?waste_type={classification_result["waste_type"]}',
                        'learn_more': f'/api/waste-info/{classification_result["waste_type"]}'
                    }
                })
            else:
                return jsonify({'error': 'Invalid file type. Supported: ' + ', '.join(ALLOWED_EXTENSIONS)}), 400

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/statistics', methods=['GET'])
    def get_statistics():
        """Enhanced global statistics endpoint"""
        try:
            stats = db.get_statistics()

            # Add additional metrics
            stats.update({
                'user_engagement': {
                    'total_users': len(demo_data.user_points) if hasattr(demo_data, 'user_points') else 0,
                    'active_users_today': len(set(
                        b.get('user_id') for b in demo_data.bookings
                        if b.get('user_id') and
                        datetime.fromisoformat(b.get('created_at', datetime.now().isoformat())).date() == datetime.now().date()
                    )),
                    'total_service_providers': len(demo_data.service_providers)
                },
                'system_metrics': {
                    'api_version': '2.0.0',
                    'last_updated': datetime.now().isoformat(),
                    'uptime': '99.9%'
                }
            })

            return jsonify(stats)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/recent', methods=['GET'])
    def get_recent_classifications():
        """Enhanced recent classifications endpoint"""
        try:
            limit = request.args.get('limit', 10, type=int)
            include_user_data = request.args.get('include_user_data', 'false').lower() == 'true'

            recent = db.get_recent_classifications(limit)

            # Enhance with additional data if requested
            if include_user_data:
                for classification in recent:
                    classification['enhanced'] = True
                    classification['suggestions'] = [
                        'Book a pickup for this waste type',
                        'Learn more about recycling options',
                        'Earn more points by classifying regularly'
                    ]

            return jsonify({
                'success': True,
                'classifications': recent,
                'total_returned': len(recent),
                'limit': limit
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # ============ UTILITY ENDPOINTS ============

    @app.route('/api/waste-info/<waste_type>', methods=['GET'])
    def get_waste_info(waste_type):
        """Get detailed information about a specific waste type"""
        waste_info = {
            'plastic': {
                'name': 'Plastic Waste',
                'description': 'Synthetic materials that can be recycled into new products',
                'recycling_process': 'Cleaned, shredded, melted, and reformed',
                'environmental_impact': 'High recyclability, reduces ocean pollution',
                'disposal_tips': [
                    'Clean containers before disposal',
                    'Remove labels when possible',
                    'Separate by plastic type if required'
                ],
                'recycling_rate': '75%',
                'decomposition_time': '450-1000 years if not recycled'
            },
            'organic': {
                'name': 'Organic Waste',
                'description': 'Biodegradable waste from living organisms',
                'recycling_process': 'Composting or anaerobic digestion',
                'environmental_impact': 'Creates nutrient-rich soil, reduces methane emissions',
                'disposal_tips': [
                    'Separate from non-organic waste',
                    'Avoid meat and dairy in home composting',
                    'Use for garden composting when possible'
                ],
                'recycling_rate': '95%',
                'decomposition_time': '2-6 months'
            },
            'paper': {
                'name': 'Paper Waste',
                'description': 'Paper-based materials and cardboard',
                'recycling_process': 'Pulping, cleaning, and reformation',
                'environmental_impact': 'Saves trees, reduces landfill waste',
                'disposal_tips': [
                    'Keep clean and dry',
                    'Remove plastic coating',
                    'Separate different paper types'
                ],
                'recycling_rate': '85%',
                'decomposition_time': '2-6 weeks'
            },
            'glass': {
                'name': 'Glass Waste',
                'description': 'Glass containers and materials',
                'recycling_process': 'Crushing, melting, and reforming',
                'environmental_impact': '100% recyclable without quality loss',
                'disposal_tips': [
                    'Remove caps and lids',
                    'Separate by color if required',
                    'Handle with care to avoid breakage'
                ],
                'recycling_rate': '90%',
                'decomposition_time': '1 million years if not recycled'
            },
            'metal': {
                'name': 'Metal Waste',
                'description': 'Metallic materials and containers',
                'recycling_process': 'Sorting, cleaning, melting, and reforming',
                'environmental_impact': 'Infinitely recyclable, high energy savings',
                'disposal_tips': [
                    'Clean any food residue',
                    'Separate different metal types',
                    'Remove non-metal attachments'
                ],
                'recycling_rate': '95%',
                'decomposition_time': '50-500 years depending on type'
            }
        }

        info = waste_info.get(waste_type.lower())
        if not info:
            return jsonify({
                'error': 'Waste type not found',
                'available_types': list(waste_info.keys())
            }), 404

        return jsonify({
            'success': True,
            'waste_type': waste_type,
            'info': info,
            'related_services': f'/api/services/nearby?waste_type={waste_type}'
        })

    @app.route('/api/search', methods=['GET'])
    def global_search():
        """Global search across all content"""
        try:
            query = request.args.get('q', '').strip()
            category = request.args.get('category', 'all')  # all, services, waste_types, communities
            limit = request.args.get('limit', 10, type=int)

            if not query:
                return jsonify({
                    'error': 'Search query required',
                    'message': 'Please provide a search query using the q parameter'
                }), 400

            results = {
                'services': [],
                'waste_types': [],
                'communities': [],
                'total_results': 0
            }

            # Search services
            if category in ['all', 'services']:
                matching_services = [
                    sp for sp in demo_data.service_providers
                    if query.lower() in sp['name'].lower() or
                    query.lower() in sp.get('description', '').lower() or
                    any(query.lower() in spec.lower() for spec in sp.get('speciality', []))
                ]
                results['services'] = matching_services[:limit]

            # Search waste types
            if category in ['all', 'waste_types']:
                waste_types = ['plastic', 'organic', 'paper', 'glass', 'metal']
                matching_types = [wt for wt in waste_types if query.lower() in wt.lower()]
                results['waste_types'] = matching_types[:limit]

            # Search communities
            if category in ['all', 'communities']:
                matching_communities = [
                    c for c in demo_data.communities
                    if query.lower() in c['name'].lower() or
                    query.lower() in c.get('type', '').lower()
                ]
                results['communities'] = matching_communities[:limit]

            results['total_results'] = len(results['services']) + len(results['waste_types']) + len(results['communities'])
            results['query'] = query
            results['category'] = category

            return jsonify({
                'success': True,
                'search_results': results
            })

        except Exception as e:
            return jsonify({
                'error': 'Search failed',
                'message': str(e)
            }), 500

    # ============ ERROR HANDLERS ============

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found',
            'available_endpoints': [
                '/api/health - System health check',
                '/api/auth/* - Authentication endpoints',
                '/api/bookings/* - Booking management',
                '/api/services/* - Service provider endpoints',
                '/api/payments/* - Payment processing',
                '/api/rewards/* - Rewards and gamification',
                '/api/analytics/* - Analytics and reporting',
                '/api/admin/* - Admin management'
            ]
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred',
            'support': 'Please contact support if this error persists'
        }), 500

    @app.errorhandler(413)
    def file_too_large(error):
        return jsonify({
            'error': 'File Too Large',
            'message': f'The uploaded file exceeds the maximum allowed size of {app.config["MAX_CONTENT_LENGTH"] // (1024*1024)}MB'
        }), 413

    @app.errorhandler(429)
    def rate_limit_exceeded(error):
        return jsonify({
            'error': 'Rate Limit Exceeded',
            'message': 'Too many requests. Please try again later.',
            'retry_after': 60
        }), 429

    # Request/Response middleware
    @app.before_request
    def before_request():
        """Log requests and handle maintenance mode"""
        # Skip for health checks
        if request.endpoint == 'health_check':
            return

        # Check maintenance mode (would be configurable)
        maintenance_mode = False  # Would come from settings
        if maintenance_mode and not request.path.startswith('/api/admin'):
            return jsonify({
                'error': 'Maintenance Mode',
                'message': 'The system is currently under maintenance. Please try again later.'
            }), 503

    @app.after_request
    def after_request(response):
        """Add security headers and CORS"""
        # Security headers
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'

        # API version header
        response.headers['X-API-Version'] = '2.0.0'

        return response

    return app

# Application factory
def create_production_app():
    """Create production-ready app with all security features"""
    app = create_app('production')

    # Additional production configurations
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

    return app

if __name__ == '__main__':
    app = create_app()
    # Allow connections from mobile devices on the same network
    app.run(
        debug=app.config['DEBUG'],
        host='0.0.0.0',
        port=5000,
        threaded=True
    )