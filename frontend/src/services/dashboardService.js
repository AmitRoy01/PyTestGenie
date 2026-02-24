import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'https://pytestgenie.onrender.com/api';

function authHeader() {
  const token = localStorage.getItem('token');
  return token ? { Authorization: `Bearer ${token}` } : {};
}

const dashboardService = {
  /** Fetch the 4 stat counts + recent activity for the current user. */
  async getStats() {
    const res = await axios.get(`${API_BASE}/dashboard/stats`, {
      headers: authHeader(),
    });
    return res.data;
  },

  /**
   * Change the current user's password.
   * @param {string} currentPassword
   * @param {string} newPassword
   */
  async changePassword(currentPassword, newPassword) {
    const res = await axios.put(
      `${API_BASE}/dashboard/change-password`,
      { current_password: currentPassword, new_password: newPassword },
      { headers: authHeader() }
    );
    return res.data;
  },
};

export default dashboardService;
