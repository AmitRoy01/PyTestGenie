import { useState, useEffect } from 'react';
import { generatePipelineReportHTML } from '../utils/pipelineReportGenerator';
import { saveReport } from '../services/reportArchiveService';

/**
 * PipelineReportModal
 *
 * Props:
 *   open         {boolean}  – controls visibility
 *   onClose      {function} – called when modal should close
 *   pipelineData {object}   – all pipeline state (see pipelineReportGenerator.js)
 */
export default function PipelineReportModal({ open, onClose, pipelineData = {} }) {
  const [html,    setHtml]    = useState('');
  const [title,   setTitle]   = useState('');
  const [saving,  setSaving]  = useState(false);
  const [saved,   setSaved]   = useState(false);
  const [saveErr, setSaveErr] = useState('');

  // Regenerate HTML whenever the modal opens
  useEffect(() => {
    if (!open) return;
    const defaultTitle = `Pipeline Report – ${new Date().toLocaleString()}`;
    setTitle(pipelineData.title || defaultTitle);
    setSaved(false);
    setSaveErr('');
    const generated = generatePipelineReportHTML({
      ...pipelineData,
      title: pipelineData.title || defaultTitle,
    });
    setHtml(generated);
  }, [open]); // eslint-disable-line react-hooks/exhaustive-deps

  if (!open) return null;

  // ── Actions ────────────────────────────────────────────────────────────────

  const handleView = () => {
    const blob = new Blob([html], { type: 'text/html' });
    const url  = URL.createObjectURL(blob);
    window.open(url, '_blank');
    // Revoke after a short delay so the tab has time to load it
    setTimeout(() => URL.revokeObjectURL(url), 10_000);
  };

  const handleDownload = () => {
    const blob     = new Blob([html], { type: 'text/html' });
    const url      = URL.createObjectURL(blob);
    const a        = document.createElement('a');
    a.href         = url;
    a.download     = `${title.replace(/[^a-z0-9_\- ]/gi, '_')}.html`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handleSave = async () => {
    setSaving(true);
    setSaveErr('');
    try {
      const stages       = [];
      if (pipelineData.sourceCode)     stages.push('input');
      if (pipelineData.testCode)       stages.push('test_generation');
      if (pipelineData.smellResults)   stages.push('smell_detection');
      if (pipelineData.refactorResult) stages.push('refactoring');

      const meta = {
        stages,
        total_smells: pipelineData.smellResults?.total_smells ?? 0,
        username:     pipelineData.username ?? '',
        input_mode:   pipelineData.inputMode ?? '',
        filename:     pipelineData.sourceFilename ?? '',
      };

      await saveReport(title, html, meta);
      setSaved(true);
    } catch (err) {
      setSaveErr(err?.response?.data?.error || err.message || 'Save failed');
    } finally {
      setSaving(false);
    }
  };

  // ── Styles (inline to keep component self-contained) ─────────────────────

  const overlay = {
    position: 'fixed', inset: 0,
    background: 'rgba(0,0,0,.55)',
    display: 'flex', alignItems: 'center', justifyContent: 'center',
    zIndex: 9999,
  };

  const dialog = {
    background: '#fff',
    borderRadius: 12,
    width: 520,
    maxWidth: '95vw',
    padding: '28px 30px',
    boxShadow: '0 8px 32px rgba(0,0,0,.25)',
    fontFamily: "'Segoe UI', Arial, sans-serif",
  };

  const inputStyle = {
    width: '100%', padding: '8px 12px',
    border: '1px solid #ccc', borderRadius: 6,
    fontSize: '.94rem', marginTop: 6, marginBottom: 16,
  };

  const btn = (bg, hoverBg) => ({
    padding: '9px 20px',
    borderRadius: 7, border: 'none',
    background: bg, color: '#fff',
    fontWeight: 600, fontSize: '.9rem',
    cursor: 'pointer',
  });

  return (
    <div style={overlay} onClick={(e) => e.target === e.currentTarget && onClose()}>
      <div style={dialog}>
        {/* Header */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 18 }}>
          <h2 style={{ fontSize: '1.15rem', color: '#1a237e' }}>📄 Generate Pipeline Report</h2>
          <button onClick={onClose} style={{ background: 'none', border: 'none', fontSize: '1.3rem', cursor: 'pointer', color: '#888' }}>✕</button>
        </div>

        {/* Title input */}
        <label style={{ fontSize: '.88rem', color: '#555', fontWeight: 600 }}>Report Title</label>
        <input
          type="text"
          style={inputStyle}
          value={title}
          onChange={(e) => { setTitle(e.target.value); setSaved(false); }}
          placeholder="Enter a title for this report"
        />

        {/* Summary chips */}
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, marginBottom: 20 }}>
          {pipelineData.sourceCode     && <Chip label="📥 Input"          bg="#1565c0" />}
          {pipelineData.testCode       && <Chip label="🚀 Tests Generated" bg="#2e7d32" />}
          {pipelineData.smellResults   && <Chip label={`🔍 ${pipelineData.smellResults.total_smells ?? 0} Smells`} bg="#e65100" />}
          {pipelineData.refactorResult && <Chip label="🔧 Refactored"     bg="#6a1b9a" />}
        </div>

        {/* Action buttons */}
        <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap' }}>
          <button style={btn('#1565c0')} onClick={handleView}>
            👁 View Report
          </button>
          <button style={btn('#37474f')} onClick={handleDownload}>
            ⬇️ Download HTML
          </button>
          <button
            style={btn(saved ? '#2e7d32' : '#6a1b9a')}
            onClick={handleSave}
            disabled={saving || saved}
          >
            {saving ? '⏳ Saving…' : saved ? '✅ Saved!' : '💾 Save to Archive'}
          </button>
        </div>

        {/* Error / success messages */}
        {saveErr && (
          <div style={{ marginTop: 12, color: '#c62828', fontSize: '.87rem' }}>
            ⚠️ {saveErr}
          </div>
        )}
        {saved && (
          <div style={{ marginTop: 12, color: '#2e7d32', fontSize: '.87rem', fontWeight: 600 }}>
            ✅ Report saved to archive! You can view it from the Report Archive page.
          </div>
        )}
      </div>
    </div>
  );
}

// Small helper chip
function Chip({ label, bg }) {
  return (
    <span style={{
      background: bg, color: '#fff',
      padding: '4px 12px', borderRadius: 20,
      fontSize: '.8rem', fontWeight: 600,
    }}>
      {label}
    </span>
  );
}
