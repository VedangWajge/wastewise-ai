from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from werkzeug.utils import secure_filename
import os, uuid
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from config.settings import config
from models.database import DatabaseManager
from models.user_manager import UserManager
from models.waste_classifier import WasteClassifier
from models.unified_classifier import UnifiedWasteClassifier  # New unified classifier

# Import your route blueprints
from routes.auth import auth_bp
from routes.bookings import bookings_bp
from routes.services import services_bp
from routes.payments import payments_bp
from routes.rewards import rewards_bp
from routes.analytics import analytics_bp
from routes.admin import admin_bp
from routes.marketplace import marketplace_bp
from routes.ai_routes import ai_bp  # New unified AI classifier

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Enable CORS & JWT
    # Allow specific origins for CORS (required when using credentials)
    CORS(app,
         resources={r"/api/*": {"origins": ["http://localhost:3000", "http://127.0.0.1:3000"]}},
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
    jwt = JWTManager(app)

    # DB & Model instances
    db = DatabaseManager()
    user_manager = UserManager()
    # Use unified classifier instead of old WasteClassifier
    classifier = UnifiedWasteClassifier()  # Supports multiple AI providers!

    # JWT error handlers (omitted for brevity)…
    # @jwt.expired_token_loader...
    # @jwt.invalid_token_loader...
    # @jwt.token_in_blocklist_loader...

    # Register blueprints
    for bp in (auth_bp, bookings_bp, services_bp, payments_bp,
               rewards_bp, analytics_bp, admin_bp, marketplace_bp, ai_bp):
        app.register_blueprint(bp)

    # File upload config
    UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']
    ALLOWED_EXTENSIONS = set(app.config['ALLOWED_EXTENSIONS'])
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    def allowed_file(filename):
        return (
            '.' in filename
            and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        )

    @app.route('/api/classify', methods=['POST'])
    def classify_waste():
        # 1) Validate upload
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400

        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        if not allowed_file(file.filename):
            return jsonify({
                'error': f'Invalid file type. Allowed: {", ".join(ALLOWED_EXTENSIONS)}'
            }), 400

        # 2) Save to disk
        filename = f"{uuid.uuid4()}_{secure_filename(file.filename)}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # 3) Classify using unified classifier (supports multiple AI providers)
        result = classifier.classify(filepath)

        # Get recommendations
        recommendations = classifier.get_recommendations(result['waste_type'])

        # Build classification object
        classification = {
            'waste_type': result['waste_type'],
            'confidence': result['confidence'],
            'recommendations': recommendations,
            'environmental_impact': f"Proper disposal of {result['waste_type']} helps protect the environment",
            'all_predictions': result.get('all_predictions', {}),
            'provider_used': result.get('provider_used', 'unknown'),
            'raw_category': result.get('raw_category')
        }

        # 4) Persist & (optional) reward
        session_id = session.get('session_id', str(uuid.uuid4()))
        session['session_id'] = session_id

        classification_id = db.save_classification(
            filename=filename,
            original_filename=file.filename,
            waste_type=classification['waste_type'],
            confidence=classification['confidence'],
            all_predictions=classification.get('all_predictions'),
            image_path=filepath,
            recommendations=classification['recommendations'],
            environmental_impact=classification['environmental_impact']
        )

        try:
            from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
            verify_jwt_in_request(optional=True)
            user_id = get_jwt_identity()
            if user_id:
                from routes.rewards import rewards_manager
                rewards_manager.add_points(
                    user_id, 10, 'Waste classification', classification_id
                )
        except:
            pass

        # 5) Return JSON
        return jsonify({
            'success': True,
            'filename': filename,
            'classification': classification,
            'classification_id': classification_id,
            'timestamp': datetime.now().isoformat(),
            'suggestions': {
                'book_pickup': f'/api/services/nearby?waste_type={classification["waste_type"]}',
                'learn_more': f'/api/waste-info/{classification["waste_type"]}'
            }
        }), 200

    # Health, stats, error handlers…
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'error': 'Not Found'}), 404

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({'error': 'Internal Server Error'}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        debug=app.config['DEBUG'],
        host='0.0.0.0',
        port=5000,
        threaded=True
    )
