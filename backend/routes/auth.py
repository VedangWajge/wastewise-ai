from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
import uuid

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


# ================= LOGIN =================
@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400

        # DEMO LOGIN (no DB)
        user_id = str(uuid.uuid4())
        print(f"Demo login: {email}")

        access_token = create_access_token(identity=user_id)
        refresh_token = create_refresh_token(identity=user_id)

        return jsonify({
            'success': True,
            'tokens': {
                'access_token': access_token,
                'refresh_token': refresh_token
            },
            'user': {
                'id': user_id,
                'email': email,
                'name': 'Demo User'
            }
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ================= REGISTER =================
@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()

        email = data.get('email')
        password = data.get('password')
        name = data.get('name', 'User')

        if not email or not password:
            return jsonify({'error': 'Email and password required'}), 400

        # DEMO REGISTER (no DB)
        user_id = str(uuid.uuid4())
        print(f"Demo register: {email}")

        access_token = create_access_token(identity=user_id)
        refresh_token = create_refresh_token(identity=user_id)

        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'tokens': {
                'access_token': access_token,
                'refresh_token': refresh_token
            },
            'user': {
                'id': user_id,
                'email': email,
                'name': name
            }
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ================= PROFILE =================
@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    try:
        user_id = get_jwt_identity()

        return jsonify({
            'user': {
                'id': user_id,
                'email': 'demo@example.com',
                'name': 'Demo User'
            }
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ================= REFRESH =================
@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    try:
        user_id = get_jwt_identity()

        access_token = create_access_token(identity=user_id)

        return jsonify({
            'access_token': access_token
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500