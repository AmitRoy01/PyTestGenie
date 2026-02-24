import React, { useState, useEffect } from "react";
import axios from "axios";
import RefactoringPanel from "./RefactoringPanel";
import SaveVersionModal from "./SaveVersionModal";
import PipelineReportModal from "./PipelineReportModal";
import authService from "../services/authService";

const API_BASE = `${import.meta.env.VITE_API_BASE_URL || 'https://pytestgenie.onrender.com/api'}/smell-detector`;

// LLM model catalogue mirrors backend AVAILABLE_MODELS
const LLM_MODELS = {
  ollama: [
    { name: "Llama 3.2", model_id: "llama3.2" },
  ],
  huggingface: [
    { name: "Mistral 7B Instruct v0.2", model_id: "mistralai/Mistral-7B-Instruct-v0.2" },
    { name: "GPT-OSS 20B", model_id: "openai/gpt-oss-20b:groq" },
  ],
};

function SmellDetector({ initialData }) {
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
  const [showSaveModal, setShowSaveModal] = useState(false);
  const [saveFileIdx, setSaveFileIdx] = useState(null); // null = single-file, number = per-file

  // Detection method
  const [detectionMethod, setDetectionMethod] = useState("rule_based"); // rule_based | llm_based
  const [llmModelType, setLlmModelType] = useState("ollama");
  const [llmModelName, setLlmModelName] = useState("llama3.2");

  // Pipeline report
  const [refactoringResult, setRefactoringResult] = useState(null);
  const [reportModalOpen,   setReportModalOpen]   = useState(false);

  // Pre-populate from loaded version
  useEffect(() => {
    if (!initialData) return;
    if (initialData.source_code) { setCode(initialData.source_code); setAnalyzedCode(initialData.source_code); }
    if (initialData.smell_results) { setResults(initialData.smell_results); setDetectedSmells(initialData.smell_results.smells || []); }
  }, [initialData]);

  // When model type changes reset model name to first in list
  const handleLlmModelTypeChange = (type) => {
    setLlmModelType(type);
    setLlmModelName(LLM_MODELS[type][0].model_id);
  };

  const handleAnalyzeCode = async () => {
    if (!code) return;
    
    setLoading(true);
    setShowRefactoring(false);
    setMountedRefactoring(false);
    try {
      const payload = {
        code,
        filename: "test_code.py",
        detection_method: detectionMethod,
        ...(detectionMethod === 'llm_based' && { model_type: llmModelType, model_name: llmModelName }),
      };
      const resp = await axios.post(`${API_BASE}/analyze/code`, payload);
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

    const params = new URLSearchParams({ detection_method: detectionMethod });
    if (detectionMethod === 'llm_based') {
      params.set('model_type', llmModelType);
      params.set('model_name', llmModelName);
    }

    try {
      const resp = await axios.post(`${API_BASE}/analyze/file?${params}`, formData);
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

    const params = new URLSearchParams({ detection_method: detectionMethod });
    if (detectionMethod === 'llm_based') {
      params.set('model_type', llmModelType);
      params.set('model_name', llmModelName);
    }

    try {
      const resp = await axios.post(`${API_BASE}/analyze/directory?${params}`, formData);
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
      const payload = {
        github_url: githubUrl,
        detection_method: detectionMethod,
        ...(detectionMethod === 'llm_based' && { model_type: llmModelType, model_name: llmModelName }),
      };
      const resp = await axios.post(`${API_BASE}/analyze/github`, payload);
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

        {/* ---- Detection Method Selector ---- */}
        <div className="method-selector" style={{ marginBottom: "16px" }}>
          <label className="radio-label">
            <input
              type="radio"
              checked={detectionMethod === "rule_based"}
              onChange={() => setDetectionMethod("rule_based")}
            />
            <span>📏 Rule-Based</span>
          </label>
          <label className="radio-label" style={{ marginLeft: "18px" }}>
            <input
              type="radio"
              checked={detectionMethod === "llm_based"}
              onChange={() => setDetectionMethod("llm_based")}
            />
            <span>🧠 LLM-Based</span>
          </label>
        </div>

        {/* ---- LLM model picker (only visible when llm_based) ---- */}
        {detectionMethod === "llm_based" && (
          <div style={{ display: "flex", gap: "14px", flexWrap: "wrap", marginBottom: "16px", alignItems: "center" }}>
            <div>
              <label style={{ fontWeight: "bold", marginRight: "8px" }}>🖥️ Provider:</label>
              <select
                value={llmModelType}
                onChange={(e) => handleLlmModelTypeChange(e.target.value)}
                style={{ padding: "7px 12px", borderRadius: "6px", border: "1px solid #ccc", fontSize: "14px" }}
              >
                <option value="ollama">Ollama (Local)</option>
                <option value="huggingface">HuggingFace API</option>
              </select>
            </div>
            <div>
              <label style={{ fontWeight: "bold", marginRight: "8px" }}>🤖 Model:</label>
              <select
                value={llmModelName}
                onChange={(e) => setLlmModelName(e.target.value)}
                style={{ padding: "7px 12px", borderRadius: "6px", border: "1px solid #ccc", fontSize: "14px" }}
              >
                {(LLM_MODELS[llmModelType] || []).map((m) => (
                  <option key={m.model_id} value={m.model_id}>{m.name}</option>
                ))}
              </select>
            </div>
            <div style={{ padding: "7px 12px", backgroundColor: "#e8f4fd", borderRadius: "6px", fontSize: "13px", color: "#1565c0" }}>
              💡 LLM detects smells with line numbers &amp; method names — may take a moment.
            </div>
          </div>
        )}
        
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
            🐙 GitHub <span style={{ fontSize: "0.78em", opacity: 0.7, fontWeight: "normal" }}>(Optional)</span>
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
                  <div key={idx} className="smell-item" style={{ flexDirection: "column", alignItems: "flex-start", gap: "6px", padding: "10px 12px" }}>
                    <div style={{ display: "flex", gap: "8px", flexWrap: "wrap", alignItems: "center" }}>
                      <span className="smell-type">{smell.type}</span>
                      <span className="smell-method">{smell.method}</span>
                      {smell.lines && smell.lines.length > 0 && (
                        <span className="smell-lines">Line {smell.lines}</span>
                      )}
                    </div>
                    {results.detection_method === "llm_based" && smell.explanation && (
                      <div style={{
                        marginTop: "4px",
                        padding: "8px 10px",
                        background: "#f8f9fa",
                        borderLeft: "3px solid #e67e22",
                        borderRadius: "4px",
                        fontSize: "13px",
                        color: "#333",
                        lineHeight: "1.55",
                        width: "100%",
                        boxSizing: "border-box",
                        whiteSpace: "pre-wrap"
                      }}>
                        {smell.explanation}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}

            {/* detection method badge */}
            <p style={{ fontSize: "12px", color: "#666", marginTop: "4px" }}>
              <strong>Detection:</strong>{" "}
              {results.detection_method === "llm_based"
                ? `🧠 LLM-Based (${results.model_used || llmModelName})`
                : "📏 Rule-Based"}
            </p>

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
            {!results.files && (
              <button
                className="btn btn-primary"
                style={{ marginLeft: "10px", marginTop: "10px" }}
                onClick={() => { setSaveFileIdx(null); setShowSaveModal(true); }}
              >
                💾 Save to Project
              </button>
            )}
          </div>
        </div>
      )}

      {/* Single-file RefactoringPanel - stays mounted once opened, CSS hide/show */}
      {mountedRefactoring && analyzedCode && (
        <div style={{ display: showRefactoring ? 'block' : 'none' }}>
          <div className="section">
            <RefactoringPanel
              code={analyzedCode}
              detectedSmells={detectedSmells}
              onRefactored={setRefactoringResult}
            />
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
                    <div key={sidx} className="smell-item" style={{ flexDirection: "column", alignItems: "flex-start", gap: "6px", padding: "10px 12px" }}>
                      <div style={{ display: "flex", gap: "8px", flexWrap: "wrap", alignItems: "center" }}>
                        <span className="smell-type">{smell.type}</span>
                        <span className="smell-method">{smell.method}</span>
                        {smell.lines && smell.lines.length > 0 && (
                          <span className="smell-lines">Line {smell.lines}</span>
                        )}
                      </div>
                      {results.detection_method === "llm_based" && smell.explanation && (
                        <div style={{
                          marginTop: "4px",
                          padding: "8px 10px",
                          background: "#f8f9fa",
                          borderLeft: "3px solid #e67e22",
                          borderRadius: "4px",
                          fontSize: "13px",
                          color: "#333",
                          lineHeight: "1.55",
                          width: "100%",
                          boxSizing: "border-box",
                          whiteSpace: "pre-wrap"
                        }}>
                          {smell.explanation}
                        </div>
                      )}
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
                <button
                  className="btn btn-primary"
                  style={{ marginTop: "10px", marginLeft: "8px" }}
                  onClick={() => { setSaveFileIdx(idx); setShowSaveModal(true); }}
                >
                  💾 Save to Project
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

      {showSaveModal && (
        <SaveVersionModal
          open={showSaveModal}
          onClose={() => setShowSaveModal(false)}
          onSaved={() => setShowSaveModal(false)}
          step="smell_detected"
          defaultLabel="After smell detection"
          data={saveFileIdx === null ? {
            source_code:  analyzedCode,
            smell_results: results,
          } : {
            source_code:   results?.files?.[saveFileIdx]?.code || '',
            source_filename: results?.files?.[saveFileIdx]?.filename || '',
            smell_results: { smells: results?.files?.[saveFileIdx]?.smells, total_smells: results?.files?.[saveFileIdx]?.smell_count },
          }}
        />
      )}

      {/* Floating report button — visible once any input or result exists */}
      {(code || analyzedCode || results) && (
        <div style={{ position: 'fixed', bottom: 28, right: 28, zIndex: 1000, display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 8 }}>
          <div className="report-btn-tooltip">
            Click to generate<br />Pipeline Report
            <div className="report-btn-tooltip-arrow" />
          </div>
          <button
            onClick={() => setReportModalOpen(true)}
            title="Generate Pipeline Report"
            style={{
              background: 'linear-gradient(135deg,#1a237e,#283593)',
              color: '#fff', border: 'none', borderRadius: 50,
              width: 56, height: 56, fontSize: '1.4rem',
              cursor: 'pointer', boxShadow: '0 4px 16px rgba(0,0,0,.3)',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              flexShrink: 0,
            }}
          >
            📄
          </button>
        </div>
      )}

      <PipelineReportModal
        open={reportModalOpen}
        onClose={() => setReportModalOpen(false)}
        pipelineData={{
          username:       authService.getUser()?.username || '',
          inputMode:      mode,
          sourceFilename: selectedFile?.name || 'code.py',
          sourceCode:     analyzedCode || code,
          smellResults:   results,
          refactorResult: refactoringResult,
        }}
      />
    </div>
  );
}

export default SmellDetector;
