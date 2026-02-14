"""
User Model for MongoDB
Handles user data structure and database operations
"""
from pymongo import MongoClient, ASCENDING
from datetime import datetime
from typing import Optional, Dict, List
import os


class UserModel:
    """User model for authentication and user management"""
    
    def __init__(self):
        mongodb_url = os.getenv('MONGODB_URL', 'mongodb://localhost:27017')
        database_name = os.getenv('DATABASE_NAME', 'pyTestGenie')
        
        self.client = MongoClient(mongodb_url)
        self.db = self.client[database_name]
        self.users = self.db['users']
        
        # Create indexes
        self._create_indexes()
    
    def _create_indexes(self):
        """Create database indexes for performance and uniqueness"""
        self.users.create_index([('username', ASCENDING)], unique=True)
        self.users.create_index([('email', ASCENDING)], unique=True)
    
    def create_user(self, username: str, email: str, hashed_password: str, 
                   is_admin: bool = False, is_approved: bool = False) -> Optional[str]:
        """
        Create a new user
        
        Args:
            username: Unique username
            email: Valid email address
            hashed_password: Bcrypt hashed password
            is_admin: Whether user has admin privileges
            is_approved: Whether user is approved to login
        
        Returns:
            User ID if successful, None otherwise
        """
        try:
            user = {
                'username': username,
                'email': email,
                'password': hashed_password,
                'is_admin': is_admin,
                'is_approved': is_approved,
                'is_active': True,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
            result = self.users.insert_one(user)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Get user by username"""
        return self.users.find_one({'username': username})
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email"""
        return self.users.find_one({'email': email})
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        from bson import ObjectId
        try:
            return self.users.find_one({'_id': ObjectId(user_id)})
        except Exception:
            return None
    
    def update_user(self, username: str, update_data: Dict) -> bool:
        """
        Update user information
        
        Args:
            username: Username to update
            update_data: Dictionary of fields to update
        
        Returns:
            True if successful, False otherwise
        """
        try:
            update_data['updated_at'] = datetime.utcnow()
            result = self.users.update_one(
                {'username': username},
                {'$set': update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error updating user: {e}")
            return False
    
    def delete_user(self, username: str) -> bool:
        """
        Delete a user
        
        Args:
            username: Username to delete
        
        Returns:
            True if successful, False otherwise
        """
        try:
            result = self.users.delete_one({'username': username})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Error deleting user: {e}")
            return False
    
    def approve_user(self, username: str) -> bool:
        """Approve a user for login"""
        return self.update_user(username, {'is_approved': True})
    
    def unapprove_user(self, username: str) -> bool:
        """Unapprove a user (neutral state)"""
        return self.update_user(username, {'is_approved': False})
    
    def set_user_active(self, username: str, is_active: bool) -> bool:
        """Set user active/inactive status"""
        return self.update_user(username, {'is_active': is_active})
    
    def get_all_users(self, include_inactive: bool = True) -> List[Dict]:
        """
        Get all users
        
        Args:
            include_inactive: Whether to include inactive users
        
        Returns:
            List of user dictionaries
        """
        query = {} if include_inactive else {'is_active': True}
        users = list(self.users.find(query))
        # Convert ObjectId to string for JSON serialization
        for user in users:
            user['_id'] = str(user['_id'])
            # Remove password from response
            user.pop('password', None)
        return users
    
    def get_pending_users(self) -> List[Dict]:
        """Get all users pending approval"""
        users = list(self.users.find({'is_approved': False, 'is_active': True}))
        for user in users:
            user['_id'] = str(user['_id'])
            user.pop('password', None)
        return users
    
    def username_exists(self, username: str) -> bool:
        """Check if username already exists"""
        return self.users.count_documents({'username': username}) > 0
    
    def email_exists(self, email: str) -> bool:
        """Check if email already exists"""
        return self.users.count_documents({'email': email}) > 0
