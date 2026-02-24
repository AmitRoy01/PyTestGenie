import axios from 'axios';
import authService from './authService';

const API_BASE = `${import.meta.env.VITE_API_BASE_URL || 'https://pytestgenie.onrender.com/api'}/projects`;

const _headers = () => ({
  Authorization: `Bearer ${authService.getToken()}`,
});

const projectService = {
  // ── Projects ────────────────────────────────────────────────────────────
  getProjects: async () => {
    const r = await axios.get(`${API_BASE}/`, { headers: _headers() });
    return r.data.projects;
  },

  createProject: async (name, description = '') => {
    const r = await axios.post(`${API_BASE}/`, { name, description }, { headers: _headers() });
    return r.data; // { id, name }
  },

  deleteProject: async (projectId) => {
    await axios.delete(`${API_BASE}/${projectId}`, { headers: _headers() });
  },

  // ── Versions ────────────────────────────────────────────────────────────
  getVersions: async (projectId) => {
    const r = await axios.get(`${API_BASE}/${projectId}/versions`, { headers: _headers() });
    return r.data.versions;
  },

  /**
   * Save a version.
   * @param {string} projectId
   * @param {string} label  - user-provided label e.g. "After Pynguin generation"
   * @param {string} step   - 'source' | 'test_generated' | 'smell_detected' | 'refactored'
   * @param {object} data   - any subset of {source_code, source_filename, test_code,
   *                          test_generator, test_algorithm, smell_results,
   *                          refactored_code, refactor_model, refactor_smell}
   */
  saveVersion: async (projectId, label, step, data) => {
    const r = await axios.post(
      `${API_BASE}/${projectId}/versions`,
      { label, step, ...data },
      { headers: _headers() }
    );
    return r.data; // { id, label, version_saved }
  },

  /** Load full version payload (includes all code fields). */
  loadVersion: async (versionId) => {
    const r = await axios.get(`${API_BASE}/versions/${versionId}`, { headers: _headers() });
    return r.data;
  },

  deleteVersion: async (versionId) => {
    await axios.delete(`${API_BASE}/versions/${versionId}`, { headers: _headers() });
  },
};

export default projectService;
