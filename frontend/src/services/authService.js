// Authentication service for handling login, registration, and token management

const API_BASE = import.meta.env.VITE_API_BASE_URL;

class AuthService {
  // Get token from localStorage
  getToken() {
    return localStorage.getItem('token');
  }

  // Get user info from localStorage
  getUser() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  }

  // Check if user is logged in
  isAuthenticated() {
    return !!this.getToken();
  }

  // Check if user is admin
  isAdmin() {
    const user = this.getUser();
    return user && user.is_admin;
  }

  // Register new user
  async register(username, email, password) {
    try {
      const response = await fetch(`${API_BASE}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, email, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Registration failed');
      }

      return { success: true, data };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  // Login user
  async login(username, password) {
    try {
      const response = await fetch(`${API_BASE}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Login failed');
      }

      // Store token and user info
      localStorage.setItem('token', data.data.token);
      localStorage.setItem('user', JSON.stringify({
        username: data.data.username,
        email: data.data.email,
        is_admin: data.data.is_admin,
      }));

      return { success: true, data: data.data };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  // Logout user
  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  }

  // Get user profile
  async getProfile() {
    try {
      const token = this.getToken();
      if (!token) {
        throw new Error('No token found');
      }

      const response = await fetch(`${API_BASE}/auth/profile`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to get profile');
      }

      return { success: true, data: data.user };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  // Get authorization header
  getAuthHeader() {
    const token = this.getToken();
    return token ? { 'Authorization': `Bearer ${token}` } : {};
  }

  // Admin: Get all users
  async getAllUsers() {
    try {
      const token = this.getToken();
      if (!token) {
        throw new Error('No token found');
      }

      const response = await fetch(`${API_BASE}/admin/users`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to get users');
      }

      return { success: true, data: data.users };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  // Admin: Get pending users
  async getPendingUsers() {
    try {
      const token = this.getToken();
      if (!token) {
        throw new Error('No token found');
      }

      const response = await fetch(`${API_BASE}/admin/users/pending`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to get pending users');
      }

      return { success: true, data: data.users };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  // Admin: Approve user
  async approveUser(username) {
    try {
      const token = this.getToken();
      if (!token) {
        throw new Error('No token found');
      }

      const response = await fetch(`${API_BASE}/admin/users/${username}/approve`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to approve user');
      }

      return { success: true, data };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  // Admin: Delete user
  async deleteUser(username) {
    try {
      const token = this.getToken();
      if (!token) {
        throw new Error('No token found');
      }

      const response = await fetch(`${API_BASE}/admin/users/${username}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to delete user');
      }

      return { success: true, data };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  // Admin: Deactivate user
  async deactivateUser(username) {
    try {
      const token = this.getToken();
      if (!token) {
        throw new Error('No token found');
      }

      const response = await fetch(`${API_BASE}/admin/users/${username}/deactivate`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to deactivate user');
      }

      return { success: true, data };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  // Request password reset code
  async requestPasswordReset(email) {
    try {
      const response = await fetch(`${API_BASE}/auth/forgot-password`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to request password reset');
      }

      return { success: true, message: data.message };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  // Verify reset code
  async verifyResetCode(email, code) {
    try {
      const response = await fetch(`${API_BASE}/auth/verify-reset-code`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, code }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Invalid code');
      }

      return { success: true, message: data.message };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  // Reset password
  async resetPassword(email, code, newPassword) {
    try {
      const response = await fetch(`${API_BASE}/auth/reset-password`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, code, new_password: newPassword }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to reset password');
      }

      return { success: true, message: data.message };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  // Resend reset code
  async resendResetCode(email) {
    try {
      const response = await fetch(`${API_BASE}/auth/resend-reset-code`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to resend code');
      }

      return { success: true, message: data.message };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }
}

export default new AuthService();
