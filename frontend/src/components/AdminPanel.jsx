import React, { useState, useEffect } from 'react';
import authService from '../services/authService';

function AdminPanel() {
  const [users, setUsers] = useState([]);
  const [pendingUsers, setPendingUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('pending');
  const [message, setMessage] = useState({ text: '', type: '' });

  useEffect(() => {
    loadUsers();
  }, [activeTab]);

  const loadUsers = async () => {
    setLoading(true);
    
    if (activeTab === 'pending') {
      const result = await authService.getPendingUsers();
      if (result.success) {
        setPendingUsers(result.data);
      } else {
        setMessage({ text: result.error, type: 'error' });
      }
    } else {
      const result = await authService.getAllUsers();
      if (result.success) {
        setUsers(result.data);
      } else {
        setMessage({ text: result.error, type: 'error' });
      }
    }
    
    setLoading(false);
  };

  const handleApprove = async (username) => {
    const result = await authService.approveUser(username);
    if (result.success) {
      setMessage({ text: `User ${username} approved successfully!`, type: 'success' });
      loadUsers();
    } else {
      setMessage({ text: result.error, type: 'error' });
    }
  };

  const handleDelete = async (username) => {
    if (!window.confirm(`Are you sure you want to delete user "${username}"?`)) {
      return;
    }

    const result = await authService.deleteUser(username);
    if (result.success) {
      setMessage({ text: `User ${username} deleted successfully!`, type: 'success' });
      loadUsers();
    } else {
      setMessage({ text: result.error, type: 'error' });
    }
  };

  const handleDeactivate = async (username) => {
    const result = await authService.deactivateUser(username);
    if (result.success) {
      setMessage({ text: `User ${username} deactivated successfully!`, type: 'success' });
      loadUsers();
    } else {
      setMessage({ text: result.error, type: 'error' });
    }
  };

  return (
    <div className="admin-panel">
      <h2>👨‍💼 Admin Panel</h2>
      <p className="admin-subtitle">Manage users and approvals</p>

      <div className="admin-tabs">
        <button
          className={`admin-tab ${activeTab === 'pending' ? 'active' : ''}`}
          onClick={() => setActiveTab('pending')}
        >
          ⏳ Pending Approvals ({pendingUsers.length})
        </button>
        <button
          className={`admin-tab ${activeTab === 'all' ? 'active' : ''}`}
          onClick={() => setActiveTab('all')}
        >
          👥 All Users ({users.length})
        </button>
      </div>

      {message.text && (
        <div className={`message ${message.type}`}>
          {message.text}
          <button onClick={() => setMessage({ text: '', type: '' })}>✕</button>
        </div>
      )}

      {loading ? (
        <div className="loading-state">
          <div className="spinner"></div>
          <p>Loading users...</p>
        </div>
      ) : (
        <div className="users-list">
          {activeTab === 'pending' && pendingUsers.length === 0 && (
            <div className="empty-state">
              <p>✅ No pending approvals</p>
            </div>
          )}

          {activeTab === 'all' && users.length === 0 && (
            <div className="empty-state">
              <p>No users found</p>
            </div>
          )}

          {activeTab === 'pending' &&
            pendingUsers.map((user) => (
              <div key={user.username} className="user-card pending">
                <div className="user-info">
                  <h3>{user.username}</h3>
                  <p className="user-email">{user.email}</p>
                  <span className="user-badge pending">⏳ Pending Approval</span>
                </div>
                <div className="user-actions">
                  <button
                    className="btn-approve"
                    onClick={() => handleApprove(user.username)}
                  >
                    ✓ Approve
                  </button>
                  <button
                    className="btn-delete"
                    onClick={() => handleDelete(user.username)}
                  >
                    ✕ Reject
                  </button>
                </div>
              </div>
            ))}

          {activeTab === 'all' &&
            users.map((user) => (
              <div key={user.username} className="user-card">
                <div className="user-info">
                  <h3>
                    {user.username}
                    {user.is_admin && <span className="admin-badge">👑 Admin</span>}
                  </h3>
                  <p className="user-email">{user.email}</p>
                  <div className="user-status">
                    <span className={`user-badge ${user.is_approved ? 'approved' : 'pending'}`}>
                      {user.is_approved ? '✓ Approved' : '⏳ Pending'}
                    </span>
                    <span className={`user-badge ${user.is_active ? 'active' : 'inactive'}`}>
                      {user.is_active ? '🟢 Active' : '🔴 Inactive'}
                    </span>
                  </div>
                </div>
                <div className="user-actions">
                  {!user.is_admin && (
                    <>
                      {user.is_active ? (
                        <button
                          className="btn-deactivate"
                          onClick={() => handleDeactivate(user.username)}
                        >
                          🔒 Deactivate
                        </button>
                      ) : (
                        <button
                          className="btn-approve"
                          onClick={() => handleApprove(user.username)}
                        >
                          🔓 Activate
                        </button>
                      )}
                      <button
                        className="btn-delete"
                        onClick={() => handleDelete(user.username)}
                      >
                        🗑️ Delete
                      </button>
                    </>
                  )}
                </div>
              </div>
            ))}
        </div>
      )}

      <button className="btn-refresh" onClick={loadUsers}>
        🔄 Refresh
      </button>
    </div>
  );
}

export default AdminPanel;
