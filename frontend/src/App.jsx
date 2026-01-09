import React, { useState } from "react";
import TestGenerator from "./components/TestGenerator";
import SmellDetector from "./components/SmellDetector";
import "./App.css";

function App() {
  const [activeTab, setActiveTab] = useState("generator");

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>🧪 PyTestGenie</h1>
        <p>Automated Test Generation & Smell Detection</p>
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
      </nav>

      <main className="main-content">
        {activeTab === "generator" && <TestGenerator />}
        {activeTab === "detector" && <SmellDetector />}
      </main>

      <footer className="app-footer">
        <p>PyTestGenie - Complete Testing Pipeline</p>
      </footer>
    </div>
  );
}

export default App;
