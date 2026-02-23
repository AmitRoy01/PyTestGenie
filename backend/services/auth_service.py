"""
Authentication Service
Handles password hashing, token generation, and authentication logic
"""
import bcrypt
import jwt
from datetime import datetime, timedelta
import os
from email_validator import validate_email, EmailNotValidError
from models.user import UserModel
from services.email_service import EmailService


class AuthService:
    """Service for handling authentication operations"""
    
    def __init__(self):
        self.user_model = UserModel()
        self.email_service = EmailService()
        self.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here-change-in-production')
        self.algorithm = os.getenv('ALGORITHM', 'HS256')
        self.token_expire_minutes = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '30'))
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using bcrypt
        
        Args:
            password: Plain text password
        
        Returns:
            Hashed password string
        """
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash
        
        Args:
            plain_password: Plain text password
            hashed_password: Hashed password from database
        
        Returns:
            True if password matches, False otherwise
        """
        try:
            return bcrypt.checkpw(
                plain_password.encode('utf-8'),
                hashed_password.encode('utf-8')
            )
        except Exception:
            return False
    
    @staticmethod
    def validate_email_format(email: str) -> tuple[bool, str]:
        """
        Validate email format
        
        Args:
            email: Email address to validate
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Validate email format
            validate_email(email)
            return True, ""
        except EmailNotValidError as e:
            return False, str(e)
    
    def generate_token(self, username: str) -> str:
        """
        Generate JWT token for user
        
        Args:
            username: Username to encode in token
        
        Returns:
            JWT token string
        """
        payload = {
            'username': username,
            'exp': datetime.utcnow() + timedelta(minutes=self.token_expire_minutes),
            'iat': datetime.utcnow()
        }
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token
    
    def register_user(self, username: str, email: str, password: str) -> tuple[bool, str, dict]:
        """
        Register a new user
        
        Args:
            username: Desired username
            email: Valid email address
            password: Plain text password
        
        Returns:
            Tuple of (success, message, user_data)
        """
        # Validate inputs
        if not username or len(username) < 3:
            return False, "Username must be at least 3 characters long", {}
        
        if not password or len(password) < 6:
            return False, "Password must be at least 6 characters long", {}
        
        # Validate email format
        is_valid_email, email_error = self.validate_email_format(email)
        if not is_valid_email:
            return False, f"Invalid email: {email_error}", {}
        
        # Check if username already exists
        if self.user_model.username_exists(username):
            return False, "Username already exists", {}
        
        # Check if email already exists
        if self.user_model.email_exists(email):
            return False, "Email already exists", {}
        
        # Hash password
        hashed_password = self.hash_password(password)
        
        # Create user (not approved by default)
        user_id = self.user_model.create_user(
            username=username,
            email=email,
            hashed_password=hashed_password,
            is_admin=False,
            is_approved=False
        )
        
        if user_id:
            return True, "Registration successful. Please wait for admin approval.", {
                'user_id': user_id,
                'username': username,
                'email': email,
                'is_approved': False
            }
        else:
            return False, "Failed to create user", {}
    
    def login_user(self, username: str, password: str) -> tuple[bool, str, dict]:
        """
        Authenticate user and generate token
        
        Args:
            username: Username
            password: Plain text password
        
        Returns:
            Tuple of (success, message, data)
        """
        # Get user from database
        user = self.user_model.get_user_by_username(username)
        
        if not user:
            return False, "Invalid username or password", {}
        
        # Check if user is active
        if not user.get('is_active', False):
            return False, "Account is deactivated. Please contact admin.", {}
        
        # Check if user is approved
        if not user.get('is_approved', False):
            return False, "Account is pending admin approval.", {}
        
        # Verify password
        if not self.verify_password(password, user['password']):
            return False, "Invalid username or password", {}
        
        # Generate token
        token = self.generate_token(username)
        
        return True, "Login successful", {
            'token': token,
            'username': user['username'],
            'email': user['email'],
            'is_admin': user.get('is_admin', False)
        }
    
    def create_admin_user(self, username: str, email: str, password: str) -> tuple[bool, str]:
        """
        Create an admin user (used for initial setup)
        
        Args:
            username: Admin username
            email: Admin email
            password: Admin password
        
        Returns:
            Tuple of (success, message)
        """
        # Check if username already exists
        if self.user_model.username_exists(username):
            return False, "Username already exists"
        
        # Check if email already exists
        if self.user_model.email_exists(email):
            return False, "Email already exists"
        
        # Hash password
        hashed_password = self.hash_password(password)
        
        # Create admin user (approved by default)
        user_id = self.user_model.create_user(
            username=username,
            email=email,
            hashed_password=hashed_password,
            is_admin=True,
            is_approved=True
        )
        
        if user_id:
            return True, "Admin user created successfully"
        else:
            return False, "Failed to create admin user"
    
    def request_password_reset(self, email: str) -> tuple[bool, str]:
        """
        Request a password reset - generates and sends reset code
        
        Args:
            email: User's email address
        
        Returns:
            Tuple of (success, message)
        """
        # Validate email format
        is_valid_email, email_error = self.validate_email_format(email)
        if not is_valid_email:
            return False, f"Invalid email: {email_error}"
        
        # Check if user exists
        user = self.user_model.get_user_by_email(email)
        if not user:
            # Don't reveal that the email doesn't exist for security
            return True, "If the email exists, a reset code has been sent"
        
        # Check if user is active
        if not user.get('is_active', False):
            return False, "Account is deactivated. Please contact admin."
        
        # Generate reset code
        reset_code = self.email_service.generate_reset_code()
        
        # Set expiration time (15 minutes from now)
        expiration = datetime.utcnow() + timedelta(minutes=15)
        
        # Save reset code to database
        if not self.user_model.set_password_reset_code(email, reset_code, expiration):
            return False, "Failed to generate reset code"
        
        # Send email
        success, message = self.email_service.send_password_reset_email(
            email, user['username'], reset_code
        )
        
        if success:
            return True, "Reset code sent to your email"
        else:
            return False, "Failed to send reset email"
    
    def verify_reset_code(self, email: str, code: str) -> tuple[bool, str]:
        """
        Verify password reset code
        
        Args:
            email: User's email address
            code: Reset code to verify
        
        Returns:
            Tuple of (success, message)
        """
        is_valid, message = self.user_model.verify_reset_code(email, code)
        return is_valid, message
    
    def reset_password(self, email: str, code: str, new_password: str) -> tuple[bool, str]:
        """
        Reset password using verified code
        
        Args:
            email: User's email address
            code: Reset code
            new_password: New password
        
        Returns:
            Tuple of (success, message)
        """
        # Validate new password
        if not new_password or len(new_password) < 6:
            return False, "Password must be at least 6 characters long"
        
        # Verify reset code
        is_valid, message = self.user_model.verify_reset_code(email, code)
        if not is_valid:
            return False, message
        
        # Hash new password
        hashed_password = self.hash_password(new_password)
        
        # Update password
        if not self.user_model.update_password(email, hashed_password):
            return False, "Failed to update password"
        
        # Clear reset code
        self.user_model.clear_reset_code(email)
        
        return True, "Password reset successful"
