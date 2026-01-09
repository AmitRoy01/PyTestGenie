import React, { useState } from "react";
import axios from "axios";

const API_BASE = "http://127.0.0.1:5000/api/test-generator";

function TestGenerator() {
  const [code, setCode] = useState("");
  const [testCode, setTestCode] = useState("");
  const [loading, setLoading] = useState(false);
  const [logs, setLogs] = useState([]);
  const [useAI, setUseAI] = useState(false);
  const [canDetectSmells, setCanDetectSmells] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    setTestCode("");
    setLogs([]);
    setCanDetectSmells(false);

    try {
      if (useAI) {
        // AI-based generation
        const resp = await axios.post(`${API_BASE}/generate-tests/ai`, { code });
        setTestCode(resp.data.test_code);
        setCanDetectSmells(true);
        setLoading(false);
      } else {
        // Pynguin-based generation with streaming
        const resp = await axios.post(`${API_BASE}/generate-tests/pynguin`, { code });
        const taskId = resp.data.task_id;

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
        "http://127.0.0.1:5000/api/smell-detector/analyze/code",
        { code: testCode, filename: "generated_test.py" }
      );

      if (resp.data.status === "success") {
        alert(`Analysis complete! Found ${resp.data.total_smells} test smell(s).`);
        // Open report in new tab
        window.open("http://127.0.0.1:5000/api/smell-detector/report", "_blank");
      }
    } catch (err) {
      alert("Error detecting smells: " + err.message);
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
            <span>🤖 Pynguin (Automatic)</span>
          </label>
          <label className="radio-label">
            <input
              type="radio"
              checked={useAI}
              onChange={() => setUseAI(true)}
            />
            <span>🧠 AI (OpenAI/HuggingFace)</span>
          </label>
        </div>

        <textarea
          className="code-input"
          placeholder="Paste your Python code here..."
          value={code}
          onChange={(e) => setCode(e.target.value)}
        />

        <button 
          className="btn btn-primary" 
          onClick={handleGenerate} 
          disabled={loading || !code}
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
        </div>
      )}
    </div>
  );
}

export default TestGenerator;
