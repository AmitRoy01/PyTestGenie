import React, { useState, useEffect, useCallback } from 'react';
import projectService from '../services/projectService';

const STEP_ICONS = {
  source:         '📄',
  test_generated: '🚀',
  smell_detected: '🔍',
  refactored:     '✨',
};


 //onLoadVersion  {fn(versionData)}  — called when user clicks "Load"
 
function ProjectHistory({ onLoadVersion }) {
  const [projects, setProjects]         = useState([]);
  const [openProjectId, setOpenProject] = useState(null);
  const [versions, setVersions]         = useState({});   // {projectId: [...]}
  const [loading, setLoading]           = useState(false);
  const [deleting, setDeleting]         = useState(null);

  const fetchProjects = useCallback(() => {
    setLoading(true);
    projectService.getProjects()
      .then(setProjects)
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => { fetchProjects(); }, [fetchProjects]);

  const toggleProject = async (pid) => {
    if (openProjectId === pid) {
      setOpenProject(null);
      return;
    }
    setOpenProject(pid);
    if (!versions[pid]) {
      const vers = await projectService.getVersions(pid);
      setVersions(prev => ({ ...prev, [pid]: vers }));
    }
  };

  const handleDeleteProject = async (pid, name) => {
    if (!window.confirm(`Delete project "${name}" and all its versions?`)) return;
    setDeleting(pid);
    await projectService.deleteProject(pid);
    setProjects(prev => prev.filter(p => p.id !== pid));
    if (openProjectId === pid) setOpenProject(null);
    setDeleting(null);
  };

  const handleDeleteVersion = async (projectId, versionId, label) => {
    if (!window.confirm(`Delete version "${label}"?`)) return;
    setDeleting(versionId);
    try {
      await projectService.deleteVersion(versionId);
      setVersions(prev => ({
        ...prev,
        [projectId]: prev[projectId].filter(v => v.id !== versionId),
      }));
    } catch (err) {
      alert(err?.response?.data?.error || 'Cannot delete this version.');
    }
    setDeleting(null);
  };

  const handleLoad = async (versionId) => {
    try {
      const data = await projectService.loadVersion(versionId);
      onLoadVersion(data);
    } catch {
      alert('Failed to load version.');
    }
  };

  const refreshVersions = async (pid) => {
    const vers = await projectService.getVersions(pid);
    setVersions(prev => ({ ...prev, [pid]: vers }));
  };

  // Expose refresh so parent can call after saving
  ProjectHistory.refresh = fetchProjects;
  ProjectHistory.refreshVersions = refreshVersions;

  return (
    <div style={s.container}>
      <h2 style={{ marginTop: 0 }}>📂 My Projects</h2>

      {loading && <p style={{ color: '#888' }}>Loading…</p>}

      {!loading && projects.length === 0 && (
        <div style={s.empty}>
          <p>No saved projects yet.</p>
          <p style={{ fontSize: 13, color: '#888' }}>
            Use the 💾 Save Version button in any tool to save your work.
          </p>
        </div>
      )}

      {projects.map(project => (
        <div key={project.id} style={s.projectCard}>
          {/* Project header */}
          <div style={s.projectHeader}>
            <button style={s.projectTitle} onClick={() => toggleProject(project.id)}>
              {openProjectId === project.id ? '▾' : '▸'} {project.name}
            </button>
            <div style={{ display: 'flex', gap: 6, alignItems: 'center' }}>
              <span style={s.dateText}>{fmtDate(project.updated_at)}</span>
              <button
                style={s.btnDanger}
                disabled={deleting === project.id}
                onClick={() => handleDeleteProject(project.id, project.name)}
              >
                🗑️
              </button>
            </div>
          </div>

          {/* Versions list */}
          {openProjectId === project.id && (
            <div style={s.versionList}>
              {!versions[project.id] && <p style={{ padding: '8px 16px', color: '#888', fontSize: 13 }}>Loading…</p>}
              {versions[project.id] && versions[project.id].length === 0 && (
                <p style={{ padding: '8px 16px', color: '#888', fontSize: 13 }}>No versions saved.</p>
              )}
              {versions[project.id]?.map(ver => (
                <div key={ver.id} style={s.versionRow}>
                  <div style={s.versionLeft}>
                    <span style={s.versionNum}>v{ver.version_number}</span>
                    <span style={s.stepIcon}>{STEP_ICONS[ver.step] || '•'}</span>
                    <div>
                      <span style={s.versionLabel}>{ver.label}</span>
                      <span style={s.dateText}> · {fmtDate(ver.created_at)}</span>
                    </div>
                  </div>
                  <div style={{ display: 'flex', gap: 6 }}>
                    <button
                      style={s.btnLoad}
                      onClick={() => handleLoad(ver.id)}
                    >
                      ⬇️ Load
                    </button>
                    <button
                      style={s.btnDanger}
                      disabled={deleting === ver.id}
                      onClick={() => handleDeleteVersion(project.id, ver.id, ver.label)}
                    >
                      🗑️
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

function fmtDate(iso) {
  if (!iso) return '';
  const d = new Date(iso);
  return d.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' });
}

const s = {
  container: { padding: '10px 4px' },
  empty:     { textAlign: 'center', color: '#888', padding: 32 },
  projectCard: {
    border: '1px solid #e0e0e0', borderRadius: 8,
    marginBottom: 12, overflow: 'hidden', background: '#fff',
  },
  projectHeader: {
    display: 'flex', justifyContent: 'space-between', alignItems: 'center',
    padding: '10px 14px', background: '#f7f7f7',
  },
  projectTitle: {
    background: 'none', border: 'none', cursor: 'pointer',
    fontWeight: 700, fontSize: 15, color: '#333', textAlign: 'left',
  },
  dateText: { fontSize: 12, color: '#999' },
  versionList: { borderTop: '1px solid #eee' },
  versionRow: {
    display: 'flex', justifyContent: 'space-between', alignItems: 'center',
    padding: '8px 14px', borderBottom: '1px solid #f0f0f0',
    background: '#fff',
  },
  versionLeft: { display: 'flex', alignItems: 'center', gap: 8 },
  versionNum: {
    background: '#667eea', color: '#fff', borderRadius: 4,
    padding: '1px 6px', fontSize: 11, fontWeight: 700,
  },
  stepIcon: { fontSize: 16 },
  versionLabel: { fontWeight: 600, fontSize: 13, color: '#333' },
  btnLoad: {
    padding: '4px 10px', borderRadius: 6, border: '1px solid #667eea',
    background: 'transparent', color: '#667eea', cursor: 'pointer', fontSize: 12,
  },
  btnDanger: {
    padding: '4px 8px', borderRadius: 6, border: 'none',
    background: 'transparent', cursor: 'pointer', fontSize: 14,
  },
};

export default ProjectHistory;
