from flask import Flask, request, jsonify, session
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime, timedelta
from models.database import DatabaseManager
from models.demo_data import demo_data
import random

app = Flask(__name__)
CORS(app)
app.secret_key = 'wastewise_secret_key_2024'  # Change this in production

# Initialize database
db = DatabaseManager()

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'Wastewise API is running',
        'timestamp': datetime.now().isoformat(),
        'server_info': {
            'platform': 'Flask',
            'version': '1.0.0',
            'endpoints_available': True
        }
    })

@app.route('/api/network-test', methods=['GET'])
def network_test():
    """Test endpoint to verify mobile device connectivity"""
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR') or request.environ.get('REMOTE_ADDR')
    user_agent = request.headers.get('User-Agent', 'Unknown')

    return jsonify({
        'status': 'connected',
        'message': 'Mobile device successfully connected to backend',
        'client_info': {
            'ip_address': client_ip,
            'user_agent': user_agent,
            'timestamp': datetime.now().isoformat()
        },
        'server_info': {
            'host': '0.0.0.0',
            'port': 5000,
            'debug_mode': True
        },
        'connection_test': 'PASSED'
    })

@app.route('/api/cors-test', methods=['OPTIONS', 'GET', 'POST'])
def cors_test():
    """Test CORS configuration for mobile devices"""
    if request.method == 'OPTIONS':
        return jsonify({'message': 'CORS preflight successful'})

    return jsonify({
        'cors_test': 'PASSED',
        'method': request.method,
        'origin': request.headers.get('Origin', 'No Origin'),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/classify', methods=['POST'])
def classify_waste():
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

            return jsonify({
                'success': True,
                'filename': filename,
                'classification': classification_result,
                'classification_id': classification_id,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({'error': 'Invalid file type'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    try:
        stats = db.get_statistics()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/recent', methods=['GET'])
def get_recent_classifications():
    try:
        limit = request.args.get('limit', 10, type=int)
        recent = db.get_recent_classifications(limit)
        return jsonify(recent)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# === SERVICE PROVIDER APIs ===

@app.route('/api/services/nearby', methods=['GET'])
def find_nearby_services():
    try:
        waste_type = request.args.get('waste_type')
        lat = request.args.get('lat', type=float)
        lng = request.args.get('lng', type=float)

        if not waste_type:
            return jsonify({'error': 'waste_type is required'}), 400

        location = {'lat': lat, 'lng': lng} if lat and lng else None
        services = demo_data.get_nearby_services(waste_type, location)

        return jsonify({
            'success': True,
            'services': services,
            'total_found': len(services)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/services/all', methods=['GET'])
def get_all_service_providers():
    try:
        service_type = request.args.get('type')  # NGO, E-Waste, Composting, etc.

        services = demo_data.service_providers
        if service_type:
            services = [s for s in services if s['type'].lower() == service_type.lower()]

        return jsonify({
            'success': True,
            'services': services,
            'total': len(services)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# === BOOKING APIs ===

@app.route('/api/booking/create', methods=['POST'])
def create_booking():
    try:
        booking_data = request.get_json()

        required_fields = ['service_provider_id', 'waste_type', 'quantity', 'pickup_address', 'scheduled_date']
        for field in required_fields:
            if field not in booking_data:
                return jsonify({'error': f'{field} is required'}), 400

        # Add user session info
        session_id = session.get('session_id', str(uuid.uuid4()))
        session['session_id'] = session_id
        booking_data['user_id'] = session_id

        # Simulate booking creation
        new_booking = demo_data.simulate_booking_process(booking_data)

        return jsonify({
            'success': True,
            'booking': new_booking,
            'message': 'Booking created successfully'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/booking/track/<booking_id>', methods=['GET'])
def track_booking(booking_id):
    try:
        booking = next((b for b in demo_data.bookings if b['id'] == booking_id), None)

        if not booking:
            return jsonify({'error': 'Booking not found'}), 404

        # Simulate real-time tracking updates
        if 'tracking_steps' not in booking:
            booking['tracking_steps'] = [
                {'step': 'Booking Confirmed', 'status': 'completed', 'time': booking['created_at']},
                {'step': 'Service Provider Notified', 'status': 'completed', 'time': booking['created_at']},
                {'step': 'Pickup Scheduled', 'status': 'in_progress', 'time': None},
                {'step': 'Waste Collected', 'status': 'pending', 'time': None},
                {'step': 'Processing Complete', 'status': 'pending', 'time': None}
            ]

        return jsonify({
            'success': True,
            'booking': booking
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/bookings/user', methods=['GET'])
def get_user_bookings():
    try:
        session_id = session.get('session_id')
        if not session_id:
            return jsonify({'bookings': [], 'total': 0})

        user_bookings = [b for b in demo_data.bookings if b.get('user_id') == session_id]

        return jsonify({
            'success': True,
            'bookings': user_bookings,
            'total': len(user_bookings)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# === COMMUNITY APIs ===

@app.route('/api/communities/all', methods=['GET'])
def get_all_communities():
    try:
        return jsonify({
            'success': True,
            'communities': demo_data.communities,
            'total': len(demo_data.communities)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/community/<community_id>/dashboard', methods=['GET'])
def get_community_dashboard(community_id):
    try:
        stats = demo_data.get_community_stats(community_id)

        if not stats:
            return jsonify({'error': 'Community not found'}), 404

        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/community/join', methods=['POST'])
def join_community():
    try:
        data = request.get_json()
        community_id = data.get('community_id')
        unit_number = data.get('unit_number')

        if not community_id or not unit_number:
            return jsonify({'error': 'community_id and unit_number are required'}), 400

        session_id = session.get('session_id', str(uuid.uuid4()))
        session['session_id'] = session_id
        session['community_id'] = community_id
        session['unit_number'] = unit_number

        return jsonify({
            'success': True,
            'message': f'Successfully joined community',
            'user_id': session_id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# === NOTIFICATION APIs ===

@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    try:
        return jsonify({
            'success': True,
            'notifications': demo_data.notifications,
            'unread_count': len([n for n in demo_data.notifications if not n['read']])
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/notifications/<notification_id>/read', methods=['POST'])
def mark_notification_read(notification_id):
    try:
        for notification in demo_data.notifications:
            if notification['id'] == notification_id:
                notification['read'] = True
                break

        return jsonify({
            'success': True,
            'message': 'Notification marked as read'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# === ANALYTICS APIs ===

@app.route('/api/analytics/impact', methods=['GET'])
def get_environmental_impact():
    try:
        period = request.args.get('period', 'month')  # week, month, year

        # Simulate environmental impact calculations
        if period == 'week':
            multiplier = 0.25
        elif period == 'year':
            multiplier = 12
        else:
            multiplier = 1

        impact_data = {
            'period': period,
            'co2_saved': round(245 * multiplier, 1),
            'water_saved': round(1250 * multiplier),
            'energy_saved': round(340 * multiplier),
            'waste_diverted': round(890 * multiplier),
            'trees_saved': round(12 * multiplier),
            'comparison': {
                'equivalent_to': f"{round(2.5 * multiplier, 1)} cars off road for one day",
                'energy_savings': f"Powers {round(15 * multiplier)} LED bulbs for one month"
            }
        }

        return jsonify({
            'success': True,
            'impact': impact_data
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analytics/trends', methods=['GET'])
def get_waste_trends():
    try:
        # Simulate trend data for the last 6 months
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        trends = {
            'classifications_trend': [
                {'month': month, 'count': random.randint(80, 150)}
                for month in months
            ],
            'waste_type_trends': {
                waste_type: [
                    {'month': month, 'count': random.randint(10, 40)}
                    for month in months
                ]
                for waste_type in ['plastic', 'organic', 'paper', 'glass', 'metal']
            },
            'recycling_rate_trend': [
                {'month': month, 'rate': random.randint(70, 90)}
                for month in months
            ]
        }

        return jsonify({
            'success': True,
            'trends': trends
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Allow connections from mobile devices on the same network
    app.run(debug=True, host='0.0.0.0', port=5000)