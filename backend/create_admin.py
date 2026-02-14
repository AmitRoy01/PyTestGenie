"""
Create Initial Admin User
Run this script once to create the first admin user in the database
"""
import sys
import os
from pymongo import MongoClient
import bcrypt
from datetime import datetime

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_admin_user():
    """Create initial admin user with default credentials"""
    
    # Admin credentials
    ADMIN_USERNAME = "admin"
    ADMIN_EMAIL = "admin@pytestgenie.com"
    ADMIN_PASSWORD = "admin123"
    
    print("="*60)
    print("Creating Admin User in MongoDB")
    print("="*60)
    
    # Connect to MongoDB
    try:
        mongodb_url = os.getenv('MONGODB_URL', 'mongodb://localhost:27017')
        database_name = os.getenv('DATABASE_NAME', 'pyTestGenie')
        
        client = MongoClient(mongodb_url)
        db = client[database_name]
        users_collection = db['users']
        
        print(f"✓ Connected to MongoDB: {mongodb_url}")
        print(f"✓ Database: {database_name}")
        
        # Check if admin already exists
        existing_admin = users_collection.find_one({'username': ADMIN_USERNAME})
        
        if existing_admin:
            print(f"\n⚠️  Admin user '{ADMIN_USERNAME}' already exists!")
            print(f"   Email: {existing_admin.get('email')}")
            print(f"   Created: {existing_admin.get('created_at')}")
            
            response = input("\n   Do you want to reset the password? (yes/no): ")
            if response.lower() == 'yes':
                # Hash new password
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(ADMIN_PASSWORD.encode('utf-8'), salt).decode('utf-8')
                
                # Update password
                users_collection.update_one(
                    {'username': ADMIN_USERNAME},
                    {'$set': {
                        'password': hashed_password,
                        'updated_at': datetime.utcnow()
                    }}
                )
                print(f"\n✅ Admin password reset successfully!")
            else:
                print("\n   No changes made.")
            return
        
        # Hash password
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(ADMIN_PASSWORD.encode('utf-8'), salt).decode('utf-8')
        
        # Create admin user
        admin_user = {
            'username': ADMIN_USERNAME,
            'email': ADMIN_EMAIL,
            'password': hashed_password,
            'is_admin': True,
            'is_approved': True,
            'is_active': True,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = users_collection.insert_one(admin_user)
        
        print(f"\n✅ Admin user created successfully!")
        print(f"\n{'='*60}")
        print(f"Admin Credentials:")
        print(f"{'='*60}")
        print(f"Username: {ADMIN_USERNAME}")
        print(f"Email:    {ADMIN_EMAIL}")
        print(f"Password: {ADMIN_PASSWORD}")
        print(f"{'='*60}")
        print(f"\n⚠️  IMPORTANT: Change this password after first login!")
        print(f"\n✓ You can now login at: http://localhost:3000")
        print(f"✓ Backend API running at: http://localhost:5000")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure:")
        print("  1. MongoDB is running (net start MongoDB)")
        print("  2. Dependencies are installed (pip install -r requirements.txt)")
        return False
    
    return True


if __name__ == "__main__":
    print("\n🔐 PyTestGenie - Admin User Setup")
    print("="*60)
    
    success = create_admin_user()
    
    if success:
        print("\n🎉 Setup complete! You can now start the application.")
        print("\nNext steps:")
        print("  1. Start backend:  cd backend && python app_unified.py")
        print("  2. Start frontend: cd frontend && npm run dev")
        print("  3. Open browser:   http://localhost:3000")
        print("  4. Login with admin credentials shown above")
    
    print("\n")
