import React, { useState, useEffect, useRef } from "react";
import refactoringService from "../services/refactoringService";

function RefactoringPanel({ code, detectedSmells }) {
  const [agentMode, setAgentMode] = useState("single");
  const [selectedSmell, setSelectedSmell] = useState("All");
  const [modelType, setModelType] = useState("ollama");
  const [modelName, setModelName] = useState("llama3.2");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [availableModels, setAvailableModels] = useState({ ollama: [], huggingface: [] });
  const [healthStatus, setHealthStatus] = useState(null);
  const abortControllerRef = useRef(null);

  useEffect(() => {
    // Fetch available models
    refactoringService.getModels()
      .then(data => setAvailableModels(data))
      .catch(err => console.error('Error fetching models:', err));

    // Check health status
    refactoringService.checkHealth()
      .then(data => setHealthStatus(data))
      .catch(err => console.error('Error checking health:', err));

    // Set first detected smell as default selection
    if (detectedSmells && detectedSmells.length > 0) {
      setSelectedSmell(detectedSmells[0].type);
    }
  }, [detectedSmells]);

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

  const handleRefactor = async () => {
    if (!code || !selectedSmell) {
      setError('Please provide code and select a smell type');
      return;
    }

    // Create a new AbortController for this request
    const controller = new AbortController();
    abortControllerRef.current = controller;

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
        temperature: 0.6,
        signal: controller.signal
      });

      setResult(response);
    } catch (err) {
      // Ignore abort errors — user cancelled intentionally
      if (err?.code === 'ERR_CANCELED' || err?.name === 'AbortError' || err?.name === 'CanceledError') {
        return;
      }
      setError(err.error || err.message || 'An error occurred during refactoring');
    } finally {
      setLoading(false);
      abortControllerRef.current = null;
    }
  };

  const handleCancel = () => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
      abortControllerRef.current = null;
    }
    setLoading(false);
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    alert('Copied to clipboard!');
  };

  if (!code) {
    return (
      <div className="refactoring-panel-empty">
        <p>⚠️ No test code available for refactoring.</p>
        <p>Please detect test smells first to enable refactoring.</p>
      </div>
    );
  }

  return (
    <div className="refactoring-panel">
      <div className="refactoring-header">
        <h3>🔧 AI-Powered Test Code Refactoring</h3>
        {healthStatus && (
          <div className="health-status-small">
            <span className={healthStatus.ollama_available ? 'status-ok' : 'status-error'}>
              Ollama: {healthStatus.ollama_available ? '✓' : '✗'}
            </span>
            <span className={healthStatus.huggingface_configured ? 'status-ok' : 'status-error'}>
              HuggingFace: {healthStatus.huggingface_configured ? '✓' : '✗'}
            </span>
          </div>
        )}
      </div>

      <div className="refactoring-config">
        <div className="config-section">
          <h4>Refactoring Settings</h4>
          
          <div className="config-grid">
            <div className="config-item">
              <label>Test Smell Type:</label>
              <select 
                value={selectedSmell} 
                onChange={(e) => setSelectedSmell(e.target.value)}
                disabled={loading}
              >
                {detectedSmells && detectedSmells.length > 0 ? (
                  <>
                    <option value="All">All Test Smells</option>
                    {detectedSmells.map((smell, idx) => (
                      <option key={idx} value={smell.type}>{smell.type}</option>
                    ))}
                  </>
                ) : (
                  <>
                    <option value="All">All Test Smells</option>
                    <option value="Assertion Roulette">Assertion Roulette</option>
                    <option value="Magic Number Test">Magic Number Test</option>
                    <option value="Duplicate Assert">Duplicate Assert</option>
                    <option value="Exception Handling">Exception Handling</option>
                    <option value="Conditional Test Logic">Conditional Test Logic</option>
                    <option value="Missing Assertion">Missing Assertion</option>
                  </>
                )}
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

          <button 
            onClick={handleRefactor}
            disabled={loading || !code || !selectedSmell}
            className="btn btn-primary refactor-button"
          >
            {loading ? '🔄 Refactoring...' : `✨ Refactor with ${agentMode === 'single' ? 'Single' : 'Multi'} Agent`}
          </button>
          {loading && (
            <button
              onClick={handleCancel}
              className="btn btn-danger"
              style={{ marginLeft: '10px' }}
            >
              ✖ Cancel
            </button>
          )}
        </div>
      </div>

      {error && (
        <div className="error-box">
          <h4>❌ Error</h4>
          <p>{error}</p>
        </div>
      )}

      {result && (
        <div className="refactoring-results">
          <div className="result-header">
            <h3>✅ Refactoring Complete</h3>
            {result.error && <p className="warning">⚠️ {result.error}</p>}
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
      )}
    </div>
  );
}

export default RefactoringPanel;
