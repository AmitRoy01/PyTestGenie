"""
Authentication Middleware
Handles JWT token verification and user authentication
"""
from functools import wraps
from flask import request, jsonify
import jwt
import os
from models.user import UserModel


def token_required(f):
    """
    Decorator to protect routes that require authentication
    Verifies JWT token and adds user info to request
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                # Expected format: "Bearer <token>"
                token = auth_header.split(' ')[1]
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            # Decode JWT token
            secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here-change-in-production')
            algorithm = os.getenv('ALGORITHM', 'HS256')
            data = jwt.decode(token, secret_key, algorithms=[algorithm])
            
            # Get user from database
            user_model = UserModel()
            current_user = user_model.get_user_by_username(data['username'])
            
            if not current_user:
                return jsonify({'error': 'User not found'}), 401
            
            if not current_user.get('is_active', False):
                return jsonify({'error': 'User account is deactivated'}), 401
            
            if not current_user.get('is_approved', False):
                return jsonify({'error': 'User account is not approved'}), 401
            
            # Remove password from user object
            current_user.pop('password', None)
            current_user['_id'] = str(current_user['_id'])
            
            # Add user to request context
            request.current_user = current_user
            
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        except Exception as e:
            return jsonify({'error': f'Authentication failed: {str(e)}'}), 401
        
        return f(*args, **kwargs)
    
    return decorated


def admin_required(f):
    """
    Decorator to protect routes that require admin privileges
    Must be used after token_required decorator
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if not hasattr(request, 'current_user'):
            return jsonify({'error': 'Authentication required'}), 401
        
        if not request.current_user.get('is_admin', False):
            return jsonify({'error': 'Admin privileges required'}), 403
        
        return f(*args, **kwargs)
    
    return decorated


def get_current_user():
    """Helper function to get current authenticated user"""
    return getattr(request, 'current_user', None)
