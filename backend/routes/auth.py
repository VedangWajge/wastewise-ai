from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from marshmallow import ValidationError
from datetime import datetime, timedelta
import uuid

from models.user_manager import UserManager
from utils.validators import (
    UserRegistrationSchema, UserLoginSchema, UserProfileUpdateSchema,
    PasswordChangeSchema, validate_json_request
)
from middleware.auth import AuthMiddleware

# Create blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Initialize user manager
user_manager = UserManager()

@auth_bp.route('/register', methods=['POST'])
@validate_json_request(UserRegistrationSchema)
def register():
    """User registration endpoint"""
    try:
        data = request.validated_data

        # Remove confirm_password and terms_accepted from data
        data.pop('confirm_password', None)
        data.pop('terms_accepted', None)

        # Create user
        user_id = user_manager.create_user(data)

        if not user_id:
            return jsonify({
                'error': 'Registration failed',
                'message': 'Could not create user account'
            }), 500

        # Log registration
        user_manager.log_user_activity(
            user_id,
            'user_registered',
            {'email': data['email']},
            request.remote_addr,
            request.headers.get('User-Agent')
        )

        return jsonify({
            'success': True,
            'message': 'Registration successful',
            'user_id': user_id,
            'next_step': 'Please verify your email address'
        }), 201

    except Exception as e:
        return jsonify({
            'error': 'Registration failed',
            'message': str(e)
        }), 400

@auth_bp.route('/login', methods=['POST'])
@validate_json_request(UserLoginSchema)
def login():
    """User login endpoint"""
    try:
        data = request.validated_data

        # Authenticate user
        user = user_manager.authenticate_user(
            data['email'],
            data['password'],
            request.remote_addr
        )

        if not user:
            return jsonify({
                'error': 'Authentication failed',
                'message': 'Invalid email or password'
            }), 401

        # Create JWT tokens
        additional_claims = {
            'role': user['role'],
            'is_admin': user['role'] == 'admin'
        }

        expires_delta = timedelta(days=30) if data.get('remember_me') else timedelta(hours=24)

        access_token = create_access_token(
            identity=user['id'],
            additional_claims=additional_claims,
            expires_delta=expires_delta
        )

        refresh_token = create_refresh_token(
            identity=user['id'],
            additional_claims=additional_claims,
            expires_delta=timedelta(days=30)
        )

        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user': {
                'id': user['id'],
                'email': user['email'] if user['email'] else data['email'],
                'full_name': user['full_name'],
                'role': user['role']
            },
            'tokens': {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'token_type': 'Bearer'
            }
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Authentication failed',
            'message': str(e)
        }), 401

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token"""
    try:
        current_user_id = get_jwt_identity()
        claims = get_jwt()

        # Check if refresh token is revoked
        if user_manager.is_token_revoked(claims['jti']):
            return jsonify({
                'error': 'Token revoked',
                'message': 'Refresh token has been revoked'
            }), 401

        # Create new access token
        additional_claims = {
            'role': claims.get('role', 'user'),
            'is_admin': claims.get('is_admin', False)
        }

        new_token = create_access_token(
            identity=current_user_id,
            additional_claims=additional_claims
        )

        return jsonify({
            'success': True,
            'access_token': new_token,
            'token_type': 'Bearer'
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Token refresh failed',
            'message': str(e)
        }), 401

@auth_bp.route('/logout', methods=['POST'])
@AuthMiddleware.jwt_required
def logout():
    """User logout endpoint"""
    try:
        current_user_id = get_jwt_identity()
        jti = get_jwt()['jti']

        # Revoke current token
        user_manager.revoke_token(
            jti,
            current_user_id,
            datetime.now() + timedelta(hours=24)
        )

        # Log logout activity
        user_manager.log_user_activity(
            current_user_id,
            'user_logout',
            {},
            request.remote_addr,
            request.headers.get('User-Agent')
        )

        return jsonify({
            'success': True,
            'message': 'Logout successful'
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Logout failed',
            'message': str(e)
        }), 500

@auth_bp.route('/profile', methods=['GET'])
@AuthMiddleware.jwt_required
def get_profile():
    """Get user profile"""
    try:
        current_user_id = get_jwt_identity()
        user = user_manager.get_user_by_id(current_user_id)

        if not user:
            return jsonify({
                'error': 'User not found',
                'message': 'Could not retrieve user profile'
            }), 404

        # Get user statistics
        stats = user_manager.get_user_stats(current_user_id)
        user['stats'] = stats

        return jsonify({
            'success': True,
            'user': user
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Profile retrieval failed',
            'message': str(e)
        }), 500

@auth_bp.route('/profile', methods=['PUT'])
@AuthMiddleware.jwt_required
@validate_json_request(UserProfileUpdateSchema)
def update_profile():
    """Update user profile"""
    try:
        current_user_id = get_jwt_identity()
        update_data = request.validated_data

        success = user_manager.update_user_profile(current_user_id, update_data)

        if not success:
            return jsonify({
                'error': 'Profile update failed',
                'message': 'Could not update user profile'
            }), 500

        # Get updated user data
        updated_user = user_manager.get_user_by_id(current_user_id)

        return jsonify({
            'success': True,
            'message': 'Profile updated successfully',
            'user': updated_user
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Profile update failed',
            'message': str(e)
        }), 500

@auth_bp.route('/change-password', methods=['POST'])
@AuthMiddleware.jwt_required
@validate_json_request(PasswordChangeSchema)
def change_password():
    """Change user password"""
    try:
        current_user_id = get_jwt_identity()
        data = request.validated_data

        success = user_manager.change_password(
            current_user_id,
            data['current_password'],
            data['new_password']
        )

        if not success:
            return jsonify({
                'error': 'Password change failed',
                'message': 'Current password is incorrect'
            }), 400

        # Revoke all existing tokens for security
        jti = get_jwt()['jti']
        user_manager.revoke_token(
            jti,
            current_user_id,
            datetime.now() + timedelta(hours=24)
        )

        return jsonify({
            'success': True,
            'message': 'Password changed successfully. Please login again.',
            'action_required': 'login_again'
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Password change failed',
            'message': str(e)
        }), 500

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """Request password reset"""
    try:
        data = request.get_json()
        email = data.get('email')

        if not email:
            return jsonify({
                'error': 'Email required',
                'message': 'Please provide your email address'
            }), 400

        # TODO: Implement password reset email logic
        # For now, return success message

        return jsonify({
            'success': True,
            'message': 'If an account exists with this email, you will receive password reset instructions',
            'next_step': 'Check your email for reset instructions'
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Password reset request failed',
            'message': str(e)
        }), 500

@auth_bp.route('/verify-email', methods=['POST'])
def verify_email():
    """Verify email address"""
    try:
        data = request.get_json()
        token = data.get('token')

        if not token:
            return jsonify({
                'error': 'Token required',
                'message': 'Please provide verification token'
            }), 400

        # TODO: Implement email verification logic

        return jsonify({
            'success': True,
            'message': 'Email verified successfully'
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Email verification failed',
            'message': str(e)
        }), 500

@auth_bp.route('/me', methods=['GET'])
@AuthMiddleware.jwt_required
def get_current_user():
    """Get current authenticated user info"""
    try:
        current_user_id = get_jwt_identity()
        claims = get_jwt()

        user = user_manager.get_user_by_id(current_user_id)

        if not user:
            return jsonify({
                'error': 'User not found',
                'message': 'Current user not found'
            }), 404

        return jsonify({
            'success': True,
            'user': {
                'id': user['id'],
                'email': user['email'],
                'full_name': user['full_name'],
                'role': user['role'],
                'is_verified': user['is_verified'],
                'avatar_url': user['avatar_url']
            },
            'permissions': {
                'is_admin': claims.get('is_admin', False),
                'role': claims.get('role', 'user')
            }
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'User info retrieval failed',
            'message': str(e)
        }), 500

@auth_bp.route('/activity', methods=['GET'])
@AuthMiddleware.jwt_required
def get_user_activity():
    """Get user activity log"""
    try:
        current_user_id = get_jwt_identity()
        stats = user_manager.get_user_stats(current_user_id)

        return jsonify({
            'success': True,
            'activity': stats.get('recent_activities', []),
            'total_classifications': stats.get('classifications_count', 0)
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Activity retrieval failed',
            'message': str(e)
        }), 500