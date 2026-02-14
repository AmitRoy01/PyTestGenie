# 🚀 Quick Start Checklist

## Prerequisites Setup

### 1. Install MongoDB
- [ ] Download MongoDB from https://www.mongodb.com/try/download/community
- [ ] Install MongoDB
- [ ] Start MongoDB service

**Windows:**
```bash
net start MongoDB
```

**Or manually:**
```bash
mongod --dbpath C:\data\db
```

**Verify MongoDB is running:**
```bash
mongo --eval "db.version()"
```

---

## Application Setup

### 2. Install Python Dependencies
```bash
# From project root directory
pip install -r requirements.txt
```

**Verify installation:**
```bash
python -c "import pymongo, jwt, bcrypt; print('All packages installed!')"
```

---

### 3. Start Flask Application
```bash
cd backend
python app_unified.py
```

**Expected output:**
```
* Running on http://0.0.0.0:5000
```

**Verify API is running:**
```bash
curl http://localhost:5000/health
# Should return: {"status":"healthy"}
```

---

## Initial Configuration

### 4. Create Admin User

**Option A: Using Test Script (Recommended)**
```bash
# From project root
python test_auth_system.py
# Select option 1 to create admin
```

**Option B: Using cURL**
```bash
curl -X POST http://localhost:5000/api/admin/create-admin \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"admin\",\"email\":\"admin@example.com\",\"password\":\"admin123\",\"secret\":\"SETUP_SECRET_123\"}"
```

**Expected response:**
```json
{"message": "Admin user created successfully"}
```

---

## Testing

### 5. Test the System

**Option A: Automated Test Suite**
```bash
python test_auth_system.py test
```

**Option B: Interactive Menu**
```bash
python test_auth_system.py
```

**Option C: Manual Testing**

1. **Login as Admin:**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"admin\",\"password\":\"admin123\"}"
```
Save the token from response!

2. **Register a User:**
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"testuser\",\"email\":\"test@example.com\",\"password\":\"test123\"}"
```

3. **Get Pending Users (Admin):**
```bash
curl -X GET http://localhost:5000/api/admin/users/pending \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN_HERE"
```

4. **Approve User (Admin):**
```bash
curl -X PUT http://localhost:5000/api/admin/users/testuser/approve \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN_HERE"
```

5. **Login as User:**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"testuser\",\"password\":\"test123\"}"
```

---

## Verification Checklist

- [ ] MongoDB is running on port 27017
- [ ] All Python packages installed successfully
- [ ] Flask app running on port 5000
- [ ] Health endpoint returns "healthy"
- [ ] Admin user created successfully
- [ ] Can login as admin and receive JWT token
- [ ] Can register new user
- [ ] New user appears in pending users list
- [ ] Can approve user as admin
- [ ] Approved user can login successfully
- [ ] JWT token works for protected endpoints

---

## Common Issues & Solutions

### ❌ "ModuleNotFoundError: No module named 'pymongo'"
**Solution:** Run `pip install -r requirements.txt`

### ❌ "pymongo.errors.ServerSelectionTimeoutError"
**Solution:** Start MongoDB service

### ❌ "Connection refused" when accessing API
**Solution:** Start Flask app with `python backend/app_unified.py`

### ❌ "Username already exists" when creating admin
**Solution:** Admin already created or use different username

### ❌ "Account is pending admin approval" when logging in
**Solution:** Admin must approve user first

---

## Next Steps After Setup

### Development:
- [ ] Read [AUTH_SYSTEM_GUIDE.md](AUTH_SYSTEM_GUIDE.md) for detailed documentation
- [ ] Read [AUTH_API_REFERENCE.md](AUTH_API_REFERENCE.md) for API reference
- [ ] Test all endpoints with Postman or curl
- [ ] Integrate authentication with frontend

### Production:
- [ ] Change SECRET_KEY in .env file
- [ ] Disable/secure create-admin endpoint
- [ ] Enable MongoDB authentication
- [ ] Configure HTTPS
- [ ] Set up proper CORS origins
- [ ] Add rate limiting
- [ ] Implement refresh tokens

---

## Quick Command Reference

### Start Everything:
```bash
# Terminal 1: MongoDB
mongod

# Terminal 2: Flask App
cd backend
python app_unified.py

# Terminal 3: Testing
python test_auth_system.py
```

### Check Status:
```bash
# MongoDB
mongo --eval "db.version()"

# Flask API
curl http://localhost:5000/health

# View users in MongoDB
mongo pyTestGenie --eval "db.users.find().pretty()"
```

---

## 🎉 You're All Set!

If all checkboxes are marked, your authentication system is ready to use!

**Documentation:**
- 📖 [AUTH_IMPLEMENTATION_SUMMARY.md](AUTH_IMPLEMENTATION_SUMMARY.md) - Complete overview
- 📘 [AUTH_SYSTEM_GUIDE.md](AUTH_SYSTEM_GUIDE.md) - Detailed guide
- 📗 [AUTH_API_REFERENCE.md](AUTH_API_REFERENCE.md) - API reference

**Testing:**
- 🧪 `test_auth_system.py` - Interactive testing tool

**Need Help?**
- Check the troubleshooting sections in the documentation
- Review error messages in console/logs
- Verify all services are running

Happy coding! 🚀
