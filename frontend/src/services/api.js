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
    const formData = new FormData();
    formData.append('image', imageFile);

    const headers = {};
    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    const response = await fetch(`${API_BASE_URL}/ai/predict`, {
      method: 'POST',
      headers,
      body: formData
    });

    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.error || 'Classification failed');
    }

    return await response.json();
  }

  // === SERVICE PROVIDERS ===
  async findNearbyServices(wasteType, filters = {}) {
    const queryParams = new URLSearchParams({
      waste_type: wasteType,
      ...filters
    });
    const response = await this.makeRequest(`/services/search?${queryParams}`);
    const data = await response.json();
    if (!response.ok) throw new Error(data.message || 'Failed to fetch services');
    return data;
  }

  async getServiceDetails(serviceId) {
    const response = await this.makeRequest(`/services/${serviceId}`);
    const data = await response.json();
    if (!response.ok) throw new Error(data.message || 'Failed to fetch service details');
    return data;
  }

  // === BOOKINGS ===
  async createBooking(bookingData) {
    const response = await this.makeRequest('/bookings/create', {
      method: 'POST',
      body: JSON.stringify(bookingData)
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.message || 'Booking failed');
    return data;
  }

  async getUserBookings(status = null) {
    const url = status ? `/bookings/my-bookings?status=${status}` : '/bookings/my-bookings';
    const response = await this.makeRequest(url);
    const data = await response.json();
    if (!response.ok) throw new Error(data.message || 'Failed to fetch bookings');
    return data;
  }

  // Alias for getUserBookings - for consistency
  async getBookings(status = null) {
    return this.getUserBookings(status);
  }

  async getBookingDetails(bookingId) {
    const response = await this.makeRequest(`/bookings/${bookingId}`);
    const data = await response.json();
    if (!response.ok) throw new Error(data.message || 'Failed to fetch booking details');
    return data;
  }

  async cancelBooking(bookingId, reason) {
    const response = await this.makeRequest(`/bookings/${bookingId}/cancel`, {
      method: 'POST',
      body: JSON.stringify({ reason })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.message || 'Failed to cancel booking');
    return data;
  }

  async rescheduleBooking(bookingId, newDate, newTimeSlot) {
    const response = await this.makeRequest(`/bookings/${bookingId}/reschedule`, {
      method: 'POST',
      body: JSON.stringify({
        new_scheduled_date: newDate,
        new_time_slot: newTimeSlot
      })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.message || 'Failed to reschedule booking');
    return data;
  }

  async rateBooking(bookingId, ratingData) {
    const response = await this.makeRequest(`/bookings/${bookingId}/rate`, {
      method: 'POST',
      body: JSON.stringify(ratingData)
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.message || 'Failed to submit rating');
    return data;
  }

  async trackBooking(bookingId) {
    const response = await this.makeRequest(`/bookings/${bookingId}/track`);
    const data = await response.json();
    if (!response.ok) throw new Error(data.message || 'Failed to track booking');
    return data;
  }

  // === REWARDS ===
  async getUserPoints() {
    const response = await this.makeRequest('/rewards/points');
    const data = await response.json();
    if (!response.ok) throw new Error(data.message || 'Failed to fetch points');
    return data;
  }

  async getUserBadges() {
    const response = await this.makeRequest('/rewards/badges');
    const data = await response.json();
    if (!response.ok) throw new Error(data.message || 'Failed to fetch badges');
    return data;
  }

  async getChallenges() {
    const response = await this.makeRequest('/rewards/challenges');
    const data = await response.json();
    if (!response.ok) throw new Error(data.message || 'Failed to fetch challenges');
    return data;
  }

  async getUserChallenges() {
    const response = await this.makeRequest('/rewards/my-challenges');
    const data = await response.json();
    if (!response.ok) throw new Error(data.message || 'Failed to fetch user challenges');
    return data;
  }

  async joinChallenge(challengeId) {
    const response = await this.makeRequest(`/rewards/challenges/${challengeId}/join`, {
      method: 'POST'
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.message || 'Failed to join challenge');
    return data;
  }

  async getRewardCatalog() {
    const response = await this.makeRequest('/rewards/catalog');
    const data = await response.json();
    if (!response.ok) throw new Error(data.message || 'Failed to fetch reward catalog');
    return data;
  }

  async redeemReward(rewardId, quantity = 1) {
    const response = await this.makeRequest('/rewards/redeem', {
      method: 'POST',
      body: JSON.stringify({ reward_id: rewardId, points_to_redeem: quantity })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.message || 'Failed to redeem reward');
    return data;
  }

  async getLeaderboard(filters = {}) {
    const queryParams = new URLSearchParams(filters);
    const response = await this.makeRequest(`/rewards/leaderboard?${queryParams}`);
    const data = await response.json();
    if (!response.ok) throw new Error(data.message || 'Failed to fetch leaderboard');
    return data;
  }

  // Get all rewards data (points, badges, etc.) - for Profile component
  async getRewards() {
    try {
      const [pointsData, badgesData] = await Promise.all([
        this.getUserPoints(),
        this.getUserBadges()
      ]);

      // Extract points value - handle both object and number formats
      let pointsValue = 0;
      if (pointsData && pointsData.points !== undefined) {
        if (typeof pointsData.points === 'number') {
          pointsValue = pointsData.points;
        } else if (typeof pointsData.points === 'object' && pointsData.points !== null) {
          // Handle object format: {current_balance, total_earned, total_spent, weekly_earned}
          pointsValue = pointsData.points.current_balance ||
                       pointsData.points.total_earned ||
                       0;
        }
      }

      return {
        success: true,
        points: pointsValue,
        pointsDetails: pointsData.points, // Keep original for detailed view
        level: pointsData.level || 1,
        badges: badgesData.badges || [],
        total_badges: badgesData.total_badges || 0
      };
    } catch (error) {
      console.error('Error fetching rewards:', error);
      return {
        success: false,
        points: 0,
        pointsDetails: null,
        level: 1,
        badges: [],
        total_badges: 0
      };
    }
  }

  // === PAYMENTS ===
  async getPaymentMethods() {
    const response = await this.makeRequest('/payments/methods');
    const data = await response.json();
    if (!response.ok) throw new Error(data.message || 'Failed to fetch payment methods');
    return data;
  }

  async getPaymentHistory() {
    const response = await this.makeRequest('/payments/history');
    const data = await response.json();
    if (!response.ok) throw new Error(data.message || 'Failed to fetch payment history');
    return data;
  }

  async initiatePayment(paymentData) {
    const response = await this.makeRequest('/payments/initiate', {
      method: 'POST',
      body: JSON.stringify(paymentData)
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.message || 'Failed to initiate payment');
    return data;
  }

  async verifyPayment(verificationData) {
    const response = await this.makeRequest('/payments/verify', {
      method: 'POST',
      body: JSON.stringify(verificationData)
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.message || 'Failed to verify payment');
    return data;
  }

  // === ANALYTICS ===
  async getStatistics() {
    const response = await this.makeRequest('/analytics/dashboard');
    const data = await response.json();
    if (!response.ok) throw new Error(data.message || 'Failed to fetch statistics');
    return data;
  }

  async getPersonalAnalytics(period = 'month', includeComparisons = false) {
    const queryParams = new URLSearchParams({ period, predictions: includeComparisons });
    const response = await this.makeRequest(`/analytics/personal?${queryParams}`);
    const data = await response.json();
    if (!response.ok) throw new Error(data.message || 'Failed to fetch analytics');
    return data;
  }

  async getAIInsights() {
    const response = await this.makeRequest('/analytics/insights?type=personal');
    const data = await response.json();
    if (!response.ok) throw new Error(data.message || 'Failed to fetch AI insights');
    return data;
  }

  async exportAnalyticsData(exportOptions) {
    const response = await this.makeRequest('/analytics/export', {
      method: 'POST',
      body: JSON.stringify(exportOptions)
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.message || 'Failed to export data');
    return data;
  }
}

const apiService = new ApiService();
export default apiService;
