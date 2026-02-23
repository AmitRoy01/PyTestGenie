import React, { useState } from 'react';
import authService from '../services/authService';
import ForgotPassword from './ForgotPassword';
import '../App.css';

function Login({ onLoginSuccess }) {
  const [isLogin, setIsLogin] = useState(true);
  const [showForgotPassword, setShowForgotPassword] = useState(false);
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState({ text: '', type: '' });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage({ text: '', type: '' });

    if (isLogin) {
      // Login
      const result = await authService.login(username, password);
      setLoading(false);

      if (result.success) {
        setMessage({ text: 'Login successful!', type: 'success' });
        setTimeout(() => {
          onLoginSuccess();
        }, 500);
      } else {
        setMessage({ text: result.error, type: 'error' });
      }
    } else {
      // Register
      if (!email) {
        setMessage({ text: 'Email is required', type: 'error' });
        setLoading(false);
        return;
      }

      const result = await authService.register(username, email, password);
      setLoading(false);

      if (result.success) {
        setMessage({ 
          text: 'Registration successful! Please wait for admin approval before logging in.', 
          type: 'success' 
        });
        // Switch to login after 3 seconds
        setTimeout(() => {
          setIsLogin(true);
          setMessage({ text: '', type: '' });
        }, 3000);
      } else {
        setMessage({ text: result.error, type: 'error' });
      }
    }
  };

  // Show forgot password component
  if (showForgotPassword) {
    return <ForgotPassword onBackToLogin={() => setShowForgotPassword(false)} />;
  }

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <h1>🧪 PyTestGenie</h1>
          <p>Automated Test Generation & Smell Detection</p>
        </div>

        <div className="login-tabs">
          <button
            className={`login-tab ${isLogin ? 'active' : ''}`}
            onClick={() => {
              setIsLogin(true);
              setMessage({ text: '', type: '' });
            }}
          >
            Login
          </button>
          <button
            className={`login-tab ${!isLogin ? 'active' : ''}`}
            onClick={() => {
              setIsLogin(false);
              setMessage({ text: '', type: '' });
            }}
          >
            Register
          </button>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label>Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter username"
              required
              minLength={3}
            />
          </div>

          {!isLogin && (
            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter email"
                required
              />
            </div>
          )}

          <div className="form-group">
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter password"
              required
              minLength={6}
            />
          </div>

          {isLogin && (
            <div style={{ textAlign: 'right', marginTop: '-10px', marginBottom: '15px' }}>
              <button
                type="button"
                className="link-button"
                onClick={() => setShowForgotPassword(true)}
                style={{ fontSize: '13px', color: '#667eea' }}
              >
                Forgot password?
              </button>
            </div>
          )}

          {message.text && (
            <div className={`message ${message.type}`}>
              {message.text}
            </div>
          )}

          <button type="submit" className="login-button" disabled={loading}>
            {loading ? '⏳ Please wait...' : isLogin ? '🔐 Login' : '📝 Register'}
          </button>
        </form>

        <div className="login-footer">
          <p>
            {isLogin ? "Don't have an account? " : 'Already have an account? '}
            <button
              className="link-button"
              onClick={() => {
                setIsLogin(!isLogin);
                setMessage({ text: '', type: '' });
              }}
            >
              {isLogin ? 'Register here' : 'Login here'}
            </button>
          </p>
        </div>
      </div>
    </div>
  );
}

export default Login;
