import React, { useState } from "react";
import axios from "axios";
import RefactoringPanel from "./RefactoringPanel";

const API_BASE = `${import.meta.env.VITE_API_BASE_URL || 'https://pytestgenie.onrender.com/api'}/test-generator`;
const SMELL_API_BASE = `${import.meta.env.VITE_API_BASE_URL || 'https://pytestgenie.onrender.com/api'}/smell-detector`;

function TestGenerator() {
  const [code, setCode] = useState("");
  const [testCode, setTestCode] = useState("");
  const [loading, setLoading] = useState(false);
  const [logs, setLogs] = useState([]);
  const [useAI, setUseAI] = useState(false);
  const [canDetectSmells, setCanDetectSmells] = useState(false);
  const [algorithm, setAlgorithm] = useState("DYNAMOSA");
  const [aiModel, setAiModel] = useState("gpt-oss");
  const [smellResults, setSmellResults] = useState(null);
  const [generatingAiReport, setGeneratingAiReport] = useState(false);
  const [showRefactoring, setShowRefactoring] = useState(false);
  const [detectedSmells, setDetectedSmells] = useState([]);
  
  // File upload states
  const [inputMode, setInputMode] = useState("paste"); // "paste", "file", "project"
  const [uploadedFile, setUploadedFile] = useState(null);
  const [projectFiles, setProjectFiles] = useState([]);
  const [selectedModule, setSelectedModule] = useState("");
  const [projectId, setProjectId] = useState(null);

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      const resp = await axios.post(`${API_BASE}/upload-file`, formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      
      setUploadedFile(resp.data.filename);
      setCode(resp.data.content);
      alert(`File "${resp.data.filename}" uploaded successfully!`);
    } catch (err) {
      alert("Error uploading file: " + err.message);
    }
  };

  const handleProjectUpload = async (e) => {
    const files = e.target.files;
    if (!files || files.length === 0) return;

    const formData = new FormData();
    
    // Add all files with their relative paths
    for (let i = 0; i < files.length; i++) {
      const file = files[i];
      // Use webkitRelativePath for folder structure
      const relativePath = file.webkitRelativePath || file.name;
      
      // Create a new file with the relative path as name
      const blob = new Blob([file], { type: file.type });
      formData.append("files", new File([blob], relativePath));
    }

    try {
      const resp = await axios.post(`${API_BASE}/upload-project`, formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      
      setProjectId(resp.data.project_id);
      setProjectFiles(resp.data.files);
      setSelectedModule("");
      alert(`Project uploaded! Found ${resp.data.total_files} Python files.`);
    } catch (err) {
      alert("Error uploading project: " + err.message);
    }
  };

  const handleModuleSelect = async (filepath) => {
    if (!projectId) return;
    
    // Normalize filepath (replace backslash with forward slash)
    const normalizedPath = filepath.replace(/\\/g, '/');
    
    // Extract module name from filepath (remove .py and path)
    const moduleName = normalizedPath.replace(/\.py$/, '').split('/').pop();
    setSelectedModule(moduleName);
    
    try {
      const resp = await axios.get(`${API_BASE}/project/${projectId}/file/${normalizedPath}`);
      setCode(resp.data.content);
    } catch (err) {
      alert("Error loading file: " + err.message);
    }
  };

  const handleGenerate = async () => {
    setLoading(true);
    setTestCode("");
    setLogs([]);
    setCanDetectSmells(false);

    try {
      if (useAI) {
        // AI-based generation with selected model
        if (!code) {
          alert("Please provide code (paste, upload file, or select from project)");
          setLoading(false);
          return;
        }
        
        // Build request payload
        const payload = { 
          code, 
          model: aiModel 
        };
        
        // If project mode, include project_id for dependency analysis
        if (inputMode === "project" && projectId) {
          payload.project_id = projectId;
        }
        
        const resp = await axios.post(`${API_BASE}/generate-tests/ai`, payload);
        setTestCode(resp.data.test_code);
        setCanDetectSmells(true);
        setLoading(false);
      } else {
        // Pynguin-based generation
        let taskId;
        
        if (inputMode === "project" && projectId && selectedModule) {
          // Generate for project module
          const resp = await axios.post(`${API_BASE}/generate-tests/project`, {
            project_id: projectId,
            module_name: selectedModule,
            algorithm
          });
          taskId = resp.data.task_id;
        } else {
          // Generate for code snippet
          if (!code) {
            alert("Please provide code (paste, upload file, or select from project)");
            setLoading(false);
            return;
          }
          
          const resp = await axios.post(`${API_BASE}/generate-tests/pynguin`, { code, algorithm });
          taskId = resp.data.task_id;
        }

        const url = `${API_BASE}/generate-tests/stream/${taskId}`;
        const source = new EventSource(url);

        source.onmessage = (e) => {
          const obj = JSON.parse(e.data);
          
          if (obj.type === "log") {
            setLogs((prev) => [...prev, obj.line]);
          } else if (obj.type === "result") {
            setTestCode(obj.test_code);
            setCanDetectSmells(true);
          } else if (obj.type === "error") {
            setLogs((prev) => [...prev, `ERROR: ${obj.message}`]);
          } else if (obj.type === "done") {
            setLoading(false);
            source.close();
          }
        };

        source.onerror = () => {
          setLogs((prev) => [...prev, "Connection lost."]);
          setLoading(false);
          source.close();
        };
      }
    } catch (err) {
      alert("Error generating tests: " + err.message);
      setLoading(false);
    }
  };

  const handleDetectSmells = async () => {
    if (!testCode) return;

    try {
      const resp = await axios.post(
        `${SMELL_API_BASE}/analyze/code`,
        { code: testCode, filename: "generated_test.py" }
      );
      if (resp.data.status === "success") {
        setSmellResults(resp.data);
        setDetectedSmells(resp.data.smells || []);
      }
    } catch (err) {
      alert("Error detecting smells: " + err.message);
    }
  };

  const openReport = () => {
    window.open(`${SMELL_API_BASE}/report`, "_blank");
  };

  const openAiReport = () => {
    window.open(`${SMELL_API_BASE}/report/ai`, "_blank");
  };

  const downloadReportFile = () => {
    window.open(`${SMELL_API_BASE}/report/download`, "_blank");
  };

  const downloadAiReportFile = () => {
    window.open(`${SMELL_API_BASE}/report/ai/download`, "_blank");
  };

  const generateAiReport = async () => {
    if (!testCode) return;
    try {
      setGeneratingAiReport(true);
      await axios.post(
        `${SMELL_API_BASE}/analyze/code?use_llm=true`,
        { code: testCode, filename: "generated_test.py" }
      );
      setGeneratingAiReport(false);
      openAiReport();
    } catch (err) {
      setGeneratingAiReport(false);
      alert("Error generating AI report: " + err.message);
    }
  };

  const handleDownload = () => {
    const blob = new Blob([testCode], { type: "text/python" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "test_generated.py";
    link.click();
  };

  return (
    <div className="module-container">
      <div className="section">
        <h2>📝 Generate Test Code</h2>
        
        <div className="method-selector">
          <label className="radio-label">
            <input
              type="radio"
              checked={!useAI}
              onChange={() => setUseAI(false)}
            />
            <span>🤖 Rule-Based Approach</span>
          </label>
          <label className="radio-label">
            <input
              type="radio"
              checked={useAI}
              onChange={() => setUseAI(true)}
            />
            <span>🧠 LLM Based Approach</span>
          </label>
        </div>

        {/* Input Mode Selector */}
        <div className="input-mode-selector" style={{ marginTop: "15px" }}>
          <label style={{ fontWeight: "bold", marginRight: "10px" }}>📥 Input Mode:</label>
          <label className="radio-label" style={{ marginRight: "15px" }}>
            <input
              type="radio"
              checked={inputMode === "paste"}
              onChange={() => setInputMode("paste")}
            />
            <span>Paste Code</span>
          </label>
          <label className="radio-label" style={{ marginRight: "15px" }}>
            <input
              type="radio"
              checked={inputMode === "file"}
              onChange={() => setInputMode("file")}
            />
            <span>Upload File</span>
          </label>
          <label className="radio-label">
            <input
              type="radio"
              checked={inputMode === "project"}
              onChange={() => setInputMode("project")}
            />
            <span>Upload Project</span>
          </label>
        </div>

        {/* File Upload Section */}
        {inputMode === "file" && (
          <div style={{ marginTop: "15px" }}>
            <label 
              htmlFor="file-upload" 
              style={{
                display: "inline-block",
                padding: "10px 20px",
                backgroundColor: "#4CAF50",
                color: "white",
                borderRadius: "6px",
                cursor: "pointer",
                fontSize: "14px"
              }}
            >
              📄 Choose Python File
            </label>
            <input
              id="file-upload"
              type="file"
              accept=".py"
              onChange={handleFileUpload}
              style={{ display: "none" }}
            />
            {uploadedFile && (
              <span style={{ marginLeft: "10px", color: "#4CAF50" }}>
                ✓ {uploadedFile}
              </span>
            )}
          </div>
        )}

        {/* Project Upload Section */}
        {inputMode === "project" && (
          <div style={{ marginTop: "15px" }}>
            <label 
              htmlFor="project-upload" 
              style={{
                display: "inline-block",
                padding: "10px 20px",
                backgroundColor: "#2196F3",
                color: "white",
                borderRadius: "6px",
                cursor: "pointer",
                fontSize: "14px"
              }}
            >
              📁 Choose Project Folder
            </label>
            <input
              id="project-upload"
              type="file"
              webkitdirectory="true"
              directory="true"
              multiple
              onChange={handleProjectUpload}
              style={{ display: "none" }}
            />
            
            {projectFiles.length > 0 && (
              <div style={{ marginTop: "15px" }}>
                <label style={{ fontWeight: "bold", display: "block", marginBottom: "5px" }}>
                  Select Module to Test:
                </label>
                <select
                  value={selectedModule}
                  onChange={(e) => {
                    const filepath = projectFiles.find(f => 
                      f.path.replace(/\.py$/, '').split('/').pop() === e.target.value
                    )?.path;
                    if (filepath) handleModuleSelect(filepath);
                  }}
                  style={{
                    width: "100%",
                    padding: "8px 12px",
                    borderRadius: "6px",
                    border: "1px solid #ccc",
                    fontSize: "14px"
                  }}
                >
                  <option value="">-- Select a module --</option>
                  {projectFiles.map((file, idx) => {
                    const moduleName = file.path.replace(/\.py$/, '').split('/').pop();
                    return (
                      <option key={idx} value={moduleName}>
                        {file.path} ({(file.size / 1024).toFixed(2)} KB)
                      </option>
                    );
                  })}
                </select>
              </div>
            )}
          </div>
        )}

        {/* Code textarea - only show for paste mode or after file/project selection */}
        {(inputMode === "paste" || code) && (
          <textarea
            className="code-input"
            placeholder="Paste your Python code here..."
            value={code}
            onChange={(e) => setCode(e.target.value)}
            readOnly={inputMode === "project"}
            style={{
              marginTop: "15px",
              opacity: inputMode === "project" ? 0.7 : 1
            }}
          />
        )}

        {!useAI && (
          <div className="algorithm-selector" style={{ marginTop: "15px" }}>
            <label htmlFor="algorithm-select" style={{ fontWeight: "bold", marginRight: "10px" }}>
              🔧 Algorithm:
            </label>
            <select
              id="algorithm-select"
              value={algorithm}
              onChange={(e) => setAlgorithm(e.target.value)}
              style={{
                padding: "8px 12px",
                borderRadius: "6px",
                border: "1px solid #ccc",
                fontSize: "14px",
                cursor: "pointer"
              }}
            >
              <option value="DYNAMOSA">DynaMOSA (Default)</option>
              <option value="MIO">MIO</option>
              <option value="MOSA">MOSA</option>
              {/* <option value="RANDOM">Random</option>
              <option value="RANDOMSEARCH">Random Search</option>
              <option value="WHOLESUITE">Whole Suite</option> */}
            </select>
          </div>
        )}

        {useAI && (
          <div className="model-selector" style={{ marginTop: "15px" }}>
            <label htmlFor="model-select" style={{ fontWeight: "bold", marginRight: "10px" }}>
              🤖 AI Model:
            </label>
            <select
              id="model-select"
              value={aiModel}
              onChange={(e) => setAiModel(e.target.value)}
              style={{
                padding: "8px 12px",
                borderRadius: "6px",
                border: "1px solid #ccc",
                fontSize: "14px",
                cursor: "pointer"
              }}
            >
              <option value="gpt-oss">GPT-OSS 20B (HuggingFace)</option>
              <option value="llama-3.2">Llama 3.2 (Local)</option>
            </select>
            
            {inputMode === "project" && projectId && (
              <div style={{ 
                marginTop: "8px", 
                padding: "8px 12px", 
                backgroundColor: "#e3f2fd", 
                borderRadius: "6px",
                fontSize: "13px",
                color: "#1976d2"
              }}>
                💡 <strong>Project-Aware Mode:</strong> AI will analyze imported modules for better context
              </div>
            )}
          </div>
        )}

        <button 
          className="btn btn-primary" 
          onClick={handleGenerate} 
          disabled={loading || (inputMode === "project" ? !selectedModule : !code)}
          style={{ marginTop: "15px" }}
        >
          {loading ? "⏳ Generating..." : "🚀 Generate Tests"}
        </button>
      </div>

      {!useAI && logs.length > 0 && (
        <div className="section">
          <h3>📊 Generation Logs</h3>
          <div className="log-console">
            {logs.map((log, idx) => (
              <div key={idx} className="log-line">{log}</div>
            ))}
          </div>
        </div>
      )}

      {testCode && (
        <div className="section">
          <h3>✅ Generated Test Code</h3>
          <pre className="code-output">{testCode}</pre>
          
          <div className="button-group">
            <button className="btn btn-secondary" onClick={handleDownload}>
              💾 Download
            </button>
            {canDetectSmells && (
              <button className="btn btn-accent" onClick={handleDetectSmells}>
                🔍 Detect Test Smells
              </button>
            )}
          </div>
          {smellResults && (
            <div className="results-card" style={{ marginTop: "15px" }}>
              <h3>📊 Analysis Results</h3>
              <p><strong>Total Test Smells:</strong> {smellResults.total_smells}</p>
              {smellResults.report_available && (
                <div className="button-group" style={{ marginTop: "10px" }}>
                  <button className="btn btn-accent" onClick={openReport}>
                    📄 View Report
                  </button>
                  <button 
                    className="btn btn-accent" 
                    style={{ marginLeft: "10px" }} 
                    onClick={generateAiReport}
                    disabled={generatingAiReport}
                  >
                    📄 View AI powered Report
                  </button>
                      <button 
                        className="btn" 
                        style={{ marginLeft: "10px" }} 
                        onClick={downloadReportFile}
                      >
                        ⬇️ Download Report
                      </button>
                      <button 
                        className="btn" 
                        style={{ marginLeft: "10px" }} 
                        onClick={downloadAiReportFile}
                      >
                        ⬇️ Download AI Report
                      </button>
                      {smellResults.smells && smellResults.smells.length > 0 && (
                        <button 
                          className="btn btn-primary" 
                          style={{ marginLeft: "10px" }} 
                          onClick={() => setShowRefactoring(!showRefactoring)}
                        >
                          {showRefactoring ? '🔼 Hide Refactoring' : '🔧 Refactor Code'}
                        </button>
                      )}
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {showRefactoring && testCode && (
        <div className="section">
          <RefactoringPanel code={testCode} detectedSmells={detectedSmells} />
        </div>
      )}
    </div>
  );
}

export default TestGenerator;
