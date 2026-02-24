import React, { useState, useEffect } from 'react';
import projectService from '../services/projectService';


function SaveVersionModal({ open, onClose, onSaved, step, data, defaultLabel = '' }) {
  const [projects, setProjects]   = useState([]);
  const [projectId, setProjectId] = useState('');
  const [newName, setNewName]     = useState('');
  const [label, setLabel]         = useState('');
  const [saving, setSaving]       = useState(false);
  const [error, setError]         = useState('');

  useEffect(() => {
    if (!open) return;
    setLabel(defaultLabel);
    setError('');
    projectService.getProjects()
      .then(setProjects)
      .catch(() => {});
  }, [open, defaultLabel]);

  if (!open) return null;

  const handleSave = async () => {
    setError('');
    let pid = projectId;

    if (!pid && !newName.trim()) {
      setError('Select an existing project or enter a new project name.');
      return;
    }
    if (!label.trim()) {
      setError('Please enter a version label.');
      return;
    }

    setSaving(true);
    try {
      if (!pid) {
        const created = await projectService.createProject(newName.trim());
        pid = created.id;
      }
      const ver = await projectService.saveVersion(pid, label.trim(), step, data);
      onSaved(pid, ver.id, label.trim());
      onClose();
    } catch (err) {
      setError(err?.response?.data?.error || err.message || 'Save failed');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div style={styles.overlay} onClick={onClose}>
      <div style={styles.modal} onClick={e => e.stopPropagation()}>
        <h3 style={{ marginTop: 0 }}>💾 Save Version</h3>

        {/* Project selection */}
        <label style={styles.label}>Project</label>
        <select
          style={styles.input}
          value={projectId}
          onChange={e => { setProjectId(e.target.value); setNewName(''); }}
        >
          <option value="">— Create new project —</option>
          {projects.map(p => (
            <option key={p.id} value={p.id}>{p.name}</option>
          ))}
        </select>

        {!projectId && (
          <>
            <label style={styles.label}>New project name</label>
            <input
              style={styles.input}
              placeholder="e.g. Triangle Area Tests"
              value={newName}
              onChange={e => setNewName(e.target.value)}
            />
          </>
        )}

        {/* Version label */}
        <label style={styles.label}>Version label</label>
        <input
          style={styles.input}
          placeholder="e.g. After Pynguin generation"
          value={label}
          onChange={e => setLabel(e.target.value)}
        />

        {/* Step badge */}
        <div style={{ marginBottom: 12 }}>
          <span style={styles.stepBadge}>{STEP_LABELS[step] || step}</span>
        </div>

        {error && <p style={{ color: '#c0392b', marginBottom: 10 }}>{error}</p>}

        <div style={{ display: 'flex', gap: 10, justifyContent: 'flex-end' }}>
          <button className="btn btn-secondary" onClick={onClose} disabled={saving}>Cancel</button>
          <button className="btn btn-primary" onClick={handleSave} disabled={saving}>
            {saving ? 'Saving…' : '💾 Save'}
          </button>
        </div>
      </div>
    </div>
  );
}

const STEP_LABELS = {
  source:          '📄 Source Code',
  test_generated:  '🚀 Test Generated',
  smell_detected:  '🔍 Smell Detected',
  refactored:      '✨ Refactored',
};

const styles = {
  overlay: {
    position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.5)',
    display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000,
  },
  modal: {
    background: '#fff', borderRadius: 10, padding: 28, width: 420,
    maxWidth: '90vw', boxShadow: '0 8px 32px rgba(0,0,0,0.18)',
  },
  label: { display: 'block', fontWeight: 600, marginBottom: 4, fontSize: 13 },
  input: {
    width: '100%', padding: '8px 10px', borderRadius: 6,
    border: '1px solid #ccc', fontSize: 14, marginBottom: 14, boxSizing: 'border-box',
  },
  stepBadge: {
    background: '#eef', color: '#336', padding: '3px 10px',
    borderRadius: 12, fontSize: 12, fontWeight: 600,
  },
};

export default SaveVersionModal;
