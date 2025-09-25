const API_BASE_URL = 'http://localhost:5000/api';

class ApiService {
  async healthCheck() {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      if (!response.ok) {
        throw new Error('Health check failed');
      }
      return await response.json();
    } catch (error) {
      console.error('Health check error:', error);
      throw error;
    }
  }

  async classifyWaste(imageFile) {
    try {
      const formData = new FormData();
      formData.append('image', imageFile);

      const response = await fetch(`${API_BASE_URL}/classify`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Classification failed');
      }

      return await response.json();
    } catch (error) {
      console.error('Classification error:', error);
      throw error;
    }
  }

  async getStatistics() {
    try {
      const response = await fetch(`${API_BASE_URL}/statistics`);
      if (!response.ok) {
        throw new Error('Failed to fetch statistics');
      }
      return await response.json();
    } catch (error) {
      console.error('Statistics error:', error);
      throw error;
    }
  }
}

export default new ApiService();