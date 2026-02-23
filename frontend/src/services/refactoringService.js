import axios from 'axios';

const API_BASE = `${import.meta.env.VITE_API_BASE_URL || 'https://pytestgenie.onrender.com/api'}/refactoring`;

const refactoringService = {
  /**
   * Get available AI models for refactoring
   */
  getModels: async () => {
    try {
      const response = await axios.get(`${API_BASE}/models`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  /**
   * Get available test smell types
   */
  getSmells: async () => {
    try {
      const response = await axios.get(`${API_BASE}/smells`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  /**
   * Check refactoring service health
   */
  checkHealth: async () => {
    try {
      const response = await axios.get(`${API_BASE}/health`);
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  /**
   * Refactor test code to remove test smells
   * @param {Object} params - Refactoring parameters
   * @param {string} params.code - Test code to refactor
   * @param {string} params.smell_name - Name of the test smell
   * @param {string} params.model_type - "ollama" or "huggingface"
   * @param {string} params.model_name - Model identifier
   * @param {string} params.agent_mode - "single" or "multi"
   * @param {number} params.temperature - LLM temperature (default 0.6)
   */
  refactorCode: async ({ code, smell_name, model_type = 'ollama', model_name = 'llama3.2', agent_mode = 'single', temperature = 0.6, signal = undefined }) => {
    try {
      const response = await axios.post(`${API_BASE}/refactor`, {
        code,
        smell_name,
        model_type,
        model_name,
        agent_mode,
        temperature
      }, { signal });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  }
};

export default refactoringService;
