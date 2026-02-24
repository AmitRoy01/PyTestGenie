/**
 * pipelineReportGenerator.js
 * Generates a fully self-contained, styled HTML pipeline report from the
 * current state of the TestGenerator (or any subset of completed stages).
 */

const esc = (s) =>
  String(s ?? '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');

const codeFence = (code, lang = 'python') =>
  code
    ? `<pre class="code-block"><code class="lang-${lang}">${esc(code)}</code></pre>`
    : '<p class="empty-note">— not available —</p>';

const badge = (label, color = '#555') =>
  `<span class="badge" style="background:${color}">${esc(label)}</span>`;

const smellColor = (type = '') => {
  const map = {
    'Assertion Roulette': '#c0392b',
    'Conditional Test Logic': '#8e44ad',
    'Exception Handling': '#2980b9',
    'Redundant Print': '#16a085',
    'Sleepy Test': '#d35400',
    'Unknown Test': '#7f8c8d',
    'Verbose Test': '#c0392b',
    'Verifying in Setup': '#8e44ad',
    'Non-Functional Statement': '#7f8c8d',
    'Undefined Test': '#95a5a6',
    'Magic Number Test': '#e67e22',
    'Duplicate Assert': '#2980b9',
  };
  return map[type] || '#555';
};

// ─────────────────────────────────────────────────────────────────────────────
// Main export
// ─────────────────────────────────────────────────────────────────────────────

/**
 * @param {object} data
 * @param {string}  data.username            - logged-in user
 * @param {string}  data.title               - report title
 *
 * [Stage 1 – Input]
 * @param {string}  data.inputMode           - paste | file | project
 * @param {string}  data.sourceFilename      - file name
 * @param {string}  data.sourceCode          - raw source code
 *
 * [Stage 2 – Test Generation]
 * @param {boolean} data.useAI
 * @param {string}  data.algorithm           - pynguin algorithm
 * @param {string}  data.aiModel             - AI model key
 * @param {string[]} data.logs               - pynguin logs
 * @param {string}  data.testCode            - generated test code
 *
 * [Stage 3 – Smell Detection]
 * @param {object|null} data.smellResults
 *   { detection_method, model_used, total_smells, smells: [{type,method,lines?,explanation?}] }
 *
 * [Stage 4 – Refactoring]
 * @param {object|null} data.refactorResult
 *   { smell_targeted, agent_mode, model_type, model_name, original_code, refactored_code }
 */
export function generatePipelineReportHTML(data) {
  const {
    username = 'Unknown User',
    title    = 'Pipeline Report',
    // Stage 1
    inputMode      = 'paste',
    sourceFilename = 'code.py',
    sourceCode     = '',
    // Stage 2
    useAI      = false,
    algorithm  = '',
    aiModel    = '',
    logs       = [],
    testCode   = '',
    // Stage 3
    smellResults   = null,
    // Stage 4
    refactorResult = null,
  } = data;

  const now       = new Date().toLocaleString();
  const stages    = [];
  if (sourceCode)    stages.push('Input');
  if (testCode)      stages.push('Test Generation');
  if (smellResults)  stages.push('Smell Detection');
  if (refactorResult) stages.push('Refactoring');

  // ── Stage 1: Input ────────────────────────────────────────────────────────
  const inputModeLabel = { paste: 'Paste Code', file: 'File Upload', project: 'Project Upload' }[inputMode] || inputMode;
  const s1 = `
  <section class="stage" id="stage-input">
    <div class="stage-header" style="background:#1565c0">
      <span class="stage-num">01</span>
      <h2>📥 Input</h2>
      <span class="stage-badge">Source Code</span>
    </div>
    <div class="stage-body">
      <div class="meta-grid">
        <div class="meta-item"><span class="meta-label">Input Mode</span><span class="meta-val">${esc(inputModeLabel)}</span></div>
        <div class="meta-item"><span class="meta-label">Filename</span><span class="meta-val">${esc(sourceFilename)}</span></div>
      </div>
      <h4>Source Code</h4>
      ${codeFence(sourceCode)}
    </div>
  </section>`;

  // ── Stage 2: Test Generation ──────────────────────────────────────────────
  let s2 = '';
  if (testCode || logs.length) {
    const genMethod = useAI
      ? `🧠 AI-Based &nbsp;${badge(aiModel === 'gpt-oss' ? 'GPT-OSS 20B (HuggingFace)' : 'Llama 3.2 (Ollama)', '#1565c0')}`
      : `🤖 Rule-Based (Pynguin) &nbsp;${badge(algorithm || 'DYNAMOSA', '#2e7d32')}`;

    const logsHtml = logs.length
      ? `<div class="log-block">${logs.map(l => `<div class="log-line">${esc(l)}</div>`).join('')}</div>`
      : '';

    s2 = `
  <section class="stage" id="stage-gen">
    <div class="stage-header" style="background:#2e7d32">
      <span class="stage-num">02</span>
      <h2>🚀 Test Generation</h2>
      <span class="stage-badge">Generated Tests</span>
    </div>
    <div class="stage-body">
      <div class="meta-grid">
        <div class="meta-item"><span class="meta-label">Method</span><span class="meta-val">${genMethod}</span></div>
      </div>
      ${logsHtml ? '<h4>Generation Logs</h4>' + logsHtml : ''}
      <h4>Generated Test Code</h4>
      ${codeFence(testCode)}
    </div>
  </section>`;
  }

  // ── Stage 3: Smell Detection ───────────────────────────────────────────────
  let s3 = '';
  if (smellResults) {
    const { detection_method, model_used, total_smells = 0, smells = [] } = smellResults;
    const methodLabel = detection_method === 'llm_based'
      ? `🧠 LLM-Based &nbsp;${badge(model_used || 'llama3.2', '#e65100')}`
      : '📏 Rule-Based';

    const smellRows = smells.length
      ? smells.map((s, i) => `
          <div class="smell-card">
            <div class="smell-card-header">
              <span class="smell-badge" style="background:${smellColor(s.type)}">${esc(s.type)}</span>
              <span class="smell-method">📌 ${esc(s.method)}</span>
              ${s.lines && s.lines.length ? `<span class="smell-lines">Line ${esc(String(s.lines))}</span>` : ''}
            </div>
            ${s.explanation ? `<div class="smell-explanation">${esc(s.explanation)}</div>` : ''}
          </div>`).join('')
      : '<p class="empty-note">✅ No smells detected.</p>';

    s3 = `
  <section class="stage" id="stage-smell">
    <div class="stage-header" style="background:#e65100">
      <span class="stage-num">03</span>
      <h2>🔍 Smell Detection</h2>
      <span class="stage-badge">${total_smells} smell${total_smells !== 1 ? 's' : ''} found</span>
    </div>
    <div class="stage-body">
      <div class="meta-grid">
        <div class="meta-item"><span class="meta-label">Method</span><span class="meta-val">${methodLabel}</span></div>
        <div class="meta-item"><span class="meta-label">Total Smells</span><span class="meta-val">${total_smells}</span></div>
      </div>
      <h4>Detected Smells</h4>
      <div class="smell-list">${smellRows}</div>
    </div>
  </section>`;
  }

  // ── Stage 4: Refactoring ──────────────────────────────────────────────────
  let s4 = '';
  if (refactorResult) {
    const {
      smell_targeted, agent_mode, model_type, model_name,
      original_code, refactored_code,
      detection_results = [],
    } = refactorResult;

    // ── Multi-agent process details ──────────────────────────────────────
    const multiAgentHtml = (agent_mode === 'multi' && detection_results.length)
      ? `<div class="ma-wrapper">
          <h4>🔍 Multi-Agent Process Details</h4>
          ${detection_results.map((item, i) => {
            const isDetect  = item.detected_smell !== undefined;
            const isRefactor = item.approved !== undefined;
            const icon  = isRefactor ? '🔧' : '🔎';
            const label = isRefactor ? 'Refactoring' : 'Detection';

            const detectionBody = isDetect ? `
              <div class="ma-badges">
                <span class="ma-label">Smell Detected:</span>
                <span class="badge ${item.detected_smell === 'YES' ? 'badge-yes' : 'badge-no'}">${esc(item.detected_smell)}</span>
                &nbsp;
                <span class="ma-label">Evaluator Agreed:</span>
                <span class="badge ${item.agreed_with_detection === 'YES' ? 'badge-yes' : 'badge-no'}">${esc(item.agreed_with_detection)}</span>
              </div>
              ${item.detection_response  ? `<details class="ma-details"><summary>🔍 Detection Response</summary><pre class="ma-pre">${esc(item.detection_response)}</pre></details>` : ''}
              ${item.evaluation_response ? `<details class="ma-details"><summary>✅ Evaluation Feedback</summary><pre class="ma-pre">${esc(item.evaluation_response)}</pre></details>` : ''}
            ` : '';

            const refactorBody = isRefactor ? `
              <div class="ma-badges">
                <span class="ma-label">Approved:</span>
                <span class="badge ${item.approved === 'YES' ? 'badge-yes' : 'badge-no'}">${esc(item.approved)}</span>
              </div>
              ${item.refactored_code ? `<details class="ma-details"><summary>🔧 Refactored Code (Iteration ${esc(String(item.iteration))})</summary><pre class="code-block"><code>${esc(item.refactored_code)}</code></pre></details>` : ''}
              ${item.evaluation       ? `<details class="ma-details"><summary>📝 Code Review</summary><pre class="ma-pre">${esc(item.evaluation)}</pre></details>` : ''}
            ` : '';

            return `
            <div class="ma-step">
              <div class="ma-step-header">${icon} ${label} Step ${esc(String(item.iteration))}</div>
              ${detectionBody}${refactorBody}
            </div>`;
          }).join('')}
        </div>`
      : '';

    s4 = `
  <section class="stage" id="stage-refactor">
    <div class="stage-header" style="background:#6a1b9a">
      <span class="stage-num">04</span>
      <h2>🔧 Refactoring</h2>
      <span class="stage-badge">${esc(agent_mode === 'multi' ? 'Multi-Agent' : 'Single-Agent')} · Code Improved</span>
    </div>
    <div class="stage-body">
      <div class="meta-grid">
        <div class="meta-item"><span class="meta-label">Smell Targeted</span><span class="meta-val">${esc(smell_targeted || 'All')}</span></div>
        <div class="meta-item"><span class="meta-label">Agent Mode</span><span class="meta-val">${esc(agent_mode || 'single')}</span></div>
        <div class="meta-item"><span class="meta-label">Model</span><span class="meta-val">${esc(model_type)} / ${esc(model_name)}</span></div>
      </div>
      <div class="diff-wrapper">
        <div class="diff-col">
          <h4>📄 Original Test Code</h4>
          ${codeFence(original_code)}
        </div>
        <div class="diff-col">
          <h4>✨ Refactored Code</h4>
          ${codeFence(refactored_code)}
        </div>
      </div>
      ${multiAgentHtml}
    </div>
  </section>`;
  }

  // ── TOC ───────────────────────────────────────────────────────────────────
  const tocItems = [
    sourceCode && '<li><a href="#stage-input">01. Input</a></li>',
    (testCode || logs.length) && '<li><a href="#stage-gen">02. Test Generation</a></li>',
    smellResults && '<li><a href="#stage-smell">03. Smell Detection</a></li>',
    refactorResult && '<li><a href="#stage-refactor">04. Refactoring</a></li>',
  ].filter(Boolean).join('');

  // ── Full HTML ─────────────────────────────────────────────────────────────
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>${esc(title)} – PyTestGenie</title>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Segoe UI', Arial, sans-serif; background: #f4f6f9; color: #222; line-height:1.6; }

  .report-header {
    background: linear-gradient(135deg, #1a237e 0%, #283593 100%);
    color: #fff; padding: 32px 40px;
    display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;
  }
  .report-header h1 { font-size: 1.7rem; font-weight: 700; }
  .report-header .meta { font-size: 0.88rem; opacity: .85; margin-top: 4px; }
  .report-header .logo { font-size:2.4rem; }

  .toc {
    background:#fff; margin:24px 40px; border-radius:10px; padding:18px 24px;
    box-shadow:0 2px 8px rgba(0,0,0,.08);
  }
  .toc h3 { font-size:.95rem; color:#555; margin-bottom:10px; text-transform:uppercase; letter-spacing:.05em; }
  .toc ol { padding-left:20px; }
  .toc li { margin: 4px 0; }
  .toc a { color:#1565c0; text-decoration:none; font-weight:500; }
  .toc a:hover { text-decoration:underline; }

  .stage { margin: 0 40px 28px; border-radius:10px; overflow:hidden; box-shadow:0 2px 10px rgba(0,0,0,.1); }
  .stage-header {
    display:flex; align-items:center; gap:14px; padding:14px 20px; color:#fff;
  }
  .stage-header h2 { font-size:1.15rem; font-weight:600; flex:1; }
  .stage-num {
    background:rgba(255,255,255,.2); border-radius:50%; width:36px; height:36px;
    display:flex; align-items:center; justify-content:center; font-weight:700; font-size:.9rem; flex-shrink:0;
  }
  .stage-badge {
    background:rgba(255,255,255,.25); border-radius:20px; padding:3px 12px; font-size:.82rem; white-space:nowrap;
  }
  .stage-body { background:#fff; padding:24px; }
  .stage-body h4 { font-size:.93rem; color:#555; margin:18px 0 8px; text-transform:uppercase; letter-spacing:.04em; }
  .stage-body h4:first-child { margin-top:0; }

  .meta-grid { display:flex; flex-wrap:wrap; gap:12px; margin-bottom:16px; }
  .meta-item { background:#f5f7fa; border-radius:8px; padding:10px 16px; min-width:200px; }
  .meta-label { font-size:.78rem; color:#888; display:block; margin-bottom:2px; }
  .meta-val   { font-size:.93rem; font-weight:600; color:#222; }

  .code-block {
    background:#1e1e2e; color:#cdd6f4; border-radius:8px; padding:16px 18px;
    font-size:.82rem; overflow-x:auto; white-space:pre; line-height:1.55; font-family:'Cascadia Code','Fira Code',monospace;
    max-height:420px; overflow-y:auto;
  }

  .log-block {
    background:#111; color:#8bc34a; border-radius:8px; padding:12px 16px;
    font-size:.78rem; font-family:monospace; max-height:200px; overflow-y:auto; white-space:pre-wrap;
  }
  .log-line { line-height:1.6; }

  .smell-list { display:flex; flex-direction:column; gap:10px; }
  .smell-card { border:1px solid #e0e0e0; border-radius:8px; overflow:hidden; }
  .smell-card-header {
    display:flex; flex-wrap:wrap; align-items:center; gap:8px; padding:10px 14px; background:#fafafa;
  }
  .smell-badge { color:#fff; padding:3px 10px; border-radius:12px; font-size:.8rem; font-weight:600; }
  .smell-method { font-size:.88rem; font-weight:600; color:#333; }
  .smell-lines  { font-size:.8rem; color:#777; background:#f0f0f0; padding:2px 8px; border-radius:10px; }
  .smell-explanation {
    padding:10px 14px; font-size:.85rem; color:#444; line-height:1.6;
    border-top:1px solid #eee; white-space:pre-wrap;
    border-left:3px solid #e67e22; background:#fffdf5;
  }

  .diff-wrapper { display:grid; grid-template-columns:1fr 1fr; gap:16px; }
  @media(max-width:900px) { .diff-wrapper { grid-template-columns:1fr; } }

  .badge { color:#fff; padding:2px 9px; border-radius:10px; font-size:.8rem; font-weight:600; }
  .badge-yes { background:#2e7d32; color:#fff; padding:2px 9px; border-radius:10px; font-size:.8rem; font-weight:600; }
  .badge-no  { background:#c62828; color:#fff; padding:2px 9px; border-radius:10px; font-size:.8rem; font-weight:600; }
  .empty-note { color:#999; font-style:italic; font-size:.9rem; padding:8px 0; }

  /* Multi-agent process */
  .ma-wrapper { margin-top:22px; border-top:1px solid #e0e0e0; padding-top:18px; }
  .ma-wrapper h4 { font-size:.93rem; color:#555; margin-bottom:14px; text-transform:uppercase; letter-spacing:.04em; }
  .ma-step { border:1px solid #e8e0f0; border-radius:8px; margin-bottom:12px; overflow:hidden; }
  .ma-step-header {
    background:linear-gradient(90deg,#6a1b9a,#7b1fa2); color:#fff;
    padding:8px 14px; font-weight:600; font-size:.88rem;
  }
  .ma-badges { display:flex; gap:8px; align-items:center; flex-wrap:wrap; padding:10px 14px; background:#fafafa; border-bottom:1px solid #eee; }
  .ma-label  { font-size:.82rem; color:#555; font-weight:600; }
  .ma-details { padding:0 14px 10px; }
  .ma-details summary { cursor:pointer; font-size:.85rem; font-weight:600; color:#6a1b9a; padding:8px 0; user-select:none; }
  .ma-details summary:hover { color:#4a0072; }
  .ma-pre {
    background:#f5f5f5; border-radius:6px; padding:10px 12px;
    font-size:.8rem; font-family:monospace; white-space:pre-wrap;
    word-break:break-word; margin-top:6px; max-height:320px; overflow-y:auto;
    border:1px solid #e0e0e0;
  }

  .report-footer {
    text-align:center; padding:24px 40px; color:#888; font-size:.82rem; margin-top:8px;
  }
  @media print {
    body { background:#fff; }
    .stage { box-shadow:none; margin:0 0 20px; page-break-inside:avoid; }
    .report-header { print-color-adjust:exact; -webkit-print-color-adjust:exact; }
    .stage-header  { print-color-adjust:exact; -webkit-print-color-adjust:exact; }
  }
</style>
</head>
<body>

<header class="report-header">
  <div>
    <div style="font-size:1rem;opacity:.8;margin-bottom:4px;">PyTestGenie</div>
    <h1>${esc(title)}</h1>
    <div class="meta">
      👤 ${esc(username)} &nbsp;|&nbsp; 📅 Generated: ${esc(now)}
      &nbsp;|&nbsp; Stages: ${esc(stages.join(' → '))}
    </div>
  </div>
  <div class="logo">🧞</div>
</header>

<nav class="toc">
  <h3>Table of Contents</h3>
  <ol>${tocItems}</ol>
</nav>

${s1}
${s2}
${s3}
${s4}

<footer class="report-footer">
  PyTestGenie Pipeline Report &nbsp;·&nbsp; Generated on ${esc(now)} &nbsp;·&nbsp; User: ${esc(username)}
</footer>
</body>
</html>`;
}
