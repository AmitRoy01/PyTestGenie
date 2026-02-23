import React, { useState } from "react";
import axios from "axios";
import RefactoringPanel from "./RefactoringPanel";

const API_BASE = `${import.meta.env.VITE_API_BASE_URL || 'https://pytestgenie.onrender.com/api'}/smell-detector`;

function SmellDetector() {
  const [mode, setMode] = useState("code"); // code, file, directory, github
  const [code, setCode] = useState("");
  const [githubUrl, setGithubUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [selectedFile, setSelectedFile] = useState(null);
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [generatingAiReport, setGeneratingAiReport] = useState(false);
  const [showRefactoring, setShowRefactoring] = useState(false);
  const [analyzedCode, setAnalyzedCode] = useState("");
  const [detectedSmells, setDetectedSmells] = useState([]);
  const [fileRefactoringOpen, setFileRefactoringOpen] = useState({});
  const [mountedFileRefactoring, setMountedFileRefactoring] = useState({});
  const [mountedRefactoring, setMountedRefactoring] = useState(false);

  const handleAnalyzeCode = async () => {
    if (!code) return;
    
    setLoading(true);
    setShowRefactoring(false);
    setMountedRefactoring(false);
    try {
      const resp = await axios.post(`${API_BASE}/analyze/code`, {
        code,
        filename: "test_code.py"
      });
      setResults(resp.data);
      setAnalyzedCode(code);
      setDetectedSmells(resp.data.smells || []);
      setLoading(false);
    } catch (err) {
      alert("Error: " + err.message);
      setLoading(false);
    }
  };

  const handleFileSelect = (e) => {
    setSelectedFile(e.target.files[0]);
  };

  const handleAnalyzeFile = async () => {
    if (!selectedFile) return;

    setLoading(true);
    setShowRefactoring(false);
    setMountedRefactoring(false);
    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const resp = await axios.post(`${API_BASE}/analyze/file`, formData);
      setResults(resp.data);
      setAnalyzedCode(resp.data.code || "");
      setDetectedSmells(resp.data.smells || []);
      setLoading(false);
    } catch (err) {
      alert("Error: " + err.message);
      setLoading(false);
    }
  };

  const handleDirectorySelect = (e) => {
    setSelectedFiles(Array.from(e.target.files));
  };

  const handleAnalyzeDirectory = async () => {
    if (!selectedFiles || selectedFiles.length === 0) return;

    setLoading(true);
    setShowRefactoring(false);
    setFileRefactoringOpen({});
    setMountedFileRefactoring({});
    const formData = new FormData();
    for (let i = 0; i < selectedFiles.length; i++) {
      formData.append("files[]", selectedFiles[i]);
    }

    try {
      const resp = await axios.post(`${API_BASE}/analyze/directory`, formData);
      setResults(resp.data);
      setAnalyzedCode(resp.data.code || "");
      setDetectedSmells(resp.data.smells || []);
      setLoading(false);
    } catch (err) {
      alert("Error: " + err.message);
      setLoading(false);
    }
  };

  const handleAnalyzeGithub = async () => {
    if (!githubUrl) return;

    setLoading(true);
    setShowRefactoring(false);
    setFileRefactoringOpen({});
    setMountedFileRefactoring({});
    try {
      const resp = await axios.post(`${API_BASE}/analyze/github`, {
        github_url: githubUrl
      });
      setResults(resp.data);
      setAnalyzedCode(resp.data.code || "");
      setDetectedSmells(resp.data.smells || []);
      setLoading(false);
    } catch (err) {
      alert("Error: " + err.message);
      setLoading(false);
    }
  };

  const openReport = () => {
    window.open(`${API_BASE}/report`, "_blank");
  };
  const openAiReport = () => {
    window.open(`${API_BASE}/report/ai`, "_blank");
  };
  const downloadAiReport = () => {
    window.open(`${API_BASE}/report/ai/download`, "_blank");
  };
  const generateAiReport = async () => {
    try {
      setGeneratingAiReport(true);
      if (mode === "code") {
        await axios.post(`${API_BASE}/analyze/code?use_llm=true`, { code, filename: "test_code.py" });
      } else if (mode === "file") {
        const formData = new FormData();
        if (!selectedFile) return;
        formData.append("file", selectedFile);
        await axios.post(`${API_BASE}/analyze/file?use_llm=true`, formData);
      } else if (mode === "directory") {
        const formData = new FormData();
        if (!selectedFiles || selectedFiles.length === 0) return;
        for (let i = 0; i < selectedFiles.length; i++) {
          formData.append("files[]", selectedFiles[i]);
        }
        await axios.post(`${API_BASE}/analyze/directory?use_llm=true`, formData);
      } else if (mode === "github") {
        await axios.post(`${API_BASE}/analyze/github?use_llm=true`, { github_url: githubUrl });
      }
      setGeneratingAiReport(false);
      openAiReport();
    } catch (err) {
      setGeneratingAiReport(false);
      alert("Error generating AI report: " + err.message);
    }
  };

  const downloadReport = () => {
    window.open(`${API_BASE}/report/download`, "_blank");
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
                onChange={handleFileSelect}
                disabled={loading}
              />
              <span>📄 Choose Python File</span>
            </label>
            {selectedFile && (
              <div style={{ marginTop: "15px" }}>
                <p style={{ 
                  padding: "10px", 
                  background: "#f5f5f5", 
                  borderRadius: "4px",
                  marginBottom: "10px"
                }}>
                  <strong>Selected File:</strong> {selectedFile.name}
                </p>
                <button
                  className="btn btn-primary"
                  onClick={handleAnalyzeFile}
                  disabled={loading}
                >
                  {loading ? "⏳ Analyzing..." : "🔍 Detect Test Smells"}
                </button>
              </div>
            )}
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
                onChange={handleDirectorySelect}
                disabled={loading}
              />
              <span>📁 Choose Directory</span>
            </label>
            {selectedFiles.length > 0 && (
              <div style={{ marginTop: "15px" }}>
                <p style={{ 
                  padding: "10px", 
                  background: "#f5f5f5", 
                  borderRadius: "4px",
                  marginBottom: "10px"
                }}>
                  <strong>Selected:</strong> {selectedFiles.length} Python file(s)
                </p>
                <button
                  className="btn btn-primary"
                  onClick={handleAnalyzeDirectory}
                  disabled={loading}
                >
                  {loading ? "⏳ Analyzing..." : "🔍 Detect Test Smells"}
                </button>
              </div>
            )}
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

            {/* Single-file smells (code / file mode) */}
            {!results.files && results.smells && (
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
                📄 View Report
              </button>
            )}
            {results.report_available && (
              <button className="btn btn-accent" style={{ marginLeft: "10px" }} onClick={generateAiReport} disabled={generatingAiReport}>
                📄 View AI powered Report
              </button>
            )}
            {results.report_available && (
              <button className="btn" style={{ marginLeft: "10px" }} onClick={downloadReport}>
                ⬇️ Download Report
              </button>
            )}
            {results.report_available && (
              <button className="btn" style={{ marginLeft: "10px" }} onClick={downloadAiReport}>
                ⬇️ Download AI Report
              </button>
            )}

            {/* Single-file refactor button (code / file mode) */}
            {!results.files && results.smells && results.smells.length > 0 && (
              <button
                className="btn btn-primary"
                style={{ marginLeft: "10px", marginTop: "10px" }}
                onClick={() => {
                  setMountedRefactoring(true);
                  setShowRefactoring(prev => !prev);
                }}
              >
                {showRefactoring ? '🔼 Hide Refactoring' : '🔧 Refactor Code'}
              </button>
            )}
          </div>
        </div>
      )}

      {/* Single-file RefactoringPanel - stays mounted once opened, CSS hide/show */}
      {mountedRefactoring && analyzedCode && (
        <div style={{ display: showRefactoring ? 'block' : 'none' }}>
          <div className="section">
            <RefactoringPanel code={analyzedCode} detectedSmells={detectedSmells} />
          </div>
        </div>
      )}

      {/* Multi-file per-file cards (directory / github mode) */}
      {results && results.files && results.files.map((fileResult, idx) => (
        <div key={idx} className="section" style={{ marginTop: "15px" }}>
          <div className="results-card">
            <h4 style={{ marginBottom: "10px", color: "#333", display: "flex", alignItems: "center", gap: "8px" }}>
              📄 {fileResult.filename}
              <span style={{ fontSize: "0.82em", color: "#666", fontWeight: "normal" }}>
                ({fileResult.smell_count} smell{fileResult.smell_count !== 1 ? 's' : ''})
              </span>
            </h4>
            {fileResult.smells && fileResult.smells.length > 0 ? (
              <>
                <div className="smells-list">
                  {fileResult.smells.map((smell, sidx) => (
                    <div key={sidx} className="smell-item">
                      <span className="smell-type">{smell.type}</span>
                      <span className="smell-method">{smell.method}</span>
                      <span className="smell-lines">Line {smell.lines}</span>
                    </div>
                  ))}
                </div>
                <button
                  className="btn btn-primary"
                  style={{ marginTop: "10px" }}
                  onClick={() => {
                    setMountedFileRefactoring(prev => ({ ...prev, [idx]: true }));
                    setFileRefactoringOpen(prev => ({ ...prev, [idx]: !prev[idx] }));
                  }}
                >
                  {fileRefactoringOpen[idx] ? '🔼 Hide Refactoring' : '🔧 Refactor Code'}
                </button>
              </>
            ) : (
              <p style={{ color: "#28a745", marginBottom: 0 }}>✅ No smells detected in this file.</p>
            )}
          </div>
          {mountedFileRefactoring[idx] && (
            <div style={{ display: fileRefactoringOpen[idx] ? 'block' : 'none', marginTop: "10px" }} className="section">
              <RefactoringPanel code={fileResult.code} detectedSmells={fileResult.smells} />
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

export default SmellDetector;
