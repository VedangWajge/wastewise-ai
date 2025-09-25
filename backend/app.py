from flask import Flask, request, jsonify, session
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime
from models.database import DatabaseManager

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

if __name__ == '__main__':
    app.run(debug=True, port=5000)