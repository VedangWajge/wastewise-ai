// api.js

const API_BASE_URL = 'http://localhost:5000/api';

class ApiService {
  constructor() {
    this.token = localStorage.getItem('access_token');
    this.refreshToken = localStorage.getItem('refresh_token');
  }

  // ---- Token management ----
  setTokens(accessToken, refreshToken) {
    this.token = accessToken;
    this.refreshToken = refreshToken;
    localStorage.setItem('access_token', accessToken);
    if (refreshToken) localStorage.setItem('refresh_token', refreshToken);
  }

  clearTokens() {
    this.token = null;
    this.refreshToken = null;
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user_data');
  }

  getAuthHeaders() {
    const headers = { 'Content-Type': 'application/json' };
    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }
    return headers;
  }

  // ---- Core fetch helper ----
  async makeRequest(url, options = {}) {
    const config = {
      ...options,
      headers: {
        ...this.getAuthHeaders(),
        ...options.headers
      }
    };

    let response = await fetch(`${API_BASE_URL}${url}`, config);

    // Auto‐refresh token on 401
    if (response.status === 401 && this.refreshToken) {
      const ok = await this.refreshAccessToken();
      if (ok) {
        config.headers['Authorization'] = `Bearer ${this.token}`;
        response = await fetch(`${API_BASE_URL}${url}`, config);
      }
    }

    return response;
  }

  async refreshAccessToken() {
    try {
      const res = await fetch(`${API_BASE_URL}/auth/refresh`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh_token: this.refreshToken })
      });
      if (!res.ok) throw new Error('Refresh failed');
      const data = await res.json();
      this.setTokens(data.tokens.access_token, data.tokens.refresh_token);
      return true;
    } catch {
      this.clearTokens();
      return false;
    }
  }

  // ---- Other endpoints (login, profile, etc.) ----
  // ... your existing methods here, unchanged ...

  // === WASTE CLASSIFICATION ===
  async classifyWaste(imageFile) {
    // Prepare multipart form data
    const formData = new FormData();
    formData.append('image', imageFile);

    // Only set Auth header; let the browser add Content-Type with boundary
    const headers = {};
    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    // Send request
    const response = await fetch(`${API_BASE_URL}/classify`, {
      method: 'POST',
      headers,
      body: formData
    });

    // Handle errors
    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.error || 'Classification failed');
    }

    // Parse result
    return await response.json();
  }

  // ---- The rest of your service methods ----
  // getWasteTypeInfo, getRecentClassifications, booking, payments, rewards, analytics...
  // ... all unchanged ...
}

const apiService = new ApiService();
export default apiService;
