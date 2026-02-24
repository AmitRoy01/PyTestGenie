import React, { useState, useEffect } from "react";
import axios from "axios";
import {
  BrowserRouter, Routes, Route, NavLink,
  Navigate, useNavigate, useLocation,
} from "react-router-dom";
import TestGenerator  from "./components/TestGenerator";
import SmellDetector  from "./components/SmellDetector";
import TestRefactorer from "./components/TestRefactorer";
import Login          from "./components/Login";
import AdminPanel     from "./components/AdminPanel";
import ProjectHistory from "./components/ProjectHistory";
import authService    from "./services/authService";
import "./App.css";
import logoUrl       from "./assets/pyTestGenieLogo.png";
import genieImageUrl from "./assets/pyTestGenie.png";
import genieSoundUrl from "./assets/ginie_sound.mp3";

// ── Page wrappers (read location.state so components get initialData) ──────
function GeneratorPage()  {
  const { state } = useLocation();
  return <TestGenerator  key={state?.loadKey} initialData={state?.initialData} />;
}
function DetectorPage() {
  const { state } = useLocation();
  return <SmellDetector  key={state?.loadKey} initialData={state?.initialData} />;
}
function RefactorerPage() {
  const { state } = useLocation();
  return <TestRefactorer key={state?.loadKey} initialData={state?.initialData} />;
}

// ── Auth guards ────────────────────────────────────────────────────────────
function RequireAuth({ children }) {
  return authService.getToken() ? children : <Navigate to="/login" replace />;
}
function RequireAdmin({ children }) {
  const user = authService.getUser();
  if (!authService.getToken()) return <Navigate to="/login" replace />;
  if (!user?.is_admin)         return <Navigate to="/"      replace />;
  return children;
}

// ── Shared layout (header + nav + footer wrapping all authed pages) ────────
function Layout({ user, onLogout }) {
  const navigate = useNavigate();

  const handleLoadVersion = (versionData) => {
    const route = {
      source:         '/generator',
      test_generated: '/generator',
      smell_detected: '/detector',
      refactored:     '/refactorer',
    }[versionData.step] || '/generator';
    navigate(route, { state: { initialData: versionData, loadKey: Date.now() } });
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="header-content">
          <div className="header-title">
            <div className="header-title-row">
              <img src={logoUrl} alt="PyTestGenie Logo" className="app-logo" />
              <h1>PyTestGenie</h1>
            </div>
            <p>Automated Test Generation, Smell Detection &amp; Refactoring</p>
          </div>
          <div className="header-user">
            <span className="user-name">
              👤 {user?.username}
              {user?.is_admin && <span className="admin-badge-small">👑</span>}
            </span>
            <button className="logout-button" onClick={onLogout}>
              🚪 Logout
            </button>
          </div>
        </div>
      </header>

      <nav className="tab-navigation">
        <NavLink to="/generator"
          className={({ isActive }) => `tab-button${isActive ? " active" : ""}`}>
          <span className="tab-icon">🚀</span>Test Code Generator
        </NavLink>
        <NavLink to="/detector"
          className={({ isActive }) => `tab-button${isActive ? " active" : ""}`}>
          <span className="tab-icon">🔍</span>Test Smell Detector
        </NavLink>
        <NavLink to="/refactorer"
          className={({ isActive }) => `tab-button${isActive ? " active" : ""}`}>
          <span className="tab-icon">🔧</span>Test Code Refactorer
        </NavLink>
        {user?.is_admin && (
          <NavLink to="/admin"
            className={({ isActive }) => `tab-button${isActive ? " active" : ""}`}>
            <span className="tab-icon">👨‍💼</span>Admin Panel
          </NavLink>
        )}
        <NavLink to="/history"
          className={({ isActive }) => `tab-button${isActive ? " active" : ""}`}>
          <span className="tab-icon">📂</span>My Projects
        </NavLink>
      </nav>

      <main className="main-content">
        <Routes>
          <Route path="/"           element={<Navigate to="/generator" replace />} />
          <Route path="/generator"  element={<GeneratorPage />} />
          <Route path="/detector"   element={<DetectorPage />} />
          <Route path="/refactorer" element={<RefactorerPage />} />
          <Route path="/admin"      element={<RequireAdmin><AdminPanel /></RequireAdmin>} />
          <Route path="/history"    element={<ProjectHistory onLoadVersion={handleLoadVersion} />} />
          <Route path="*"           element={<Navigate to="/generator" replace />} />
        </Routes>
      </main>

      <footer className="app-footer">
        <p>PyTestGenie - Complete Testing Pipeline | Logged in as {user?.username}</p>
      </footer>
    </div>
  );
}


// ── Root entry point ──────────────────────────────────────────────────────
function AppInner() {
  // Initialise synchronously from localStorage so refresh preserves the current URL
  const [isAuthenticated, setIsAuthenticated] = useState(() => !!authService.getToken());
  const [user, setUser]                       = useState(() => authService.getUser());
  const [showGenie, setShowGenie]             = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    if (!showGenie) return;
    const audio = new Audio(genieSoundUrl);
    audio.volume = 0.9;
    audio.play().catch(() => {});
    const timer = setTimeout(() => setShowGenie(false), 4000);
    return () => { clearTimeout(timer); audio.pause(); };
  }, [showGenie]);

  // Global 401 interceptor — auto-logout when token expires
  useEffect(() => {
    const interceptor = axios.interceptors.response.use(
      res => res,
      err => {
        if (err?.response?.status === 401 && isAuthenticated) {
          authService.logout();
          setIsAuthenticated(false);
          setUser(null);
          navigate('/login', { replace: true });
          alert('Your session has expired. Please log in again.');
        }
        return Promise.reject(err);
      }
    );
    return () => axios.interceptors.response.eject(interceptor);
  }, [isAuthenticated, navigate]);

  const handleLoginSuccess = () => {
    setIsAuthenticated(true);
    setUser(authService.getUser());
    setShowGenie(true);
    navigate('/generator', { replace: true });
  };

  const handleLogout = () => {
    authService.logout();
    setIsAuthenticated(false);
    setUser(null);
    navigate('/login', { replace: true });
  };

  return (
    <>
      {showGenie && (
        <div className="genie-overlay">
          <img src={genieImageUrl} alt="PyTestGenie" className="genie-image" />
          <div className="genie-message">Tests at your command!</div>
        </div>
      )}
      <Routes>
        <Route path="/login" element={
          isAuthenticated
            ? <Navigate to="/generator" replace />
            : <Login onLoginSuccess={handleLoginSuccess} />
        } />
        <Route path="/*" element={
          isAuthenticated
            ? <Layout user={user} onLogout={handleLogout} />
            : <Navigate to="/login" replace />
        } />
      </Routes>
    </>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <AppInner />
    </BrowserRouter>
  );
}
