import { useState, useEffect, useCallback } from 'react';
import { listReports, deleteReport, reportHtmlUrl, getReport } from '../services/reportArchiveService';

const STAGE_COLORS = {
  input:           { bg: '#1565c0', label: '📥 Input' },
  test_generation: { bg: '#2e7d32', label: '🚀 Tests' },
  smell_detection: { bg: '#e65100', label: '🔍 Smells' },
  refactoring:     { bg: '#6a1b9a', label: '🔧 Refactor' },
};

function StageBadge({ stage }) {
  const c = STAGE_COLORS[stage] || { bg: '#555', label: stage };
  return (
    <span style={{
      background: c.bg, color: '#fff',
      padding: '2px 9px', borderRadius: 12,
      fontSize: '.76rem', fontWeight: 600, marginRight: 4,
    }}>
      {c.label}
    </span>
  );
}

function fmtDate(iso) {
  if (!iso) return '—';
  return new Date(iso).toLocaleString();
}

export default function ReportArchive() {
  const [reports, setReports]     = useState([]);
  const [loading, setLoading]     = useState(true);
  const [error,   setError]       = useState('');
  const [deleting, setDeleting]   = useState(null);

  const load = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const res = await listReports();
      setReports(res.data.reports || []);
    } catch (err) {
      setError(err?.response?.data?.error || err.message || 'Failed to load reports');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const handleView = async (report) => {
    try {
      // Fetch the full report with HTML, then open as blob (avoids CORS/auth issues)
      const res  = await getReport(report.id);
      const html = res.data.html || '';
      const blob = new Blob([html], { type: 'text/html' });
      const url  = URL.createObjectURL(blob);
      window.open(url, '_blank');
      setTimeout(() => URL.revokeObjectURL(url), 15_000);
    } catch (err) {
      alert('Could not load report: ' + (err?.response?.data?.error || err.message));
    }
  };

  const handleDownload = async (report) => {
    try {
      const res  = await getReport(report.id);
      const html = res.data.html || '';
      const blob = new Blob([html], { type: 'text/html' });
      const url  = URL.createObjectURL(blob);
      const a    = document.createElement('a');
      a.href     = url;
      a.download = `${(report.title || 'report').replace(/[^a-z0-9_\- ]/gi, '_')}.html`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (err) {
      alert('Could not download: ' + (err?.response?.data?.error || err.message));
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this report from the archive?')) return;
    setDeleting(id);
    try {
      await deleteReport(id);
      setReports((prev) => prev.filter((r) => r.id !== id));
    } catch (err) {
      alert('Delete failed: ' + (err?.response?.data?.error || err.message));
    } finally {
      setDeleting(null);
    }
  };

  // ── Styles ────────────────────────────────────────────────────────────────
  const styles = {
    page:  { padding: '32px 40px', maxWidth: 1100, margin: '0 auto', fontFamily: "'Segoe UI', Arial, sans-serif" },
    heading: { fontSize: '1.5rem', fontWeight: 700, color: '#1a237e', marginBottom: 6 },
    sub:     { fontSize: '.9rem', color: '#666', marginBottom: 24 },
    card:  {
      background: '#fff', borderRadius: 10, boxShadow: '0 2px 8px rgba(0,0,0,.1)',
      padding: '18px 22px', marginBottom: 14,
      display: 'flex', alignItems: 'center', gap: 16, flexWrap: 'wrap',
    },
    info:   { flex: 1, minWidth: 200 },
    title:  { fontWeight: 700, fontSize: '1rem', color: '#222', marginBottom: 4 },
    meta:   { fontSize: '.82rem', color: '#666' },
    actions: { display: 'flex', gap: 8, flexShrink: 0 },
    btn:    (bg) => ({
      padding: '6px 14px', borderRadius: 6, border: 'none',
      background: bg, color: '#fff', fontWeight: 600, fontSize: '.83rem',
      cursor: 'pointer',
    }),
    empty: { textAlign: 'center', color: '#999', padding: '60px 0', fontSize: '1rem' },
  };

  return (
    <div style={styles.page}>
      <h1 style={styles.heading}>📋 Report Archive</h1>
      <p style={styles.sub}>All pipeline reports saved to your account.</p>

      <button
        onClick={load}
        style={{ ...styles.btn('#37474f'), marginBottom: 20, padding: '7px 18px' }}
      >
        🔄 Refresh
      </button>

      {loading && <p style={{ color: '#1565c0' }}>Loading reports…</p>}
      {error   && <p style={{ color: '#c62828' }}>⚠️ {error}</p>}

      {!loading && !error && reports.length === 0 && (
        <div style={styles.empty}>
          No saved reports yet. Use the "📄 Generate Report" button inside the Test Generator to save one.
        </div>
      )}

      {reports.map((r) => (
        <div key={r.id} style={styles.card}>
          {/* Info */}
          <div style={styles.info}>
            <div style={styles.title}>{r.title || 'Untitled Report'}</div>
            <div style={styles.meta}>
              📅 {fmtDate(r.created_at)}
              {r.meta?.filename ? `  ·  📄 ${r.meta.filename}` : ''}
              {r.meta?.total_smells != null ? `  ·  🔍 ${r.meta.total_smells} smell(s)` : ''}
            </div>
            <div style={{ marginTop: 6 }}>
              {(r.meta?.stages || []).map((s) => <StageBadge key={s} stage={s} />)}
            </div>
          </div>

          {/* Actions */}
          <div style={styles.actions}>
            <button style={styles.btn('#1565c0')} onClick={() => handleView(r)}>
              👁 View
            </button>
            <button style={styles.btn('#37474f')} onClick={() => handleDownload(r)}>
              ⬇️ Download
            </button>
            <button
              style={styles.btn(deleting === r.id ? '#999' : '#c62828')}
              onClick={() => handleDelete(r.id)}
              disabled={deleting === r.id}
            >
              {deleting === r.id ? '…' : '🗑 Delete'}
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}
