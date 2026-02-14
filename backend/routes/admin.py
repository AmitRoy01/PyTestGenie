"""
Admin Routes
Handles user management (add, delete, approve, deactivate users)
Requires admin privileges
"""
from flask import Blueprint, request, jsonify
from services.auth_service import AuthService
from models.user import UserModel
from middleware.auth import token_required, admin_required

admin_bp = Blueprint('admin', __name__)
auth_service = AuthService()
user_model = UserModel()


@admin_bp.route('/users', methods=['GET'])
@token_required
@admin_required
def get_all_users():
    """
    Get all users
    Requires admin privileges
    
    Query Parameters:
        include_inactive: Include inactive users (default: true)
    
    Returns:
        JSON response with list of users
    """
    try:
        include_inactive = request.args.get('include_inactive', 'true').lower() == 'true'
        users = user_model.get_all_users(include_inactive=include_inactive)
        
        return jsonify({
            'users': users,
            'count': len(users)
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to get users: {str(e)}'}), 500


@admin_bp.route('/users/pending', methods=['GET'])
@token_required
@admin_required
def get_pending_users():
    """
    Get all users pending approval
    Requires admin privileges
    
    Returns:
        JSON response with list of pending users
    """
    try:
        users = user_model.get_pending_users()
        
        return jsonify({
            'users': users,
            'count': len(users)
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to get pending users: {str(e)}'}), 500


@admin_bp.route('/users', methods=['POST'])
@token_required
@admin_required
def add_user():
    """
    Add a new user (by admin)
    Requires admin privileges
    
    Request Body:
        {
            "username": "string",
            "email": "string",
            "password": "string",
            "is_admin": boolean (optional),
            "is_approved": boolean (optional)
        }
    
    Returns:
        JSON response with created user
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        is_admin = data.get('is_admin', False)
        is_approved = data.get('is_approved', True)  # Admin can create pre-approved users
        
        if not username or not email or not password:
            return jsonify({'error': 'Username, email, and password are required'}), 400
        
        # Validate email format
        is_valid_email, email_error = auth_service.validate_email_format(email)
        if not is_valid_email:
            return jsonify({'error': f'Invalid email: {email_error}'}), 400
        
        # Check if username already exists
        if user_model.username_exists(username):
            return jsonify({'error': 'Username already exists'}), 400
        
        # Check if email already exists
        if user_model.email_exists(email):
            return jsonify({'error': 'Email already exists'}), 400
        
        # Hash password
        hashed_password = auth_service.hash_password(password)
        
        # Create user
        user_id = user_model.create_user(
            username=username,
            email=email,
            hashed_password=hashed_password,
            is_admin=is_admin,
            is_approved=is_approved
        )
        
        if user_id:
            return jsonify({
                'message': 'User created successfully',
                'user': {
                    'user_id': user_id,
                    'username': username,
                    'email': email,
                    'is_admin': is_admin,
                    'is_approved': is_approved
                }
            }), 201
        else:
            return jsonify({'error': 'Failed to create user'}), 500
    
    except Exception as e:
        return jsonify({'error': f'Failed to add user: {str(e)}'}), 500


@admin_bp.route('/users/<username>/approve', methods=['PUT'])
@token_required
@admin_required
def approve_user(username):
    """
    Approve a user
    Requires admin privileges
    
    Returns:
        JSON response with approval status
    """
    try:
        if not user_model.get_user_by_username(username):
            return jsonify({'error': 'User not found'}), 404
        
        success = user_model.approve_user(username)
        
        if success:
            return jsonify({
                'message': f'User {username} approved successfully'
            }), 200
        else:
            return jsonify({'error': 'Failed to approve user'}), 500
    
    except Exception as e:
        return jsonify({'error': f'Failed to approve user: {str(e)}'}), 500


@admin_bp.route('/users/<username>/unapprove', methods=['PUT'])
@token_required
@admin_required
def unapprove_user(username):
    """
    Unapprove a user (set to neutral/pending state)
    Requires admin privileges
    
    Returns:
        JSON response with unapproval status
    """
    try:
        if not user_model.get_user_by_username(username):
            return jsonify({'error': 'User not found'}), 404
        
        success = user_model.unapprove_user(username)
        
        if success:
            return jsonify({
                'message': f'User {username} set to pending approval'
            }), 200
        else:
            return jsonify({'error': 'Failed to unapprove user'}), 500
    
    except Exception as e:
        return jsonify({'error': f'Failed to unapprove user: {str(e)}'}), 500


@admin_bp.route('/users/<username>/activate', methods=['PUT'])
@token_required
@admin_required
def activate_user(username):
    """
    Activate a user
    Requires admin privileges
    
    Returns:
        JSON response with activation status
    """
    try:
        if not user_model.get_user_by_username(username):
            return jsonify({'error': 'User not found'}), 404
        
        success = user_model.set_user_active(username, True)
        
        if success:
            return jsonify({
                'message': f'User {username} activated successfully'
            }), 200
        else:
            return jsonify({'error': 'Failed to activate user'}), 500
    
    except Exception as e:
        return jsonify({'error': f'Failed to activate user: {str(e)}'}), 500


@admin_bp.route('/users/<username>/deactivate', methods=['PUT'])
@token_required
@admin_required
def deactivate_user(username):
    """
    Deactivate a user
    Requires admin privileges
    
    Returns:
        JSON response with deactivation status
    """
    try:
        if not user_model.get_user_by_username(username):
            return jsonify({'error': 'User not found'}), 404
        
        success = user_model.set_user_active(username, False)
        
        if success:
            return jsonify({
                'message': f'User {username} deactivated successfully'
            }), 200
        else:
            return jsonify({'error': 'Failed to deactivate user'}), 500
    
    except Exception as e:
        return jsonify({'error': f'Failed to deactivate user: {str(e)}'}), 500


@admin_bp.route('/users/<username>', methods=['DELETE'])
@token_required
@admin_required
def delete_user(username):
    """
    Delete a user
    Requires admin privileges
    
    Returns:
        JSON response with deletion status
    """
    try:
        if not user_model.get_user_by_username(username):
            return jsonify({'error': 'User not found'}), 404
        
        success = user_model.delete_user(username)
        
        if success:
            return jsonify({
                'message': f'User {username} deleted successfully'
            }), 200
        else:
            return jsonify({'error': 'Failed to delete user'}), 500
    
    except Exception as e:
        return jsonify({'error': f'Failed to delete user: {str(e)}'}), 500


@admin_bp.route('/users/<username>', methods=['GET'])
@token_required
@admin_required
def get_user(username):
    """
    Get user details by username
    Requires admin privileges
    
    Returns:
        JSON response with user details
    """
    try:
        user = user_model.get_user_by_username(username)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Remove password and convert ObjectId
        user.pop('password', None)
        user['_id'] = str(user['_id'])
        
        return jsonify({'user': user}), 200
    
    except Exception as e:
        return jsonify({'error': f'Failed to get user: {str(e)}'}), 500


@admin_bp.route('/create-admin', methods=['POST'])
def create_initial_admin():
    """
    Create initial admin user (for setup only)
    This endpoint should be secured or disabled in production
    
    Request Body:
        {
            "username": "string",
            "email": "string",
            "password": "string",
            "secret": "string"  # Add a secret key for security
        }
    
    Returns:
        JSON response with creation status
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Add a secret key check for security
        secret = data.get('secret', '')
        expected_secret = 'SETUP_SECRET_123'  # Change this in production
        
        if secret != expected_secret:
            return jsonify({'error': 'Invalid secret key'}), 403
        
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not username or not email or not password:
            return jsonify({'error': 'Username, email, and password are required'}), 400
        
        success, message = auth_service.create_admin_user(username, email, password)
        
        if success:
            return jsonify({'message': message}), 201
        else:
            return jsonify({'error': message}), 400
    
    except Exception as e:
        return jsonify({'error': f'Failed to create admin: {str(e)}'}), 500
