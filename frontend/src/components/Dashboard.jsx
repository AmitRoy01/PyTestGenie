import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import dashboardService from '../services/dashboardService';
import authService from '../services/authService';

// ──────────────────────────────────────────────────────────────────
// Helpers
// ──────────────────────────────────────────────────────────────────
function fmtDate(iso) {
  if (!iso) return '';
  try {
    return new Date(iso).toLocaleDateString(undefined, {
      year: 'numeric', month: 'short', day: 'numeric',
    });
  } catch { return iso; }
}

function stepLabel(step) {
  return {
    source:         '📝 Uploaded',
    test_generated: '🚀 Tests Generated',
    smell_detected: '🔍 Smells Detected',
    refactored:     '🔧 Refactored',
  }[step] || step;
}

// ──────────────────────────────────────────────────────────────────
// Stat Card
// ──────────────────────────────────────────────────────────────────
function StatCard({ icon, label, value, color, onClick, loading }) {
  return (
    <div
      className={`dashboard-stat-card${onClick ? ' clickable' : ''}`}
      style={{ '--card-accent': color }}
      onClick={onClick}
      title={onClick ? `Go to ${label}` : undefined}
    >
      <div className="stat-icon" style={{ color }}>{icon}</div>
      <div className="stat-body">
        <div className="stat-value">
          {loading ? <span className="stat-loading-dot" /> : value ?? '—'}
        </div>
        <div className="stat-label">{label}</div>
      </div>
    </div>
  );
}

// ──────────────────────────────────────────────────────────────────
// Dashboard
// ──────────────────────────────────────────────────────────────────
export default function Dashboard() {
  const navigate  = useNavigate();
  const user      = authService.getUser();

  // ── stats state ──────────────────────────────────────────────
  const [stats,        setStats]        = useState(null);
  const [statsLoading, setStatsLoading] = useState(true);
  const [statsError,   setStatsError]   = useState('');

  // ── password-change state ─────────────────────────────────────
  const [currentPw,  setCurrentPw]  = useState('');
  const [newPw,      setNewPw]      = useState('');
  const [confirmPw,  setConfirmPw]  = useState('');
  const [pwLoading,  setPwLoading]  = useState(false);
  const [pwError,    setPwError]    = useState('');
  const [pwSuccess,  setPwSuccess]  = useState('');

  // ── load stats ────────────────────────────────────────────────
  const loadStats = useCallback(async () => {
    setStatsLoading(true);
    setStatsError('');
    try {
      const data = await dashboardService.getStats();
      setStats(data);
    } catch (err) {
      setStatsError(err?.response?.data?.error || 'Failed to load stats');
    } finally {
      setStatsLoading(false);
    }
  }, []);

  useEffect(() => { loadStats(); }, [loadStats]);

  // ── password change handler ───────────────────────────────────
  const handlePasswordChange = async (e) => {
    e.preventDefault();
    setPwError('');
    setPwSuccess('');

    if (!currentPw.trim() || !newPw.trim() || !confirmPw.trim()) {
      setPwError('Please fill in all password fields.');
      return;
    }
    if (newPw !== confirmPw) {
      setPwError('New password and confirmation do not match.');
      return;
    }
    if (newPw.length < 6) {
      setPwError('New password must be at least 6 characters.');
      return;
    }
    if (newPw === currentPw) {
      setPwError('New password must differ from the current password.');
      return;
    }

    setPwLoading(true);
    try {
      const res = await dashboardService.changePassword(currentPw, newPw);
      setPwSuccess(res.message || 'Password changed successfully!');
      setCurrentPw('');
      setNewPw('');
      setConfirmPw('');
    } catch (err) {
      setPwError(err?.response?.data?.error || 'Failed to change password.');
    } finally {
      setPwLoading(false);
    }
  };

  // ── today's greeting ─────────────────────────────────────────
  const greeting = () => {
    const h = new Date().getHours();
    if (h < 12) return '🌤️ Good morning';
    if (h < 17) return '☀️ Good afternoon';
    return '🌙 Good evening';
  };

  const today = new Date().toLocaleDateString(undefined, {
    weekday: 'long', year: 'numeric', month: 'long', day: 'numeric',
  });

  // ──────────────────────────────────────────────────────────────
  return (
    <div className="dashboard">

      {/* ── Welcome Banner ───────────────────────────────────── */}
      <div className="dashboard-welcome">
        <div className="welcome-left">
          <h2>{greeting()}, <span className="welcome-name">{user?.username || 'there'}</span>! 👋</h2>
          <p className="welcome-date">{today}</p>
        </div>
        <button className="dashboard-refresh-btn" onClick={loadStats} title="Refresh stats">
          🔄 Refresh
        </button>
      </div>

      {/* ── Stats Error ──────────────────────────────────────── */}
      {statsError && (
        <div className="dashboard-error-banner">{statsError}</div>
      )}

      {/* ── Quick Stats ──────────────────────────────────────── */}
      <section className="dashboard-section">
        <h3 className="dashboard-section-title">📊 Quick Stats</h3>
        <div className="dashboard-stat-grid">
          <StatCard
            icon="📂" label="Saved Projects"
            value={stats?.saved_projects}
            color="#4f86f7"
            loading={statsLoading}
            onClick={() => navigate('/history')}
          />
          <StatCard
            icon="📋" label="Saved Reports"
            value={stats?.saved_reports}
            color="#7c5cbf"
            loading={statsLoading}
            onClick={() => navigate('/reports')}
          />
          <StatCard
            icon="🔍" label="Total Smells Detected"
            value={stats?.total_smells}
            color="#e8a020"
            loading={statsLoading}
            onClick={() => navigate('/detector')}
          />
          <StatCard
            icon="🔧" label="Total Refactorings Done"
            value={stats?.total_refactorings}
            color="#27ae60"
            loading={statsLoading}
            onClick={() => navigate('/refactorer')}
          />
        </div>
      </section>

      {/* ── Quick Actions ─────────────────────────────────────── */}
      <section className="dashboard-section">
        <h3 className="dashboard-section-title">⚡ Quick Actions</h3>
        <div className="dashboard-actions-grid">
          <button className="dashboard-action-btn action-generate"
            onClick={() => navigate('/generator')}>
            <span className="action-icon">🚀</span>
            <span className="action-label">Generate Tests</span>
          </button>
          <button className="dashboard-action-btn action-detect"
            onClick={() => navigate('/detector')}>
            <span className="action-icon">🔍</span>
            <span className="action-label">Detect Smells</span>
          </button>
          <button className="dashboard-action-btn action-refactor"
            onClick={() => navigate('/refactorer')}>
            <span className="action-icon">🔧</span>
            <span className="action-label">Refactor Tests</span>
          </button>
          <button className="dashboard-action-btn action-reports"
            onClick={() => navigate('/reports')}>
            <span className="action-icon">📋</span>
            <span className="action-label">View Reports</span>
          </button>
        </div>
      </section>

      {/* ── Recent Activity ───────────────────────────────────── */}
      {stats?.recent_activity?.length > 0 && (
        <section className="dashboard-section">
          <h3 className="dashboard-section-title">🕐 Recent Activity</h3>
          <div className="dashboard-activity-list">
            {stats.recent_activity.map((item) => (
              <div key={item.id} className={`activity-item activity-${item.kind}`}>
                <span className="activity-kind-icon">
                  {item.kind === 'report' ? '📋' : '📂'}
                </span>
                <span className="activity-title">{item.title}</span>
                {item.step && (
                  <span className="activity-step">{stepLabel(item.step)}</span>
                )}
                <span className="activity-date">{fmtDate(item.date)}</span>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* ── Profile Section ───────────────────────────────────── */}
      <section className="dashboard-section dashboard-profile">
        <h3 className="dashboard-section-title">👤 Profile</h3>
        <div className="profile-inner">

          {/* Read-only info */}
          <div className="profile-info-card">
            <div className="profile-field">
              <label>Username</label>
              <div className="profile-value">
                {user?.username}
                {user?.is_admin && <span className="admin-badge-small">👑 Admin</span>}
              </div>
            </div>
          </div>

          {/* Password change */}
          <div className="profile-pw-card">
            <h4>🔑 Change Password</h4>
            <form onSubmit={handlePasswordChange} className="pw-form" autoComplete="off">
              <div className="pw-field">
                <label htmlFor="cur-pw">Current Password</label>
                <input
                  id="cur-pw"
                  type="password"
                  placeholder="Enter current password"
                  value={currentPw}
                  onChange={e => setCurrentPw(e.target.value)}
                  autoComplete="current-password"
                />
              </div>
              <div className="pw-field">
                <label htmlFor="new-pw">New Password</label>
                <input
                  id="new-pw"
                  type="password"
                  placeholder="At least 6 characters"
                  value={newPw}
                  onChange={e => setNewPw(e.target.value)}
                  autoComplete="new-password"
                />
              </div>
              <div className="pw-field">
                <label htmlFor="confirm-pw">Confirm New Password</label>
                <input
                  id="confirm-pw"
                  type="password"
                  placeholder="Repeat new password"
                  value={confirmPw}
                  onChange={e => setConfirmPw(e.target.value)}
                  autoComplete="new-password"
                />
              </div>

              {pwError   && <div className="pw-msg pw-error">❌ {pwError}</div>}
              {pwSuccess && <div className="pw-msg pw-success">✅ {pwSuccess}</div>}

              <button
                type="submit"
                className="pw-submit-btn"
                disabled={pwLoading}
              >
                {pwLoading ? '⏳ Saving…' : '🔑 Change Password'}
              </button>
            </form>
          </div>

        </div>
      </section>

    </div>
  );
}
