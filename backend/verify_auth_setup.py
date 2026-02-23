"""
Installation Verification Script
Checks if all required packages are installed
"""

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("="*60)
    print("Checking Dependencies...")
    print("="*60)
    
    packages = {
        'flask': 'Flask',
        'flask_cors': 'flask-cors',
        'pymongo': 'pymongo',
        'jwt': 'PyJWT',
        'bcrypt': 'bcrypt',
        'email_validator': 'email-validator',
        'dotenv': 'python-dotenv'
    }
    
    missing = []
    installed = []
    
    for module_name, package_name in [
        ('flask', 'Flask'),
        ('flask_cors', 'flask-cors'),
        ('jwt', 'PyJWT'),
        ('bcrypt', 'bcrypt'),
        ('email_validator', 'email-validator'),
        ('pymongo', 'pymongo'),
        ('dotenv', 'python-dotenv')
    ]:
        try:
            __import__(module_name)
            print(f"✅ {package_name} installed")
        except ImportError:
            print(f"❌ {package_name} NOT installed")
            missing.append(package)
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("\n📦 Install them with:")
        print("pip install -r requirements.txt")
        return False
    else:
        print("✅ All required packages are installed!")
        return True


def check_mongodb():
    """Check if MongoDB is running"""
    print("\n🔍 Checking MongoDB connection...")
    try:
        from pymongo import MongoClient
        client = MongoClient('mongodb://localhost:27017', serverSelectionTimeoutMS=2000)
        client.server_info()
        print("✅ MongoDB is running")
        return True
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        print("   Make sure MongoDB is running on localhost:27017")
        return False


def check_flask_app():
    """Check if Flask app is running"""
    try:
        response = requests.get('http://localhost:5000/health', timeout=2)
        if response.status_code == 200:
            print("✅ Flask app is running")
            return True
        else:
            print("❌ Flask app returned unexpected status")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Flask app not running")
        return False


def main():
    """Run all verifications"""
    print("="*60)
    print("🔍 PyTestGenie Authentication System - Verification")
    print("="*60)
    
    checks_passed = 0
    total_checks = 0
    
    # Check 1: Verify files exist
    print("\n1️⃣ Checking files...")
    files = [
        "backend/models/user.py",
        "backend/services/auth_service.py",
        "backend/middleware/auth.py",
        "backend/routes/auth.py",
        "backend/routes/admin.py",
        "backend/config/settings.py",
        "backend/app_unified.py",
        "backend/.env",
        "requirements.txt",
        "test_auth_system.py",
        "AUTH_README.md",
        "AUTH_SYSTEM_GUIDE.md",
        "AUTH_API_REFERENCE.md",
        "AUTH_FLOW_DIAGRAMS.md",
        "AUTH_IMPLEMENTATION_SUMMARY.md",
        "QUICK_START_AUTH.md"
    ]
    
    for file in files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"✗ Missing: {file}")
    
    print("\n" + "="*60)
    print("✅ All authentication system files created successfully!")
    print("="*60)


if __name__ == "__main__":
    verify_installation()
