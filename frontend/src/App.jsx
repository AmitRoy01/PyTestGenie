import React, { useState, useEffect } from "react";
import TestGenerator from "./components/TestGenerator";
import SmellDetector from "./components/SmellDetector";
import TestRefactorer from "./components/TestRefactorer";
import Login from "./components/Login";
import AdminPanel from "./components/AdminPanel";
import authService from "./services/authService";
import "./App.css";
import logoUrl from "../../assets/pyTestGenieLogo.png";
import genieImageUrl from "../../assets/pyTestGenie.png";
//import genieSoundUrl from "../../assets/genie_appear.m4a";
import genieSoundUrl from "../../assets/ginie_sound.mp3";


function App() {
  const [activeTab, setActiveTab] = useState("generator");
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [showGenie, setShowGenie] = useState(false);

  useEffect(() => {
    // Check if user is already logged in
    const token = authService.getToken();
    const userData = authService.getUser();
    
    if (token && userData) {
      setIsAuthenticated(true);
      setUser(userData);
    }
  }, []);

  useEffect(() => {
    if (!showGenie) return;
    const audio = new Audio(genieSoundUrl);
    audio.volume = 0.9;
    audio.play().catch(() => {});
    const timer = setTimeout(() => setShowGenie(false), 4000);
    return () => {
      clearTimeout(timer);
      audio.pause();
    };
  }, [showGenie]);

  const handleLoginSuccess = () => {
    setIsAuthenticated(true);
    setUser(authService.getUser());
    setShowGenie(true);
  };

  const handleLogout = () => {
    authService.logout();
    setIsAuthenticated(false);
    setUser(null);
    setActiveTab("generator");
  };

  if (!isAuthenticated) {
    return <Login onLoginSuccess={handleLoginSuccess} />;
  }

  return (
    <div className="app-container">
      {showGenie && (
        <div className="genie-overlay">
          <img src={genieImageUrl} alt="PyTestGenie" className="genie-image" />
          <div className="genie-message">Tests at your command!</div>
        </div>
      )}
      <header className="app-header">
        <div className="header-content">
          <div className="header-title">
            <div className="header-title-row">
              <img src={logoUrl} alt="PyTestGenie Logo" className="app-logo" />
              <h1>PyTestGenie</h1>
            </div>
            <p>Automated Test Generation, Smell Detection & Refactoring</p>
          </div>
          <div className="header-user">
            <span className="user-name">
              👤 {user?.username}
              {user?.is_admin && <span className="admin-badge-small">👑</span>}
            </span>
            <button className="logout-button" onClick={handleLogout}>
              🚪 Logout
            </button>
          </div>
        </div>
      </header>

      <nav className="tab-navigation">
        <button
          className={`tab-button ${activeTab === "generator" ? "active" : ""}`}
          onClick={() => setActiveTab("generator")}
        >
          <span className="tab-icon">🚀</span>
          Test Code Generator
        </button>
        <button
          className={`tab-button ${activeTab === "detector" ? "active" : ""}`}
          onClick={() => setActiveTab("detector")}
        >
          <span className="tab-icon">🔍</span>
          Test Smell Detector
        </button>
        <button
          className={`tab-button ${activeTab === "refactorer" ? "active" : ""}`}
          onClick={() => setActiveTab("refactorer")}
        >
          <span className="tab-icon">🔧</span>
          Test Code Refactorer
        </button>
        {user?.is_admin && (
          <button
            className={`tab-button ${activeTab === "admin" ? "active" : ""}`}
            onClick={() => setActiveTab("admin")}
          >
            <span className="tab-icon">👨‍💼</span>
            Admin Panel
          </button>
        )}
      </nav>

      <main className="main-content">
        {activeTab === "generator" && <TestGenerator />}
        {activeTab === "detector" && <SmellDetector />}
        {activeTab === "refactorer" && <TestRefactorer />}
        {activeTab === "admin" && user?.is_admin && <AdminPanel />}
      </main>

      <footer className="app-footer">
        <p>PyTestGenie - Complete Testing Pipeline | Logged in as {user?.username}</p>
      </footer>
    </div>
  );
}

export default App;
