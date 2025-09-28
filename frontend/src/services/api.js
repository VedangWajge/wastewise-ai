const API_BASE_URL = 'http://localhost:5000/api';

class ApiService {
  constructor() {
    this.token = localStorage.getItem('access_token');
    this.refreshToken = localStorage.getItem('refresh_token');
  }

  // Token management
  setTokens(accessToken, refreshToken) {
    this.token = accessToken;
    this.refreshToken = refreshToken;
    localStorage.setItem('access_token', accessToken);
    if (refreshToken) {
      localStorage.setItem('refresh_token', refreshToken);
    }
  }

  clearTokens() {
    this.token = null;
    this.refreshToken = null;
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user_data');
  }

  getAuthHeaders() {
    const headers = {
      'Content-Type': 'application/json',
    };
    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }
    return headers;
  }

  async makeRequest(url, options = {}) {
    const config = {
      ...options,
      headers: {
        ...this.getAuthHeaders(),
        ...options.headers,
      },
    };

    try {
      const response = await fetch(`${API_BASE_URL}${url}`, config);

      if (response.status === 401 && this.refreshToken) {
        // Try to refresh token
        const refreshed = await this.refreshAccessToken();
        if (refreshed) {
          // Retry with new token
          config.headers['Authorization'] = `Bearer ${this.token}`;
          return await fetch(`${API_BASE_URL}${url}`, config);
        }
      }

      return response;
    } catch (error) {
      console.error('API request error:', error);
      throw error;
    }
  }

  async refreshAccessToken() {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/refresh`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh_token: this.refreshToken }),
      });

      if (response.ok) {
        const data = await response.json();
        this.setTokens(data.tokens.access_token, data.tokens.refresh_token);
        return true;
      } else {
        this.clearTokens();
        return false;
      }
    } catch (error) {
      console.error('Token refresh error:', error);
      this.clearTokens();
      return false;
    }
  }

  // === SYSTEM ENDPOINTS ===

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

  async globalSearch(query, category = 'all', limit = 10) {
    try {
      const params = new URLSearchParams({ q: query, category, limit });
      const response = await fetch(`${API_BASE_URL}/search?${params}`);
      if (!response.ok) {
        throw new Error('Search failed');
      }
      return await response.json();
    } catch (error) {
      console.error('Search error:', error);
      throw error;
    }
  }

  // === AUTHENTICATION ===

  async register(userData) {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Registration failed');
      }

      return await response.json();
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  }

  async login(email, password, rememberMe = false) {
    try {
      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password, remember_me: rememberMe }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Login failed');
      }

      const data = await response.json();
      this.setTokens(data.tokens.access_token, data.tokens.refresh_token);
      localStorage.setItem('user_data', JSON.stringify(data.user));
      return data;
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  }

  async logout() {
    try {
      if (this.token) {
        await this.makeRequest('/auth/logout', { method: 'POST' });
      }
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      this.clearTokens();
    }
  }

  async getProfile() {
    try {
      const response = await this.makeRequest('/auth/profile');
      if (!response.ok) {
        throw new Error('Failed to fetch profile');
      }
      return await response.json();
    } catch (error) {
      console.error('Profile fetch error:', error);
      throw error;
    }
  }

  async updateProfile(profileData) {
    try {
      const response = await this.makeRequest('/auth/profile', {
        method: 'PUT',
        body: JSON.stringify(profileData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Profile update failed');
      }

      return await response.json();
    } catch (error) {
      console.error('Profile update error:', error);
      throw error;
    }
  }

  async changePassword(currentPassword, newPassword) {
    try {
      const response = await this.makeRequest('/auth/change-password', {
        method: 'POST',
        body: JSON.stringify({
          current_password: currentPassword,
          new_password: newPassword,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Password change failed');
      }

      return await response.json();
    } catch (error) {
      console.error('Password change error:', error);
      throw error;
    }
  }

  // === WASTE CLASSIFICATION ===

  async classifyWaste(imageFile) {
    try {
      const formData = new FormData();
      formData.append('image', imageFile);

      const response = await fetch(`${API_BASE_URL}/classify`, {
        method: 'POST',
        body: formData,
        headers: this.token ? { 'Authorization': `Bearer ${this.token}` } : {},
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

  async getWasteTypeInfo(wasteType) {
    try {
      const response = await fetch(`${API_BASE_URL}/waste-info/${wasteType}`);
      if (!response.ok) {
        throw new Error('Failed to fetch waste type info');
      }
      return await response.json();
    } catch (error) {
      console.error('Waste type info error:', error);
      throw error;
    }
  }

  async getRecentClassifications() {
    try {
      const response = await this.makeRequest('/recent');
      if (!response.ok) {
        throw new Error('Failed to fetch recent classifications');
      }
      return await response.json();
    } catch (error) {
      console.error('Recent classifications error:', error);
      throw error;
    }
  }

  // === SERVICE PROVIDERS ===

  async searchServiceProviders(params = {}) {
    try {
      const queryParams = new URLSearchParams(params);
      const response = await fetch(`${API_BASE_URL}/services/search?${queryParams}`);
      if (!response.ok) {
        throw new Error('Failed to search services');
      }
      return await response.json();
    } catch (error) {
      console.error('Service search error:', error);
      throw error;
    }
  }

  async getServiceProviderDetails(providerId) {
    try {
      const response = await fetch(`${API_BASE_URL}/services/${providerId}`);
      if (!response.ok) {
        throw new Error('Failed to fetch provider details');
      }
      return await response.json();
    } catch (error) {
      console.error('Provider details error:', error);
      throw error;
    }
  }

  async getServiceProviderReviews(providerId) {
    try {
      const response = await fetch(`${API_BASE_URL}/services/${providerId}/reviews`);
      if (!response.ok) {
        throw new Error('Failed to fetch provider reviews');
      }
      return await response.json();
    } catch (error) {
      console.error('Provider reviews error:', error);
      throw error;
    }
  }

  async registerAsServiceProvider(providerData) {
    try {
      const response = await this.makeRequest('/services/register', {
        method: 'POST',
        body: JSON.stringify(providerData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Service provider registration failed');
      }

      return await response.json();
    } catch (error) {
      console.error('Service provider registration error:', error);
      throw error;
    }
  }

  async findNearbyServices(wasteType = null, location = null, radius = 10) {
    try {
      const params = new URLSearchParams();
      if (wasteType) params.append('waste_type', wasteType);
      if (location) params.append('location', location);
      params.append('radius', radius);

      const response = await fetch(`${API_BASE_URL}/services/search?${params}`);
      if (!response.ok) {
        throw new Error('Failed to find nearby services');
      }

      const data = await response.json();
      return { services: data.providers || [] };
    } catch (error) {
      console.error('Nearby services error:', error);
      throw error;
    }
  }

  // === BOOKING MANAGEMENT ===

  async createBooking(bookingData) {
    try {
      const response = await this.makeRequest('/bookings/create', {
        method: 'POST',
        body: JSON.stringify(bookingData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Booking failed');
      }

      return await response.json();
    } catch (error) {
      console.error('Booking error:', error);
      throw error;
    }
  }

  async getUserBookings(status = null, limit = 20, offset = 0) {
    try {
      const params = new URLSearchParams({ limit, offset });
      if (status) params.append('status', status);

      const response = await this.makeRequest(`/bookings/my-bookings?${params}`);
      if (!response.ok) {
        throw new Error('Failed to fetch bookings');
      }
      return await response.json();
    } catch (error) {
      console.error('Bookings fetch error:', error);
      throw error;
    }
  }

  async getBookingDetails(bookingId) {
    try {
      const response = await this.makeRequest(`/bookings/${bookingId}`);
      if (!response.ok) {
        throw new Error('Failed to fetch booking details');
      }
      return await response.json();
    } catch (error) {
      console.error('Booking details error:', error);
      throw error;
    }
  }

  async trackBooking(bookingId) {
    try {
      const response = await this.makeRequest(`/bookings/${bookingId}/track`);
      if (!response.ok) {
        throw new Error('Failed to track booking');
      }
      return await response.json();
    } catch (error) {
      console.error('Booking tracking error:', error);
      throw error;
    }
  }

  async cancelBooking(bookingId, reason = '') {
    try {
      const response = await this.makeRequest(`/bookings/${bookingId}/cancel`, {
        method: 'POST',
        body: JSON.stringify({ reason }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to cancel booking');
      }

      return await response.json();
    } catch (error) {
      console.error('Booking cancellation error:', error);
      throw error;
    }
  }

  async rescheduleBooking(bookingId, newDate, newTimeSlot) {
    try {
      const response = await this.makeRequest(`/bookings/${bookingId}/reschedule`, {
        method: 'POST',
        body: JSON.stringify({
          new_scheduled_date: newDate,
          new_time_slot: newTimeSlot,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to reschedule booking');
      }

      return await response.json();
    } catch (error) {
      console.error('Booking reschedule error:', error);
      throw error;
    }
  }

  async rateBooking(bookingId, ratingData) {
    try {
      const response = await this.makeRequest(`/bookings/${bookingId}/rate`, {
        method: 'POST',
        body: JSON.stringify(ratingData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to rate booking');
      }

      return await response.json();
    } catch (error) {
      console.error('Booking rating error:', error);
      throw error;
    }
  }

  // === PAYMENTS ===

  async getPaymentMethods() {
    try {
      const response = await fetch(`${API_BASE_URL}/payments/methods`);
      if (!response.ok) {
        throw new Error('Failed to fetch payment methods');
      }
      return await response.json();
    } catch (error) {
      console.error('Payment methods error:', error);
      throw error;
    }
  }

  async initiatePayment(paymentData) {
    try {
      const response = await this.makeRequest('/payments/initiate', {
        method: 'POST',
        body: JSON.stringify(paymentData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Payment initiation failed');
      }

      return await response.json();
    } catch (error) {
      console.error('Payment initiation error:', error);
      throw error;
    }
  }

  async verifyPayment(verificationData) {
    try {
      const response = await this.makeRequest('/payments/verify', {
        method: 'POST',
        body: JSON.stringify(verificationData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Payment verification failed');
      }

      return await response.json();
    } catch (error) {
      console.error('Payment verification error:', error);
      throw error;
    }
  }

  async getPaymentHistory() {
    try {
      const response = await this.makeRequest('/payments/history');
      if (!response.ok) {
        throw new Error('Failed to fetch payment history');
      }
      return await response.json();
    } catch (error) {
      console.error('Payment history error:', error);
      throw error;
    }
  }

  // === REWARDS & GAMIFICATION ===

  async getUserPoints() {
    try {
      const response = await this.makeRequest('/rewards/points');
      if (!response.ok) {
        throw new Error('Failed to fetch user points');
      }
      return await response.json();
    } catch (error) {
      console.error('User points error:', error);
      throw error;
    }
  }

  async getUserBadges() {
    try {
      const response = await this.makeRequest('/rewards/badges');
      if (!response.ok) {
        throw new Error('Failed to fetch user badges');
      }
      return await response.json();
    } catch (error) {
      console.error('User badges error:', error);
      throw error;
    }
  }

  async getLeaderboard(period = 'weekly', category = 'points') {
    try {
      const params = new URLSearchParams({ period, category });
      const response = await this.makeRequest(`/rewards/leaderboard?${params}`);
      if (!response.ok) {
        throw new Error('Failed to fetch leaderboard');
      }
      return await response.json();
    } catch (error) {
      console.error('Leaderboard error:', error);
      throw error;
    }
  }

  async getRewardCatalog() {
    try {
      const response = await fetch(`${API_BASE_URL}/rewards/catalog`);
      if (!response.ok) {
        throw new Error('Failed to fetch reward catalog');
      }
      return await response.json();
    } catch (error) {
      console.error('Reward catalog error:', error);
      throw error;
    }
  }

  async redeemReward(rewardId, quantity = 1) {
    try {
      const response = await this.makeRequest('/rewards/redeem', {
        method: 'POST',
        body: JSON.stringify({ reward_id: rewardId, quantity }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Reward redemption failed');
      }

      return await response.json();
    } catch (error) {
      console.error('Reward redemption error:', error);
      throw error;
    }
  }

  async getChallenges() {
    try {
      const response = await this.makeRequest('/rewards/challenges');
      if (!response.ok) {
        throw new Error('Failed to fetch challenges');
      }
      return await response.json();
    } catch (error) {
      console.error('Challenges error:', error);
      throw error;
    }
  }

  async getUserChallenges() {
    try {
      const response = await this.makeRequest('/rewards/user-challenges');
      if (!response.ok) {
        throw new Error('Failed to fetch user challenges');
      }
      return await response.json();
    } catch (error) {
      console.error('User challenges error:', error);
      throw error;
    }
  }

  async joinChallenge(challengeId) {
    try {
      const response = await this.makeRequest('/rewards/challenges/join', {
        method: 'POST',
        body: JSON.stringify({ challenge_id: challengeId }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to join challenge');
      }

      return await response.json();
    } catch (error) {
      console.error('Join challenge error:', error);
      throw error;
    }
  }

  // === ANALYTICS ===

  async getPersonalAnalytics(period = 'month', includePredictions = false) {
    try {
      const params = new URLSearchParams({ period, predictions: includePredictions });
      const response = await this.makeRequest(`/analytics/personal?${params}`);
      if (!response.ok) {
        throw new Error('Failed to fetch personal analytics');
      }
      return await response.json();
    } catch (error) {
      console.error('Personal analytics error:', error);
      throw error;
    }
  }

  async getCommunityAnalytics(communityId) {
    try {
      const response = await this.makeRequest(`/analytics/community/${communityId}`);
      if (!response.ok) {
        throw new Error('Failed to fetch community analytics');
      }
      return await response.json();
    } catch (error) {
      console.error('Community analytics error:', error);
      throw error;
    }
  }

  async exportAnalyticsData(exportData) {
    try {
      const response = await this.makeRequest('/analytics/export', {
        method: 'POST',
        body: JSON.stringify(exportData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Analytics export failed');
      }

      return await response.json();
    } catch (error) {
      console.error('Analytics export error:', error);
      throw error;
    }
  }

  async getAIInsights() {
    try {
      const response = await this.makeRequest('/analytics/insights');
      if (!response.ok) {
        throw new Error('Failed to fetch AI insights');
      }
      return await response.json();
    } catch (error) {
      console.error('AI insights error:', error);
      throw error;
    }
  }

  // === UTILITY METHODS ===

  isAuthenticated() {
    return !!this.token;
  }

  getCurrentUser() {
    const userData = localStorage.getItem('user_data');
    return userData ? JSON.parse(userData) : null;
  }
}

const apiService = new ApiService();
export default apiService;