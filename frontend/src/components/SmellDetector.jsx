import React, { useState } from "react";
import axios from "axios";

const API_BASE = "http://127.0.0.1:5000/api/smell-detector";

function SmellDetector() {
  const [mode, setMode] = useState("code"); // code, file, directory, github
  const [code, setCode] = useState("");
  const [githubUrl, setGithubUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);

  const handleAnalyzeCode = async () => {
    if (!code) return;
    
    setLoading(true);
    try {
      const resp = await axios.post(`${API_BASE}/analyze/code`, {
        code,
        filename: "test_code.py"
      });
      setResults(resp.data);
      setLoading(false);
    } catch (err) {
      alert("Error: " + err.message);
      setLoading(false);
    }
  };

  const handleAnalyzeFile = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const resp = await axios.post(`${API_BASE}/analyze/file`, formData);
      setResults(resp.data);
      setLoading(false);
    } catch (err) {
      alert("Error: " + err.message);
      setLoading(false);
    }
  };

  const handleAnalyzeDirectory = async (e) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;

    setLoading(true);
    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
      formData.append("files[]", files[i]);
    }

    try {
      const resp = await axios.post(`${API_BASE}/analyze/directory`, formData);
      setResults(resp.data);
      setLoading(false);
    } catch (err) {
      alert("Error: " + err.message);
      setLoading(false);
    }
  };

  const handleAnalyzeGithub = async () => {
    if (!githubUrl) return;

    setLoading(true);
    try {
      const resp = await axios.post(`${API_BASE}/analyze/github`, {
        github_url: githubUrl
      });
      setResults(resp.data);
      setLoading(false);
    } catch (err) {
      alert("Error: " + err.message);
      setLoading(false);
    }
  };

  const openReport = () => {
    window.open(`${API_BASE}/report`, "_blank");
  };

  return (
    <div className="module-container">
      <div className="section">
        <h2>🔍 Detect Test Smells</h2>
        
        <div className="mode-selector">
          <button
            className={`mode-btn ${mode === "code" ? "active" : ""}`}
            onClick={() => setMode("code")}
          >
            📝 Code
          </button>
          <button
            className={`mode-btn ${mode === "file" ? "active" : ""}`}
            onClick={() => setMode("file")}
          >
            📄 File
          </button>
          <button
            className={`mode-btn ${mode === "directory" ? "active" : ""}`}
            onClick={() => setMode("directory")}
          >
            📁 Directory
          </button>
          <button
            className={`mode-btn ${mode === "github" ? "active" : ""}`}
            onClick={() => setMode("github")}
          >
            🐙 GitHub
          </button>
        </div>

        {mode === "code" && (
          <div>
            <textarea
              className="code-input"
              placeholder="Paste your test code here..."
              value={code}
              onChange={(e) => setCode(e.target.value)}
            />
            <button
              className="btn btn-primary"
              onClick={handleAnalyzeCode}
              disabled={loading || !code}
            >
              {loading ? "⏳ Analyzing..." : "🔍 Analyze Code"}
            </button>
          </div>
        )}

        {mode === "file" && (
          <div>
            <label className="file-upload-label">
              <input
                type="file"
                accept=".py"
                onChange={handleAnalyzeFile}
                disabled={loading}
              />
              <span>📄 Choose Python File</span>
            </label>
          </div>
        )}

        {mode === "directory" && (
          <div>
            <label className="file-upload-label">
              <input
                type="file"
                accept=".py"
                multiple
                webkitdirectory="true"
                onChange={handleAnalyzeDirectory}
                disabled={loading}
              />
              <span>📁 Choose Directory</span>
            </label>
          </div>
        )}

        {mode === "github" && (
          <div>
            <input
              type="text"
              className="text-input"
              placeholder="https://github.com/username/repo"
              value={githubUrl}
              onChange={(e) => setGithubUrl(e.target.value)}
            />
            <button
              className="btn btn-primary"
              onClick={handleAnalyzeGithub}
              disabled={loading || !githubUrl}
            >
              {loading ? "⏳ Analyzing..." : "🐙 Analyze Repository"}
            </button>
          </div>
        )}
      </div>

      {results && (
        <div className="section">
          <h3>📊 Analysis Results</h3>
          <div className="results-card">
            {results.files_analyzed && (
              <p><strong>Files Analyzed:</strong> {results.files_analyzed}</p>
            )}
            <p><strong>Total Test Smells:</strong> {results.total_smells}</p>
            {results.smells && (
              <div className="smells-list">
                <h4>Detected Smells:</h4>
                {results.smells.map((smell, idx) => (
                  <div key={idx} className="smell-item">
                    <span className="smell-type">{smell.type}</span>
                    <span className="smell-method">{smell.method}</span>
                    <span className="smell-lines">Line {smell.lines}</span>
                  </div>
                ))}
              </div>
            )}
            {results.report_available && (
              <button className="btn btn-accent" onClick={openReport}>
                📄 View Full Report
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default SmellDetector;
