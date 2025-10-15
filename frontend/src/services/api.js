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

  isAuthenticated() {
    return !!this.token && !!localStorage.getItem('access_token');
  }

  getCurrentUser() {
    const userData = localStorage.getItem('user_data');
    return userData ? JSON.parse(userData) : null;
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

  // ---- Authentication endpoints ----
  async register(userData) {
    const response = await this.makeRequest('/auth/register', {
      method: 'POST',
      body: JSON.stringify(userData)
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.message || 'Registration failed');
    return data;
  }

  async login(email, password, rememberMe = false) {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, remember_me: rememberMe })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.message || 'Login failed');

    // Store tokens and user data
    if (data.success && data.tokens) {
      this.setTokens(data.tokens.access_token, data.tokens.refresh_token);
      localStorage.setItem('user_data', JSON.stringify(data.user));
    }
    return data;
  }

  async logout() {
    try {
      await this.makeRequest('/auth/logout', { method: 'POST' });
    } finally {
      this.clearTokens();
    }
  }

  async getProfile() {
    const response = await this.makeRequest('/auth/profile');
    const data = await response.json();
    if (!response.ok) throw new Error(data.message || 'Failed to fetch profile');
    return data;
  }

  async updateProfile(profileData) {
    const response = await this.makeRequest('/auth/profile', {
      method: 'PUT',
      body: JSON.stringify(profileData)
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.message || 'Profile update failed');
    if (data.success && data.user) {
      localStorage.setItem('user_data', JSON.stringify(data.user));
    }
    return data;
  }

  async changePassword(currentPassword, newPassword) {
    const response = await this.makeRequest('/auth/change-password', {
      method: 'POST',
      body: JSON.stringify({
        current_password: currentPassword,
        new_password: newPassword,
        confirm_password: newPassword
      })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.message || 'Password change failed');
    return data;
  }

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
