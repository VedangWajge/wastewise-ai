import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Use your computer's IP address for testing on physical device
// or use 10.0.2.2 for Android emulator, 127.0.0.1 for iOS simulator
const API_BASE_URL = 'http://192.168.1.100:5000/api'; // Replace with your actual IP

class ApiService {
  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add request interceptor for auth
    this.client.interceptors.request.use(async (config) => {
      try {
        const sessionId = await AsyncStorage.getItem('session_id');
        if (sessionId) {
          config.headers['X-Session-ID'] = sessionId;
        }
      } catch (error) {
        console.error('Error getting session ID:', error);
      }
      return config;
    });

    // Add response interceptor for session handling
    this.client.interceptors.response.use(
      (response) => {
        // Store session ID if provided
        if (response.headers['x-session-id']) {
          AsyncStorage.setItem('session_id', response.headers['x-session-id']);
        }
        return response;
      },
      (error) => {
        console.error('API Error:', error.response?.data || error.message);
        return Promise.reject(error);
      },
    );
  }

  // === HEALTH CHECK ===
  async healthCheck() {
    try {
      const response = await this.client.get('/health');
      return response.data;
    } catch (error) {
      throw new Error('Health check failed');
    }
  }

  // === CLASSIFICATION ===
  async classifyWaste(imageUri, imageData) {
    try {
      const formData = new FormData();

      // For React Native, we need to handle image upload differently
      const imageFile = {
        uri: imageUri,
        type: 'image/jpeg',
        name: `waste-image-${Date.now()}.jpg`,
      };

      formData.append('image', imageFile);

      const response = await this.client.post('/classify', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 60000, // Longer timeout for image processing
      });

      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Classification failed');
    }
  }

  // === STATISTICS ===
  async getStatistics() {
    try {
      const response = await this.client.get('/statistics');
      return response.data;
    } catch (error) {
      throw new Error('Failed to fetch statistics');
    }
  }

  // === SERVICE DISCOVERY ===
  async findNearbyServices(wasteType, location = null) {
    try {
      let url = `/services/nearby?waste_type=${encodeURIComponent(wasteType)}`;

      if (location && location.latitude && location.longitude) {
        url += `&lat=${location.latitude}&lng=${location.longitude}`;
      }

      const response = await this.client.get(url);
      return response.data;
    } catch (error) {
      throw new Error('Failed to find services');
    }
  }

  async getAllServiceProviders(type = null) {
    try {
      let url = '/services/all';
      if (type) {
        url += `?type=${encodeURIComponent(type)}`;
      }

      const response = await this.client.get(url);
      return response.data;
    } catch (error) {
      throw new Error('Failed to fetch services');
    }
  }

  // === BOOKING ===
  async createBooking(bookingData) {
    try {
      const response = await this.client.post('/booking/create', bookingData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Booking failed');
    }
  }

  async trackBooking(bookingId) {
    try {
      const response = await this.client.get(`/booking/track/${bookingId}`);
      return response.data;
    } catch (error) {
      throw new Error('Failed to track booking');
    }
  }

  async getUserBookings() {
    try {
      const response = await this.client.get('/bookings/user');
      return response.data;
    } catch (error) {
      throw new Error('Failed to fetch bookings');
    }
  }

  // === COMMUNITY ===
  async getAllCommunities() {
    try {
      const response = await this.client.get('/communities/all');
      return response.data;
    } catch (error) {
      throw new Error('Failed to fetch communities');
    }
  }

  async getCommunityDashboard(communityId) {
    try {
      const response = await this.client.get(`/community/${communityId}/dashboard`);
      return response.data;
    } catch (error) {
      throw new Error('Failed to fetch community dashboard');
    }
  }

  async joinCommunity(communityId, unitNumber) {
    try {
      const response = await this.client.post('/community/join', {
        community_id: communityId,
        unit_number: unitNumber,
      });
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Failed to join community');
    }
  }

  // === NOTIFICATIONS ===
  async getNotifications() {
    try {
      const response = await this.client.get('/notifications');
      return response.data;
    } catch (error) {
      throw new Error('Failed to fetch notifications');
    }
  }

  async markNotificationRead(notificationId) {
    try {
      const response = await this.client.post(`/notifications/${notificationId}/read`);
      return response.data;
    } catch (error) {
      throw new Error('Failed to mark notification as read');
    }
  }

  // === ANALYTICS ===
  async getEnvironmentalImpact(period = 'month') {
    try {
      const response = await this.client.get(`/analytics/impact?period=${period}`);
      return response.data;
    } catch (error) {
      throw new Error('Failed to fetch impact data');
    }
  }

  async getWasteTrends() {
    try {
      const response = await this.client.get('/analytics/trends');
      return response.data;
    } catch (error) {
      throw new Error('Failed to fetch trends data');
    }
  }

  // === LOCATION ===
  async updateUserLocation(location) {
    try {
      await AsyncStorage.setItem('user_location', JSON.stringify(location));
      return true;
    } catch (error) {
      console.error('Failed to store location:', error);
      return false;
    }
  }

  async getUserLocation() {
    try {
      const locationStr = await AsyncStorage.getItem('user_location');
      return locationStr ? JSON.parse(locationStr) : null;
    } catch (error) {
      console.error('Failed to get stored location:', error);
      return null;
    }
  }
}

export default new ApiService();