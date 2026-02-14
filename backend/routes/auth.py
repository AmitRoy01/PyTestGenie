"""
Authentication Routes
Handles user registration, login, and profile management
"""
from flask import Blueprint, request, jsonify
from services.auth_service import AuthService
from middleware.auth import token_required, get_current_user

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    
    Request Body:
        {
            "username": "string",
            "email": "string",
            "password": "string"
        }
    
    Returns:
        JSON response with registration status
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not username or not email or not password:
            return jsonify({'error': 'Username, email, and password are required'}), 400
        
        # Register user
        success, message, user_data = auth_service.register_user(username, email, password)
        
        if success:
            return jsonify({
                'message': message,
                'user': user_data
            }), 201
        else:
            return jsonify({'error': message}), 400
    
    except Exception as e:
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login with username and password
    
    Request Body:
        {
            "username": "string",
            "password": "string"
        }
    
    Returns:
        JSON response with JWT token
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400
        
        # Authenticate user
        success, message, user_data = auth_service.login_user(username, password)
        
        if success:
            return jsonify({
                'message': message,
                'data': user_data
            }), 200
        else:
            return jsonify({'error': message}), 401
    
    except Exception as e:
        return jsonify({'error': f'Login failed: {str(e)}'}), 500


@auth_bp.route('/profile', methods=['GET'])
@token_required
def get_profile():
    """
    Get current user profile
    Requires authentication token
    
    Returns:
        JSON response with user profile
    """
    try:
        current_user = get_current_user()
        
        if not current_user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'user': {
                'username': current_user['username'],
                'email': current_user['email'],
                'is_admin': current_user.get('is_admin', False),
                'is_approved': current_user.get('is_approved', False),
                'is_active': current_user.get('is_active', False),
                'created_at': str(current_user.get('created_at', ''))
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to get profile: {str(e)}'}), 500


@auth_bp.route('/verify-token', methods=['GET'])
@token_required
def verify_token():
    """
    Verify if token is valid
    Requires authentication token
    
    Returns:
        JSON response with verification status
    """
    try:
        current_user = get_current_user()
        
        return jsonify({
            'valid': True,
            'user': {
                'username': current_user['username'],
                'is_admin': current_user.get('is_admin', False)
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Token verification failed: {str(e)}'}), 500
