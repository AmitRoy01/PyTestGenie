"""
Authentication System Setup and Testing Script
Helps with initial setup and testing of the authentication system
"""

import requests
import json
from typing import Dict, Optional

BASE_URL = "http://localhost:5000/api"


class AuthTester:
    """Helper class for testing authentication endpoints"""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.admin_token: Optional[str] = None
        self.user_token: Optional[str] = None
    
    def create_admin(self, username: str = "admin", 
                    email: str = "admin@example.com", 
                    password: str = "admin123") -> Dict:
        """Create initial admin user"""
        url = f"{self.base_url}/admin/create-admin"
        data = {
            "username": username,
            "email": email,
            "password": password,
            "secret": "SETUP_SECRET_123"
        }
        
        try:
            response = requests.post(url, json=data)
            return self._handle_response(response, f"Create Admin ({username})")
        except requests.exceptions.ConnectionError:
            return {"error": "Cannot connect to server. Make sure Flask app is running on port 5000"}
    
    def register_user(self, username: str, email: str, password: str) -> Dict:
        """Register a new user"""
        url = f"{self.base_url}/auth/register"
        data = {
            "username": username,
            "email": email,
            "password": password
        }
        
        response = requests.post(url, json=data)
        return self._handle_response(response, f"Register User ({username})")
    
    def login(self, username: str, password: str, is_admin: bool = False) -> Dict:
        """Login and save token"""
        url = f"{self.base_url}/auth/login"
        data = {
            "username": username,
            "password": password
        }
        
        response = requests.post(url, json=data)
        result = self._handle_response(response, f"Login ({username})")
        
        if response.status_code == 200 and 'data' in result and 'token' in result['data']:
            if is_admin:
                self.admin_token = result['data']['token']
                print(f"✓ Admin token saved")
            else:
                self.user_token = result['data']['token']
                print(f"✓ User token saved")
        
        return result
    
    def get_profile(self, use_admin_token: bool = False) -> Dict:
        """Get user profile"""
        url = f"{self.base_url}/auth/profile"
        token = self.admin_token if use_admin_token else self.user_token
        
        if not token:
            return {"error": "No token available. Please login first."}
        
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(url, headers=headers)
        return self._handle_response(response, "Get Profile")
    
    def get_all_users(self) -> Dict:
        """Get all users (admin only)"""
        url = f"{self.base_url}/admin/users"
        
        if not self.admin_token:
            return {"error": "Admin token required. Please login as admin first."}
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        response = requests.get(url, headers=headers)
        return self._handle_response(response, "Get All Users")
    
    def get_pending_users(self) -> Dict:
        """Get pending users (admin only)"""
        url = f"{self.base_url}/admin/users/pending"
        
        if not self.admin_token:
            return {"error": "Admin token required. Please login as admin first."}
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        response = requests.get(url, headers=headers)
        return self._handle_response(response, "Get Pending Users")
    
    def approve_user(self, username: str) -> Dict:
        """Approve a user (admin only)"""
        url = f"{self.base_url}/admin/users/{username}/approve"
        
        if not self.admin_token:
            return {"error": "Admin token required. Please login as admin first."}
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        response = requests.put(url, headers=headers)
        return self._handle_response(response, f"Approve User ({username})")
    
    def deactivate_user(self, username: str) -> Dict:
        """Deactivate a user (admin only)"""
        url = f"{self.base_url}/admin/users/{username}/deactivate"
        
        if not self.admin_token:
            return {"error": "Admin token required. Please login as admin first."}
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        response = requests.put(url, headers=headers)
        return self._handle_response(response, f"Deactivate User ({username})")
    
    def delete_user(self, username: str) -> Dict:
        """Delete a user (admin only)"""
        url = f"{self.base_url}/admin/users/{username}"
        
        if not self.admin_token:
            return {"error": "Admin token required. Please login as admin first."}
        
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        response = requests.delete(url, headers=headers)
        return self._handle_response(response, f"Delete User ({username})")
    
    def _handle_response(self, response: requests.Response, action: str) -> Dict:
        """Handle and display API response"""
        print(f"\n{'='*60}")
        print(f"Action: {action}")
        print(f"Status Code: {response.status_code}")
        
        try:
            result = response.json()
            print(f"Response: {json.dumps(result, indent=2)}")
            return result
        except:
            print(f"Response: {response.text}")
            return {"error": "Invalid JSON response"}


def run_complete_test():
    """Run a complete test of the authentication system"""
    print("\n" + "="*60)
    print("🧪 PyTestGenie Authentication System Test Suite")
    print("="*60)
    
    tester = AuthTester()
    
    # Step 1: Create Admin
    print("\n📋 Step 1: Creating Admin User...")
    tester.create_admin()
    
    # Step 2: Login as Admin
    print("\n📋 Step 2: Logging in as Admin...")
    tester.login("admin", "admin123", is_admin=True)
    
    # Step 3: Register Regular User
    print("\n📋 Step 3: Registering Regular User...")
    tester.register_user("testuser", "test@example.com", "test123")
    
    # Step 4: Try to login (should fail - not approved)
    print("\n📋 Step 4: Attempting to login as unapproved user...")
    tester.login("testuser", "test123")
    
    # Step 5: Get pending users
    print("\n📋 Step 5: Getting Pending Users...")
    tester.get_pending_users()
    
    # Step 6: Approve user
    print("\n📋 Step 6: Approving User...")
    tester.approve_user("testuser")
    
    # Step 7: Login as approved user
    print("\n📋 Step 7: Logging in as approved user...")
    tester.login("testuser", "test123")
    
    # Step 8: Get user profile
    print("\n📋 Step 8: Getting User Profile...")
    tester.get_profile()
    
    # Step 9: Get all users (admin)
    print("\n📋 Step 9: Getting All Users (Admin)...")
    tester.get_all_users()
    
    print("\n" + "="*60)
    print("✅ Test Suite Complete!")
    print("="*60)


def interactive_menu():
    """Interactive menu for testing"""
    tester = AuthTester()
    
    while True:
        print("\n" + "="*60)
        print("🔐 PyTestGenie Authentication System - Interactive Menu")
        print("="*60)
        print("\n📌 Setup:")
        print("  1. Create Admin User")
        print("  2. Login as Admin")
        print("\n👤 User Operations:")
        print("  3. Register New User")
        print("  4. Login as User")
        print("  5. Get Profile")
        print("\n👨‍💼 Admin Operations:")
        print("  6. Get All Users")
        print("  7. Get Pending Users")
        print("  8. Approve User")
        print("  9. Deactivate User")
        print("  10. Delete User")
        print("\n🧪 Testing:")
        print("  11. Run Complete Test Suite")
        print("\n  0. Exit")
        print("="*60)
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == "0":
            print("👋 Goodbye!")
            break
        elif choice == "1":
            username = input("Admin Username (admin): ").strip() or "admin"
            email = input("Admin Email (admin@example.com): ").strip() or "admin@example.com"
            password = input("Admin Password (admin123): ").strip() or "admin123"
            tester.create_admin(username, email, password)
        elif choice == "2":
            username = input("Username (admin): ").strip() or "admin"
            password = input("Password (admin123): ").strip() or "admin123"
            tester.login(username, password, is_admin=True)
        elif choice == "3":
            username = input("Username: ").strip()
            email = input("Email: ").strip()
            password = input("Password: ").strip()
            if username and email and password:
                tester.register_user(username, email, password)
        elif choice == "4":
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            if username and password:
                tester.login(username, password)
        elif choice == "5":
            use_admin = input("Use admin token? (y/n): ").strip().lower() == 'y'
            tester.get_profile(use_admin_token=use_admin)
        elif choice == "6":
            tester.get_all_users()
        elif choice == "7":
            tester.get_pending_users()
        elif choice == "8":
            username = input("Username to approve: ").strip()
            if username:
                tester.approve_user(username)
        elif choice == "9":
            username = input("Username to deactivate: ").strip()
            if username:
                tester.deactivate_user(username)
        elif choice == "10":
            username = input("Username to delete: ").strip()
            if username:
                confirm = input(f"Are you sure you want to delete '{username}'? (yes/no): ").strip()
                if confirm.lower() == 'yes':
                    tester.delete_user(username)
        elif choice == "11":
            run_complete_test()
        else:
            print("❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    import sys
    
    print("\n🚀 PyTestGenie Authentication System Setup Script")
    print("=" * 60)
    print("\n⚠️  Prerequisites:")
    print("  1. MongoDB must be running on localhost:27017")
    print("  2. Flask app must be running on localhost:5000")
    print("  3. Run: cd backend && python app_unified.py")
    print("=" * 60)
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        run_complete_test()
    else:
        interactive_menu()
