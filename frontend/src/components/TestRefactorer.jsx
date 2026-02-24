import React, { useState, useEffect } from "react";
import refactoringService from "../services/refactoringService";
import SaveVersionModal from "./SaveVersionModal";
import PipelineReportModal from "./PipelineReportModal";
import authService from "../services/authService";

function TestRefactorer({ initialData }) {
  const [mode, setMode] = useState("code"); // code or file
  const [code, setCode] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);
  const [selectedSmell, setSelectedSmell] = useState("All");
  const [agentMode, setAgentMode] = useState("single");
  const [modelType, setModelType] = useState("ollama");
  const [modelName, setModelName] = useState("llama3.2");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [availableModels, setAvailableModels] = useState({ ollama: [], huggingface: [] });
  const [availableSmells, setAvailableSmells] = useState([]);
  const [healthStatus, setHealthStatus] = useState(null);
  const [showSaveModal, setShowSaveModal] = useState(false);
  const [reportModalOpen, setReportModalOpen] = useState(false);

  // Pre-populate from loaded version
  useEffect(() => {
    if (!initialData) return;
    if (initialData.test_code)      setCode(initialData.test_code);
    if (initialData.refactor_smell) setSelectedSmell(initialData.refactor_smell);
    if (initialData.refactor_model) setModelName(initialData.refactor_model);
    if (initialData.refactored_code) setResult({ refactored_code: initialData.refactored_code });
  }, [initialData]);

  useEffect(() => {
    // Fetch available models
    refactoringService.getModels()
      .then(data => {
        setAvailableModels(data);
        if (data.ollama && data.ollama.length > 0) {
          setModelName(data.ollama[0].model_id);
        }
      })
      .catch(err => console.error('Error fetching models:', err));

    // Fetch available smells
    refactoringService.getSmells()
      .then(data => {
        setAvailableSmells(data.smells);
        // Keep default as 'All'
      })
      .catch(err => console.error('Error fetching smells:', err));

    // Check health status
    refactoringService.checkHealth()
      .then(data => setHealthStatus(data))
      .catch(err => console.error('Error checking health:', err));
  }, []);

  const handleModelTypeChange = (type) => {
    setModelType(type);
    // Set default model for the selected type
    if (type === 'ollama') {
      // For Ollama, always use Llama 3.2
      setModelName('llama3.2');
    } else {
      setModelName(availableModels.huggingface[0]?.model_id || 'mistralai/Mistral-7B-Instruct-v0.2');
    }
  };

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      // Read file content
      const reader = new FileReader();
      reader.onload = (event) => {
        setCode(event.target.result);
      };
      reader.readAsText(file);
    }
  };

  const handleRefactor = async () => {
    if (!code) {
      setError('Please provide test code to refactor');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await refactoringService.refactorCode({
        code,
        smell_name: selectedSmell,
        model_type: modelType,
        model_name: modelName,
        agent_mode: agentMode,
        temperature: 0.6
      });

      setResult(response);
    } catch (err) {
      setError(err.error || err.message || 'An error occurred during refactoring');
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    alert('Copied to clipboard!');
  };

  const clearAll = () => {
    setCode("");
    setSelectedFile(null);
    setResult(null);
    setError(null);
  };

  return (
    <>
    <div className="module-container">
      <div className="section">
        <h2>🔧 AI-Powered Test Code Refactorer</h2>
        <p className="subtitle">Refactor your test code to remove test smells using AI agents</p>

        {healthStatus && (
          <div className="health-status-banner">
            <span className={healthStatus.ollama_available ? 'status-ok' : 'status-error'}>
              🤖 Ollama: {healthStatus.ollama_available ? '✓ Available' : '✗ Not Available'}
            </span>
            <span className={healthStatus.huggingface_configured ? 'status-ok' : 'status-error'}>
              ☁️ HuggingFace: {healthStatus.huggingface_configured ? '✓ Configured' : '✗ Not Configured'}
            </span>
          </div>
        )}

        <div className="mode-selector">
          <button
            className={`mode-btn ${mode === "code" ? "active" : ""}`}
            onClick={() => setMode("code")}
          >
            📝 Paste Code
          </button>
          <button
            className={`mode-btn ${mode === "file" ? "active" : ""}`}
            onClick={() => setMode("file")}
          >
            📄 Upload File
          </button>
        </div>

        {mode === "code" && (
          <div>
            <label className="input-label">Test Code:</label>
            <textarea
              className="code-input"
              placeholder="Paste your test code here..."
              value={code}
              onChange={(e) => setCode(e.target.value)}
              rows={15}
            />
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
              <span>📄 Choose Python Test File</span>
            </label>
            {selectedFile && (
              <div className="file-info">
                <p><strong>Selected File:</strong> {selectedFile.name}</p>
                <p><strong>Size:</strong> {(selectedFile.size / 1024).toFixed(2)} KB</p>
              </div>
            )}
            {code && (
              <div>
                <label className="input-label">File Content:</label>
                <textarea
                  className="code-input"
                  value={code}
                  onChange={(e) => setCode(e.target.value)}
                  rows={15}
                />
              </div>
            )}
          </div>
        )}

        <div className="refactoring-config-inline">
          <h3>⚙️ Refactoring Settings</h3>
          
          <div className="config-grid">
            <div className="config-item">
              <label>Test Smell Type:</label>
              <select 
                value={selectedSmell} 
                onChange={(e) => setSelectedSmell(e.target.value)}
                disabled={loading}
              >
                <option value="All">All Test Smells</option>
                {availableSmells.map((smell, idx) => (
                  <option key={idx} value={smell}>{smell}</option>
                ))}
              </select>
            </div>

            <div className="config-item">
              <label>Agent Mode:</label>
              <select 
                value={agentMode} 
                onChange={(e) => setAgentMode(e.target.value)}
                disabled={loading}
              >
                <option value="single">Single Agent (Fast)</option>
                <option value="multi">Multi Agent (Thorough)</option>
              </select>
            </div>

            <div className="config-item">
              <label>Model Type:</label>
              <select 
                value={modelType} 
                onChange={(e) => handleModelTypeChange(e.target.value)}
                disabled={loading}
              >
                <option value="ollama">Ollama (Local)</option>
                <option value="huggingface">HuggingFace API</option>
              </select>
            </div>

            <div className="config-item">
              <label>Model Name:</label>
              <select 
                value={modelName} 
                onChange={(e) => setModelName(e.target.value)}
                disabled={loading || modelType === 'ollama'}
              >
                {modelType === 'ollama' 
                  ? (
                      <option value="llama3.2">Llama 3.2</option>
                    )
                  : availableModels.huggingface.map(model => (
                      <option key={model.model_id} value={model.model_id}>
                        {model.name}
                      </option>
                    ))
                }
              </select>
            </div>
          </div>

          <div className="action-buttons">
            <button 
              onClick={handleRefactor}
              disabled={loading || !code}
              className="btn btn-primary"
            >
              {loading ? '🔄 Refactoring...' : `✨ Refactor with ${agentMode === 'single' ? 'Single' : 'Multi'} Agent`}
            </button>
            <button 
              onClick={clearAll}
              disabled={loading}
              className="btn btn-secondary"
            >
              🗑️ Clear All
            </button>
          </div>
        </div>
      </div>

      {error && (
        <div className="section">
          <div className="error-box">
            <h3>❌ Error</h3>
            <p>{error}</p>
          </div>
        </div>
      )}

      {result && (
        <div className="section">
          <div className="refactoring-results">
            <div className="result-header">
              <h3>✅ Refactoring Complete</h3>
              {result.error && <p className="warning">⚠️ {result.error}</p>}
              <button
                className="btn btn-primary"
                style={{ marginTop: 8 }}
                onClick={() => setShowSaveModal(true)}
              >
                💾 Save to Project
              </button>
            </div>

            <div className="code-comparison">
              <div className="code-panel">
                <div className="code-panel-header">
                  <h4>📄 Original Code</h4>
                </div>
                <pre><code>{code}</code></pre>
              </div>

              <div className="code-panel">
                <div className="code-panel-header">
                  <h4>✨ Refactored Code</h4>
                  <button 
                    onClick={() => copyToClipboard(result.refactored_code)}
                    className="btn-copy-small"
                  >
                    📋 Copy
                  </button>
                </div>
                <pre><code>{result.refactored_code}</code></pre>
              </div>
            </div>

            {result.detection_results && agentMode === 'multi' && (
              <div className="multi-agent-process">
                <h4>🔍 Multi-Agent Process Details</h4>
                {result.detection_results.map((item, idx) => (
                  <div key={idx} className="process-step">
                    <h5>
                      {item.phase === 'refactor' ? '🔧' : '🔎'} 
                      {item.phase === 'refactor' ? ' Refactoring' : ' Detection'} Step {item.iteration}
                    </h5>
                    
                    {/* Detection Phase */}
                    {item.detected_smell !== undefined && (
                      <>
                        <div className="step-summary">
                          <p><strong>Smell Detected:</strong> 
                            <span className={item.detected_smell === 'YES' ? 'badge-yes' : 'badge-no'}>
                              {item.detected_smell}
                            </span>
                          </p>
                          <p><strong>Evaluator Agreed:</strong> 
                            <span className={item.agreed_with_detection === 'YES' ? 'badge-yes' : 'badge-no'}>
                              {item.agreed_with_detection}
                            </span>
                          </p>
                        </div>
                        
                        {item.detection_response && (
                          <details className="step-details">
                            <summary>🔍 Detection Response</summary>
                            <pre>{item.detection_response}</pre>
                          </details>
                        )}
                        
                        {item.evaluation_response && (
                          <details className="step-details">
                            <summary>✅ Evaluation Feedback</summary>
                            <pre>{item.evaluation_response}</pre>
                          </details>
                        )}
                      </>
                    )}
                    
                    {/* Refactoring Phase */}
                    {item.approved !== undefined && (
                      <>
                        <div className="step-summary">
                          <p><strong>Approved:</strong> 
                            <span className={item.approved === 'YES' ? 'badge-yes' : 'badge-no'}>
                              {item.approved}
                            </span>
                          </p>
                        </div>
                        
                        {item.refactored_code && (
                          <details className="step-details">
                            <summary>🔧 Refactored Code (Iteration {item.iteration})</summary>
                            <pre><code>{item.refactored_code}</code></pre>
                          </details>
                        )}
                        
                        {item.evaluation && (
                          <details className="step-details">
                            <summary>📝 Code Review</summary>
                            <pre>{item.evaluation}</pre>
                          </details>
                        )}
                      </>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>

    {showSaveModal && (
      <SaveVersionModal
        open={showSaveModal}
        onClose={() => setShowSaveModal(false)}
        onSaved={() => setShowSaveModal(false)}
        step="refactored"
        defaultLabel="After refactoring"
        data={{
          test_code:       code,
          refactored_code: result?.refactored_code || '',
          refactor_model:  modelName,
          refactor_smell:  selectedSmell,
        }}
      />
    )}

      {/* Floating report button — visible once code is present */}
      {code && (
        <button
          onClick={() => setReportModalOpen(true)}
          title="Generate Pipeline Report"
          style={{
            position: 'fixed', bottom: 28, right: 28, zIndex: 1000,
            background: 'linear-gradient(135deg,#1a237e,#283593)',
            color: '#fff', border: 'none', borderRadius: 50,
            width: 56, height: 56, fontSize: '1.4rem',
            cursor: 'pointer', boxShadow: '0 4px 16px rgba(0,0,0,.3)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
          }}
        >
          📄
        </button>
      )}

      <PipelineReportModal
        open={reportModalOpen}
        onClose={() => setReportModalOpen(false)}
        pipelineData={{
          username:       authService.getUser()?.username || '',
          inputMode:      mode,
          sourceFilename: selectedFile?.name || 'code.py',
          sourceCode:     code,
          refactorResult: result ? {
            smell_targeted:    selectedSmell,
            agent_mode:        agentMode,
            model_type:        modelType,
            model_name:        modelName,
            original_code:     code,
            refactored_code:   result.refactored_code,
            detection_results: result.detection_results || [],
          } : null,
        }}
      />
    </>
  );
}

export default TestRefactorer;
