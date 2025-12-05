import React, { useState } from "react";
import axios from "axios";

function App() {
  const [code, setCode] = useState("");
  const [testCode, setTestCode] = useState("");
  const [loading, setLoading] = useState(false);
  
  const [logs, setLogs] = useState([]);
  const [taskId, setTaskId] = useState(null);
  const [es, setEs] = useState(null);
  const [useAI, setUseAI] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    setTestCode("");
    setLogs([]);
    setTaskId(null);
    // Start generation task
    try {
      if (useAI) {
        // Use AI-based generation (direct response)
        const resp = await axios.post("http://127.0.0.1:5000/generate-ai-tests", { code });
        setTestCode(resp.data.test_code);
        setLoading(false);
        return;
      }
      
      // Use Pynguin-based generation (streaming)
      const resp = await axios.post("http://127.0.0.1:5000/generate-tests", { code });
      const tid = resp.data.task_id;
      setTaskId(tid);

      // Open EventSource to stream logs/results
      const url = `http://127.0.0.1:5000/generate-tests/stream/${tid}`;
      const source = new EventSource(url);
      setEs(source);

      source.onmessage = (e) => {
        try {
          const obj = JSON.parse(e.data);
          if (obj.type === 'log') {
            setLogs((prev) => [...prev, obj.line]);
          } else if (obj.type === 'result') {
            setTestCode(obj.test_code);
          } else if (obj.type === 'error') {
            setLogs((prev) => [...prev, `ERROR: ${obj.message}`]);
          } else if (obj.type === 'done') {
            // finished
            setLoading(false);
            source.close();
            setEs(null);
          }
        } catch (err) {
          // fallback: append raw data
          setLogs((prev) => [...prev, e.data]);
        }
      };

      source.onerror = (err) => {
        console.error('EventSource error', err);
        setLogs((prev) => [...prev, 'Connection to server lost.']);
        setLoading(false);
        if (source) source.close();
        setEs(null);
      };

    } catch (err) {
      console.error(err);
      alert("Error starting generation task");
      setLoading(false);
    }
  };

  const handleDownload = () => {
    const blob = new Blob([testCode], { type: "text/python" });
    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "test_user_code.py";
    link.click();
  };


  return (
    <div style={{ padding: "20px" }}>
      <h1>Python Test Generator</h1>
      <div style={{ marginBottom: "10px" }}>
        <label style={{ marginRight: "10px" }}>
          <input
            type="radio"
            checked={!useAI}
            onChange={() => setUseAI(false)}
            name="generator"
          />
          Use Pynguin (Automatic)
        </label>
        <label>
          <input
            type="radio"
            checked={useAI}
            onChange={() => setUseAI(true)}
            name="generator"
          />
          Use AI (OpenAI/HuggingFace)
        </label>
      </div>
      <textarea
        placeholder="Paste your Python code here..."
        value={code}
        onChange={(e) => setCode(e.target.value)}
        style={{ width: "100%", height: "200px" }}
      ></textarea>
      <br />
      <button onClick={handleSubmit} disabled={loading} style={{ marginTop: "10px" }}>
        {loading ? "Generating..." : "Generate Tests"}
      </button>

      {testCode && (
        <div style={{ marginTop: "20px" }}>
          <h2>Generated Tests</h2>
          <pre style={{ background: "#f0f0f0", padding: "10px" }}>{testCode}</pre>
          <button onClick={handleDownload} style={{ marginTop: "10px" }}>
            Download Test File
          </button>
        </div>
      )}

      {!useAI && (
        <div style={{ marginTop: "20px" }}>
          <h2>Generation Logs</h2>
          <div style={{ background: "#111", color: "#0f0", padding: "10px", height: "240px", overflow: "auto", fontFamily: "monospace" }}>
            {logs.length === 0 && <div style={{ color: '#aaa' }}>{loading ? 'Waiting for logs...' : 'No logs yet.'}</div>}
            {logs.map((l, idx) => (
              <div key={idx}>{l}</div>
            ))}
          </div>
        </div>
      )}

      {/* Symbols UI removed as requested */}
    </div>
  );
}

export default App;
