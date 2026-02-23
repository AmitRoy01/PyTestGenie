import React, { useState } from 'react';
import authService from '../services/authService';
import '../App.css';

function ForgotPassword({ onBackToLogin }) {
  const [step, setStep] = useState(1); // 1: email, 2: code, 3: new password
  const [email, setEmail] = useState('');
  const [code, setCode] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ text: '', type: '' });

  const handleSendCode = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage({ text: '', type: '' });

    const result = await authService.requestPasswordReset(email);
    setLoading(false);

    if (result.success) {
      setMessage({ text: result.message, type: 'success' });
      setTimeout(() => {
        setStep(2);
        setMessage({ text: '', type: '' });
      }, 1500);
    } else {
      setMessage({ text: result.error, type: 'error' });
    }
  };

  const handleResendCode = async () => {
    setLoading(true);
    setMessage({ text: '', type: '' });

    const result = await authService.resendResetCode(email);
    setLoading(false);

    if (result.success) {
      setMessage({ text: 'Code resent to your email!', type: 'success' });
    } else {
      setMessage({ text: result.error, type: 'error' });
    }
  };

  const handleVerifyCode = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage({ text: '', type: '' });

    const result = await authService.verifyResetCode(email, code);
    setLoading(false);

    if (result.success) {
      setMessage({ text: 'Code verified!', type: 'success' });
      setTimeout(() => {
        setStep(3);
        setMessage({ text: '', type: '' });
      }, 1000);
    } else {
      setMessage({ text: result.error, type: 'error' });
    }
  };

  const handleResetPassword = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage({ text: '', type: '' });

    if (newPassword !== confirmPassword) {
      setMessage({ text: 'Passwords do not match', type: 'error' });
      setLoading(false);
      return;
    }

    if (newPassword.length < 6) {
      setMessage({ text: 'Password must be at least 6 characters', type: 'error' });
      setLoading(false);
      return;
    }

    const result = await authService.resetPassword(email, code, newPassword);
    setLoading(false);

    if (result.success) {
      setMessage({ text: 'Password reset successful! Redirecting to login...', type: 'success' });
      setTimeout(() => {
        onBackToLogin();
      }, 2000);
    } else {
      setMessage({ text: result.error, type: 'error' });
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <h1>🔐 Password Recovery</h1>
          <p>Reset your PyTestGenie account password</p>
        </div>

        {/* Step 1: Enter Email */}
        {step === 1 && (
          <form onSubmit={handleSendCode} className="login-form">
            <div className="form-group">
              <label>Email Address</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter your registered email"
                required
              />
              <small style={{ color: '#666', fontSize: '12px', marginTop: '5px', display: 'block' }}>
                We'll send a 6-digit verification code to this email
              </small>
            </div>

            {message.text && (
              <div className={`message ${message.type}`}>
                {message.text}
              </div>
            )}

            <button type="submit" className="login-button" disabled={loading}>
              {loading ? '⏳ Sending...' : '📧 Send Reset Code'}
            </button>
          </form>
        )}

        {/* Step 2: Enter Code */}
        {step === 2 && (
          <form onSubmit={handleVerifyCode} className="login-form">
            <div className="form-group">
              <label>Verification Code</label>
              <input
                type="text"
                value={code}
                onChange={(e) => setCode(e.target.value)}
                placeholder="Enter 6-digit code"
                required
                maxLength={6}
                style={{ fontSize: '20px', letterSpacing: '5px', textAlign: 'center' }}
              />
              <small style={{ color: '#666', fontSize: '12px', marginTop: '5px', display: 'block' }}>
                Check your email ({email}) for the code
              </small>
            </div>

            {message.text && (
              <div className={`message ${message.type}`}>
                {message.text}
              </div>
            )}

            <button type="submit" className="login-button" disabled={loading}>
              {loading ? '⏳ Verifying...' : '✅ Verify Code'}
            </button>

            <div style={{ textAlign: 'center', marginTop: '15px' }}>
              <button
                type="button"
                className="link-button"
                onClick={handleResendCode}
                disabled={loading}
              >
                🔄 Resend Code
              </button>
            </div>
          </form>
        )}

        {/* Step 3: New Password */}
        {step === 3 && (
          <form onSubmit={handleResetPassword} className="login-form">
            <div className="form-group">
              <label>New Password</label>
              <input
                type="password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                placeholder="Enter new password"
                required
                minLength={6}
              />
            </div>

            <div className="form-group">
              <label>Confirm Password</label>
              <input
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="Confirm new password"
                required
                minLength={6}
              />
            </div>

            {message.text && (
              <div className={`message ${message.type}`}>
                {message.text}
              </div>
            )}

            <button type="submit" className="login-button" disabled={loading}>
              {loading ? '⏳ Resetting...' : '🔒 Reset Password'}
            </button>
          </form>
        )}

        <div className="login-footer">
          <p>
            <button
              className="link-button"
              onClick={onBackToLogin}
            >
              ← Back to Login
            </button>
          </p>
        </div>
      </div>
    </div>
  );
}

export default ForgotPassword;
