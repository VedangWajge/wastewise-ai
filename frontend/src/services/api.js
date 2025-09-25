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

  // === SERVICE PROVIDER APIs ===

  async findNearbyServices(wasteType, location = null) {
    try {
      let url = `${API_BASE_URL}/services/nearby?waste_type=${encodeURIComponent(wasteType)}`;

      if (location && location.lat && location.lng) {
        url += `&lat=${location.lat}&lng=${location.lng}`;
      }

      const response = await fetch(url);
      if (!response.ok) {
        throw new Error('Failed to find services');
      }
      return await response.json();
    } catch (error) {
      console.error('Service discovery error:', error);
      throw error;
    }
  }

  async getAllServiceProviders(type = null) {
    try {
      let url = `${API_BASE_URL}/services/all`;
      if (type) {
        url += `?type=${encodeURIComponent(type)}`;
      }

      const response = await fetch(url);
      if (!response.ok) {
        throw new Error('Failed to fetch services');
      }
      return await response.json();
    } catch (error) {
      console.error('Service fetch error:', error);
      throw error;
    }
  }

  // === BOOKING APIs ===

  async createBooking(bookingData) {
    try {
      const response = await fetch(`${API_BASE_URL}/booking/create`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(bookingData),
        credentials: 'include', // Include session cookies
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Booking failed');
      }

      return await response.json();
    } catch (error) {
      console.error('Booking error:', error);
      throw error;
    }
  }

  async trackBooking(bookingId) {
    try {
      const response = await fetch(`${API_BASE_URL}/booking/track/${bookingId}`, {
        credentials: 'include',
      });

      if (!response.ok) {
        throw new Error('Failed to track booking');
      }

      return await response.json();
    } catch (error) {
      console.error('Tracking error:', error);
      throw error;
    }
  }

  async getUserBookings() {
    try {
      const response = await fetch(`${API_BASE_URL}/bookings/user`, {
        credentials: 'include',
      });

      if (!response.ok) {
        throw new Error('Failed to fetch bookings');
      }

      return await response.json();
    } catch (error) {
      console.error('Bookings fetch error:', error);
      throw error;
    }
  }

  // === COMMUNITY APIs ===

  async getAllCommunities() {
    try {
      const response = await fetch(`${API_BASE_URL}/communities/all`);
      if (!response.ok) {
        throw new Error('Failed to fetch communities');
      }
      return await response.json();
    } catch (error) {
      console.error('Communities fetch error:', error);
      throw error;
    }
  }

  async getCommunityDashboard(communityId) {
    try {
      const response = await fetch(`${API_BASE_URL}/community/${communityId}/dashboard`);
      if (!response.ok) {
        throw new Error('Failed to fetch community dashboard');
      }
      return await response.json();
    } catch (error) {
      console.error('Community dashboard error:', error);
      throw error;
    }
  }

  async joinCommunity(communityId, unitNumber) {
    try {
      const response = await fetch(`${API_BASE_URL}/community/join`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ community_id: communityId, unit_number: unitNumber }),
        credentials: 'include',
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to join community');
      }

      return await response.json();
    } catch (error) {
      console.error('Community join error:', error);
      throw error;
    }
  }

  // === NOTIFICATION APIs ===

  async getNotifications() {
    try {
      const response = await fetch(`${API_BASE_URL}/notifications`, {
        credentials: 'include',
      });

      if (!response.ok) {
        throw new Error('Failed to fetch notifications');
      }

      return await response.json();
    } catch (error) {
      console.error('Notifications fetch error:', error);
      throw error;
    }
  }

  async markNotificationRead(notificationId) {
    try {
      const response = await fetch(`${API_BASE_URL}/notifications/${notificationId}/read`, {
        method: 'POST',
        credentials: 'include',
      });

      if (!response.ok) {
        throw new Error('Failed to mark notification as read');
      }

      return await response.json();
    } catch (error) {
      console.error('Notification update error:', error);
      throw error;
    }
  }

  // === ANALYTICS APIs ===

  async getEnvironmentalImpact(period = 'month') {
    try {
      const response = await fetch(`${API_BASE_URL}/analytics/impact?period=${period}`);
      if (!response.ok) {
        throw new Error('Failed to fetch impact data');
      }
      return await response.json();
    } catch (error) {
      console.error('Impact data error:', error);
      throw error;
    }
  }

  async getWasteTrends() {
    try {
      const response = await fetch(`${API_BASE_URL}/analytics/trends`);
      if (!response.ok) {
        throw new Error('Failed to fetch trends data');
      }
      return await response.json();
    } catch (error) {
      console.error('Trends data error:', error);
      throw error;
    }
  }
}

export default new ApiService();