# 🔐 Forgot Password Feature - Quick Start

## ✅ Installation Complete!

The forgot password feature has been successfully added to your PyTestGenie project.

## 🚀 How to Use (For Testing Without Email Setup)

### 1. Start the Backend
```bash
python backend/app_unified.py
```

### 2. Start the Frontend
```bash
cd frontend
npm start
```

### 3. Test the Feature

1. Go to the login page
2. Click on **"Forgot password?"** link
3. Enter a registered email address
4. **Check the backend console** - you'll see the reset code printed there (since SMTP is not configured yet)
5. Copy the 6-digit code from the console
6. Enter the code in the UI
7. Set your new password
8. Login with your new credentials! ✨

## 📧 To Enable Real Email Sending

1. Copy `.env.example` to `.env` if you haven't already
2. Add your SMTP credentials to `.env`:
   ```env
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USERNAME=your-email@gmail.com
   SMTP_PASSWORD=your-app-password
   ```

3. For Gmail, you need an App Password:
   - Enable 2-Factor Authentication
   - Go to: https://myaccount.google.com/apppasswords
   - Generate an app password
   - Use that as `SMTP_PASSWORD`

4. Restart the backend

See `instructions/FORGOT_PASSWORD_SETUP.md` for detailed configuration options.

## 🔒 Security Features

- ✅ 6-digit verification codes
- ✅ Codes expire after 15 minutes
- ✅ Secure password hashing (bcrypt)
- ✅ Email validation
- ✅ Resend code option
- ✅ Password confirmation check

## 📁 New Files Added

**Backend:**
- `backend/services/email_service.py` - Email sending service
- Updated `backend/models/user.py` - Password reset database operations
- Updated `backend/services/auth_service.py` - Password reset logic
- Updated `backend/routes/auth.py` - New API endpoints

**Frontend:**
- `frontend/src/components/ForgotPassword.jsx` - Password recovery UI
- Updated `frontend/src/components/Login.jsx` - Added forgot password link
- Updated `frontend/src/services/authService.js` - API integration

**Documentation:**
- `instructions/FORGOT_PASSWORD_SETUP.md` - Complete setup guide
- `test_forgot_password.py` - Verification test script

## 🎯 Flow Diagram

```
Login Page
    ↓
Click "Forgot password?"
    ↓
Enter Email → Code sent to email (or console in dev mode)
    ↓
Enter 6-digit Code (with resend option)
    ↓
Set New Password + Confirm
    ↓
Success! → Back to Login
    ↓
Login with New Password ✅
```

## 🧪 Test Status

All tests passed! ✅
- Email service: ✓ Working (simulation mode)
- User model methods: ✓ All present
- Auth service methods: ✓ All present
- Routes: ✓ Loaded successfully

## 💡 Tips

- **Development Mode**: Emails are printed to console - perfect for testing!
- **Production Mode**: Configure SMTP to send real emails
- **Code Expiration**: Codes automatically expire after 15 minutes
- **Resend Option**: Users can request a new code if needed
- **Security**: The system doesn't reveal if an email exists (security best practice)

---

**Ready to test!** Just start the backend and frontend, then try the forgot password flow.

For any issues, check `instructions/FORGOT_PASSWORD_SETUP.md` for troubleshooting.
