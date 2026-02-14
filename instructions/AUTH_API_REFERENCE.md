# Authentication API Quick Reference

## Base URL
```
http://localhost:5000/api
```

## Authentication Flow

### 1️⃣ User Registration Flow
```
User Registers → is_approved=false → Admin Approves → User Can Login
```

### 2️⃣ Login Flow
```
User Login → Verify Credentials → Check is_approved && is_active → Generate JWT Token
```

## Quick API Reference

### 🔓 Public Endpoints (No Auth Required)

#### Register User
```bash
POST /api/auth/register
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

#### Login
```bash
POST /api/auth/login
{
  "username": "string",
  "password": "string"
}
# Returns: { "data": { "token": "JWT_TOKEN", ... } }
```

#### Create Admin (Setup Only)
```bash
POST /api/admin/create-admin
{
  "username": "admin",
  "email": "admin@example.com",
  "password": "admin123",
  "secret": "SETUP_SECRET_123"
}
```

---

### 🔐 Protected Endpoints (Requires Auth Token)

**Header Required:** `Authorization: Bearer <JWT_TOKEN>`

#### Get Profile
```bash
GET /api/auth/profile
```

#### Verify Token
```bash
GET /api/auth/verify-token
```

---

### 👨‍💼 Admin Endpoints (Requires Admin Token)

**Header Required:** `Authorization: Bearer <ADMIN_JWT_TOKEN>`

#### Get All Users
```bash
GET /api/admin/users?include_inactive=true
```

#### Get Pending Users
```bash
GET /api/admin/users/pending
```

#### Get User Details
```bash
GET /api/admin/users/<username>
```

#### Add User
```bash
POST /api/admin/users
{
  "username": "string",
  "email": "string",
  "password": "string",
  "is_admin": false,
  "is_approved": true
}
```

#### Approve User
```bash
PUT /api/admin/users/<username>/approve
```

#### Unapprove User
```bash
PUT /api/admin/users/<username>/unapprove
```

#### Activate User
```bash
PUT /api/admin/users/<username>/activate
```

#### Deactivate User
```bash
PUT /api/admin/users/<username>/deactivate
```

#### Delete User
```bash
DELETE /api/admin/users/<username>
```

---

## Response Formats

### Success Response (200/201)
```json
{
  "message": "Success message",
  "data": { ... },
  "user": { ... }
}
```

### Error Response (400/401/403/500)
```json
{
  "error": "Error message"
}
```

---

## Common Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized (invalid/missing token) |
| 403 | Forbidden (insufficient privileges) |
| 404 | Not Found |
| 500 | Internal Server Error |

---

## User Status Fields

| Field | Type | Description |
|-------|------|-------------|
| `is_approved` | boolean | User approved by admin (can login) |
| `is_active` | boolean | Account is active (not deactivated) |
| `is_admin` | boolean | Has admin privileges |

### Login Requirements
User can login ONLY if:
- ✅ `is_approved = true`
- ✅ `is_active = true`
- ✅ Correct password

---

## Testing Commands

### 1. Create Admin
```bash
curl -X POST http://localhost:5000/api/admin/create-admin \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","email":"admin@example.com","password":"admin123","secret":"SETUP_SECRET_123"}'
```

### 2. Login as Admin
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```
💾 Save the token!

### 3. Register User
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"john","email":"john@example.com","password":"password123"}'
```

### 4. Get Pending Users (Admin)
```bash
curl -X GET http://localhost:5000/api/admin/users/pending \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"
```

### 5. Approve User (Admin)
```bash
curl -X PUT http://localhost:5000/api/admin/users/john/approve \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"
```

### 6. Login as User
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"password123"}'
```

### 7. Get Profile (User)
```bash
curl -X GET http://localhost:5000/api/auth/profile \
  -H "Authorization: Bearer YOUR_USER_TOKEN"
```

---

## Python Testing Script

Run interactive testing:
```bash
python test_auth_system.py
```

Run automated test suite:
```bash
python test_auth_system.py test
```

---

## MongoDB Queries

### View all users
```javascript
mongo
use pyTestGenie
db.users.find().pretty()
```

### Count users
```javascript
db.users.count()
```

### Find specific user
```javascript
db.users.findOne({username: "admin"})
```

### Delete all users (dev only)
```javascript
db.users.drop()
```

---

## JWT Token Structure

### Payload:
```json
{
  "username": "string",
  "exp": "timestamp",
  "iat": "timestamp"
}
```

### Token Format in Header:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## Environment Variables

```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=pyTestGenie
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## Common Errors

### "Token is missing"
- Add Authorization header: `Bearer <token>`

### "Account is pending admin approval"
- Admin must approve user first

### "Invalid username or password"
- Check credentials

### "Admin privileges required"
- Use admin token, not regular user token

### "Token has expired"
- Login again (default: 30 min expiry)

---

## File Structure

```
backend/
├── models/user.py           # MongoDB user model
├── services/auth_service.py # Password & token handling
├── middleware/auth.py       # JWT verification decorators
├── routes/auth.py           # Auth endpoints
├── routes/admin.py          # Admin endpoints
├── config/settings.py       # Configuration
└── app_unified.py           # Main app with routes
```

---

## Next Steps

1. ✅ Install dependencies
2. ✅ Start MongoDB
3. ✅ Start Flask app
4. ✅ Create admin user
5. ✅ Test with curl or test script
6. 🔄 Integrate with frontend
7. 🔄 Add password reset
8. 🔄 Add email verification
9. 🔄 Deploy to production
