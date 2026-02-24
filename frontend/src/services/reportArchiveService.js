import axios from 'axios';

const API_BASE = `${import.meta.env.VITE_API_BASE_URL || 'https://pytestgenie.onrender.com/api'}/pipeline-reports`;

const authHeaders = () => ({
  headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
});

/**
 * Save a new report to the archive.
 * @param {string} title   - user-visible title
 * @param {string} html    - full HTML string
 * @param {object} meta    - { stages, total_smells, username, ... }
 */
export const saveReport = (title, html, meta = {}) =>
  axios.post(API_BASE + '/', { title, html, meta }, authHeaders());

/** List all reports for the current user (no HTML body). */
export const listReports = () =>
  axios.get(API_BASE + '/', authHeaders());

/** Fetch one full report including HTML. */
export const getReport = (id) =>
  axios.get(`${API_BASE}/${id}`, authHeaders());

/** Delete a report. */
export const deleteReport = (id) =>
  axios.delete(`${API_BASE}/${id}`, authHeaders());

/**
 * Returns a URL that will serve the raw HTML for a saved report.
 * We pass the token as a query param because we're opening a new tab
 * (no way to inject an Authorization header from a plain <a> or window.open).
 */
export const reportHtmlUrl = (id) => {
  const token = localStorage.getItem('token');
  return `${API_BASE}/${id}/html?token=${encodeURIComponent(token)}`;
};
