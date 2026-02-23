# Forgot Password Feature - Setup Guide

## ✨ Features Implemented

1. **Email-based password reset** with 6-digit verification code
2. **Code expiration** - codes expire after 15 minutes
3. **Resend code option** - users can request a new code
4. **3-step recovery process**:
   - Step 1: Enter email address
   - Step 2: Verify code sent to email
   - Step 3: Set new password

## 🔧 Email Configuration

### For Production (Real Email Sending)

Add these environment variables to your `.env` file:

```env
# SMTP Email Configuration
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SENDER_EMAIL=noreply@pytestgenie.com
SENDER_NAME=PyTestGenie
```

#### Using Gmail:

1. Enable 2-Factor Authentication in your Google Account
2. Generate an App Password:
   - Go to Google Account Settings
   - Security → 2-Step Verification → App passwords
   - Generate a password for "Mail"
   - Use this password as `SMTP_PASSWORD`

#### Using Other SMTP Providers:

**SendGrid:**
```env
SMTP_SERVER=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USERNAME=apikey
SMTP_PASSWORD=your-sendgrid-api-key
```

**Mailgun:**
```env
SMTP_SERVER=smtp.mailgun.org
SMTP_PORT=587
SMTP_USERNAME=postmaster@your-domain.mailgun.org
SMTP_PASSWORD=your-mailgun-password
```

**Outlook/Hotmail:**
```env
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USERNAME=your-email@outlook.com
SMTP_PASSWORD=your-password
```

### For Development/Testing

If SMTP is not configured, emails will be **simulated** and printed to the console. This is perfect for development and testing without needing real email setup.

## 🚀 API Endpoints

### 1. Request Password Reset
```
POST /api/auth/forgot-password
Content-Type: application/json

{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "message": "Reset code sent to your email"
}
```

### 2. Verify Reset Code
```
POST /api/auth/verify-reset-code
Content-Type: application/json

{
  "email": "user@example.com",
  "code": "123456"
}
```

**Response:**
```json
{
  "message": "Code verified successfully"
}
```

### 3. Reset Password
```
POST /api/auth/reset-password
Content-Type: application/json

{
  "email": "user@example.com",
  "code": "123456",
  "new_password": "newPassword123"
}
```

**Response:**
```json
{
  "message": "Password reset successful"
}
```

### 4. Resend Reset Code
```
POST /api/auth/resend-reset-code
Content-Type: application/json

{
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "message": "Reset code resent to your email"
}
```

## 📱 Frontend Flow

1. **Login page** now has "Forgot password?" link
2. Click link → **ForgotPassword component** opens
3. User enters email → 6-digit code sent
4. User enters code (with resend option)
5. User sets new password + confirm
6. Success → redirects to login

## 🔒 Security Features

- ✅ Reset codes expire after 15 minutes
- ✅ Codes are stored securely in database
- ✅ Email validation before sending codes
- ✅ Password strength requirements (min 6 characters)
- ✅ Codes cleared after successful password reset
- ✅ Security message if email doesn't exist (doesn't reveal account existence)

## 📁 Files Modified/Created

### Backend:
- ✅ `backend/services/email_service.py` - NEW: Email sending service
- ✅ `backend/models/user.py` - Updated: Password reset methods
- ✅ `backend/services/auth_service.py` - Updated: Reset logic
- ✅ `backend/routes/auth.py` - Updated: New routes for password reset

### Frontend:
- ✅ `frontend/src/components/ForgotPassword.jsx` - NEW: Password recovery UI
- ✅ `frontend/src/components/Login.jsx` - Updated: Forgot password link
- ✅ `frontend/src/services/authService.js` - Updated: API methods

## 🧪 Testing

### Without Email Configuration (Development):
1. Start the backend: `python backend/app_unified.py`
2. Start the frontend: `cd frontend && npm start`
3. Click "Forgot password?" on login page
4. Enter any registered email
5. Check the **backend console** for the simulated email with the code
6. Copy the 6-digit code from console
7. Enter code in the UI
8. Set new password
9. Login with new password

### With Email Configuration (Production):
1. Configure SMTP settings in `.env`
2. Follow the same steps as above
3. Code will be sent to the actual email address

## 📧 Sample Email Template

The password reset email includes:
- Professional HTML design
- Clear 6-digit code display
- Expiration warning (15 minutes)
- Security notice
- PyTestGenie branding

## 🐛 Troubleshooting

**Email not sending:**
- Check SMTP credentials in `.env`
- Verify SMTP port is not blocked by firewall
- For Gmail, ensure App Password is used (not regular password)
- Check backend console for error messages

**Code verification fails:**
- Code may have expired (15 minutes)
- Check if code was typed correctly
- Use resend code option

**Database errors:**
- Ensure MongoDB is running
- Check database connection in backend logs

## 🎯 Next Steps (Optional Enhancements)

1. Add rate limiting to prevent spam
2. Implement CAPTCHA on forgot password page
3. Add password strength indicator
4. Email notification when password is changed
5. Account security logs

---

**Note:** The email service will work in simulation mode without SMTP configuration, making it easy to test during development!
