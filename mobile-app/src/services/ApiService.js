import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

// IMPORTANT: Replace this IP with your computer's actual IP address
// Run get-ip.bat (Windows) or get-ip.sh (Mac/Linux) to find your IP
// For Android emulator use: 10.0.2.2:5000/api
// For iOS simulator use: localhost:5000/api or 127.0.0.1:5000/api
const API_BASE_URL = 'http://192.168.1.2:5000/api'; // Update this with your computer's IP

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

  // === NETWORK CONNECTIVITY TEST ===
  async networkTest() {
    try {
      const response = await this.client.get('/network-test');
      return response.data;
    } catch (error) {
      throw new Error('Network test failed: ' + error.message);
    }
  }

  async corsTest() {
    try {
      const response = await this.client.get('/cors-test');
      return response.data;
    } catch (error) {
      throw new Error('CORS test failed: ' + error.message);
    }
  }

  async fullConnectivityTest() {
    const results = {
      timestamp: new Date().toISOString(),
      tests: {},
      overall_status: 'unknown'
    };

    try {
      // Test 1: Basic Health Check
      results.tests.health = await this.healthCheck();
      results.tests.health.status = 'PASSED';
    } catch (error) {
      results.tests.health = { status: 'FAILED', error: error.message };
    }

    try {
      // Test 2: Network Connectivity
      results.tests.network = await this.networkTest();
      results.tests.network.status = 'PASSED';
    } catch (error) {
      results.tests.network = { status: 'FAILED', error: error.message };
    }

    try {
      // Test 3: CORS Configuration
      results.tests.cors = await this.corsTest();
      results.tests.cors.status = 'PASSED';
    } catch (error) {
      results.tests.cors = { status: 'FAILED', error: error.message };
    }

    // Determine overall status
    const testResults = Object.values(results.tests);
    const passedTests = testResults.filter(test => test.status === 'PASSED').length;
    const totalTests = testResults.length;

    if (passedTests === totalTests) {
      results.overall_status = 'ALL_PASSED';
    } else if (passedTests > 0) {
      results.overall_status = 'PARTIAL_PASSED';
    } else {
      results.overall_status = 'ALL_FAILED';
    }

    results.summary = `${passedTests}/${totalTests} tests passed`;
    return results;
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