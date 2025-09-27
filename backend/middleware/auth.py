from functools import wraps
from flask import request, jsonify, current_app
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
import jwt
from datetime import datetime

class AuthMiddleware:
    @staticmethod
    def jwt_required(f):
        """Decorator to require valid JWT token"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                verify_jwt_in_request()
                return f(*args, **kwargs)
            except Exception as e:
                return jsonify({
                    'error': 'Authentication required',
                    'message': 'Please provide a valid access token'
                }), 401
        return decorated_function

    @staticmethod
    def optional_jwt(f):
        """Decorator for optional JWT authentication"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                verify_jwt_in_request(optional=True)
            except Exception:
                pass
            return f(*args, **kwargs)
        return decorated_function

    @staticmethod
    def admin_required(f):
        """Decorator to require admin role"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                verify_jwt_in_request()
                current_user_id = get_jwt_identity()
                claims = get_jwt()

                if not claims.get('is_admin', False):
                    return jsonify({
                        'error': 'Admin access required',
                        'message': 'You do not have permission to access this resource'
                    }), 403

                return f(*args, **kwargs)
            except Exception as e:
                return jsonify({
                    'error': 'Authentication required',
                    'message': 'Please provide a valid access token'
                }), 401
        return decorated_function

    @staticmethod
    def service_provider_required(f):
        """Decorator to require service provider role"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                verify_jwt_in_request()
                current_user_id = get_jwt_identity()
                claims = get_jwt()

                user_role = claims.get('role', 'user')
                if user_role not in ['service_provider', 'admin']:
                    return jsonify({
                        'error': 'Service provider access required',
                        'message': 'You do not have permission to access this resource'
                    }), 403

                return f(*args, **kwargs)
            except Exception as e:
                return jsonify({
                    'error': 'Authentication required',
                    'message': 'Please provide a valid access token'
                }), 401
        return decorated_function

    @staticmethod
    def get_current_user_id():
        """Get current authenticated user ID"""
        try:
            return get_jwt_identity()
        except:
            return None

    @staticmethod
    def get_current_user_claims():
        """Get current user JWT claims"""
        try:
            return get_jwt()
        except:
            return {}

def handle_expired_token_callback(jwt_header, jwt_payload):
    """Handle expired JWT tokens"""
    return jsonify({
        'error': 'Token expired',
        'message': 'Your session has expired. Please login again.'
    }), 401

def handle_invalid_token_callback(error_string):
    """Handle invalid JWT tokens"""
    return jsonify({
        'error': 'Invalid token',
        'message': 'The provided token is invalid.'
    }), 401

def handle_unauthorized_callback(error_string):
    """Handle missing JWT tokens"""
    return jsonify({
        'error': 'Authorization required',
        'message': 'Request does not contain an access token.'
    }), 401

def handle_needs_fresh_token_callback(jwt_header, jwt_payload):
    """Handle requests that need fresh tokens"""
    return jsonify({
        'error': 'Fresh token required',
        'message': 'This operation requires a fresh token. Please login again.'
    }), 401

def handle_revoked_token_callback(jwt_header, jwt_payload):
    """Handle revoked JWT tokens"""
    return jsonify({
        'error': 'Token revoked',
        'message': 'Your token has been revoked. Please login again.'
    }), 401