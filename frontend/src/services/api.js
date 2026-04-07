const API_BASE_URL = "http://10.228.33.137:5000/api";

class ApiService {
  constructor() {
    this.token = localStorage.getItem("access_token");
    this.refreshToken = localStorage.getItem("refresh_token");
  }

  // ---- Token management ----
  setTokens(accessToken, refreshToken) {
    this.token = accessToken;
    this.refreshToken = refreshToken;

    localStorage.setItem("access_token", accessToken);
    if (refreshToken) {
      localStorage.setItem("refresh_token", refreshToken);
    }
  }

  clearTokens() {
    this.token = null;
    this.refreshToken = null;

    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user_data");
  }

  getAuthHeaders() {
    const headers = {
      "Content-Type": "application/json"
    };

    if (this.token) {
      headers["Authorization"] = `Bearer ${this.token}`;
    }

    return headers;
  }

  async makeRequest(url, options = {}) {
    const config = {
      ...options,
      headers: {
        ...this.getAuthHeaders(),
        ...options.headers
      }
    };

    let response = await fetch(`${API_BASE_URL}${url}`, config);

    if (response.status === 401 && this.refreshToken) {
      const ok = await this.refreshAccessToken();

      if (ok) {
        config.headers["Authorization"] = `Bearer ${this.token}`;
        response = await fetch(`${API_BASE_URL}${url}`, config);
      }
    }

    return response;
  }

  async refreshAccessToken() {
    try {
      const res = await fetch(`${API_BASE_URL}/auth/refresh`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh_token: this.refreshToken })
      });

      if (!res.ok) throw new Error();

      const data = await res.json();

      this.setTokens(data.access_token, this.refreshToken);
      return true;

    } catch {
      this.clearTokens();
      return false;
    }
  }

  // ===== AUTH =====
  async register(userData) {
    const res = await this.makeRequest("/auth/register", {
      method: "POST",
      body: JSON.stringify(userData)
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Registration failed");

    return data;
  }

  async login(email, password) {
    const res = await fetch(`${API_BASE_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Login failed");

    if (data.tokens) {
      this.setTokens(
        data.tokens.access_token,
        data.tokens.refresh_token
      );
      localStorage.setItem("user_data", JSON.stringify(data.user));
    }

    return data;
  }

  // ===== SERVICES =====
  async findNearbyServices(wasteType) {
    const res = await this.makeRequest(`/services/search?waste_type=${wasteType}`);
    const data = await res.json();

    if (!res.ok) throw new Error(data.message || "Failed");
    return data;
  }

  // ===== BOOKINGS =====
  async createBooking(bookingData) {
    const res = await this.makeRequest("/bookings/create", {
      method: "POST",
      body: JSON.stringify(bookingData)
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.message || "Booking failed");

    return data;
  }

  async getUserBookings() {
    const res = await this.makeRequest("/bookings/my-bookings");
    const data = await res.json();

    if (!res.ok) throw new Error(data.message);
    return data;
  }

  // ===== REWARDS =====
  async getUserPoints() {
    const res = await this.makeRequest("/rewards/points");
    const data = await res.json();

    if (!res.ok) throw new Error(data.message);
    return data;
  }

  async getUserBadges() {
    const res = await this.makeRequest("/rewards/badges");
    const data = await res.json();

    if (!res.ok) throw new Error(data.message);
    return data;
  }

  async getLeaderboard() {
    const res = await this.makeRequest("/rewards/leaderboard");
    const data = await res.json();

    if (!res.ok) throw new Error(data.message);
    return data;
  }

  async getChallenges() {
    const res = await this.makeRequest("/rewards/challenges");
    const data = await res.json();

    if (!res.ok) throw new Error(data.message);
    return data;
  }

  // ===== ✅ ANALYTICS (FIX FOR DASHBOARD) =====
  async getStatistics() {
    const res = await this.makeRequest("/analytics/dashboard");
    const data = await res.json();

    if (!res.ok) throw new Error(data.message || "Failed to fetch statistics");

    return data;
  }

  // ===== AI CLASSIFICATION =====
  async classifyWaste(imageFile) {
    const formData = new FormData();
    formData.append('image', imageFile);

    const res = await fetch(`${API_BASE_URL}/classify`, {
      method: 'POST',
      body: formData
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.error || 'Classification failed');

    return data;
  }
}

const apiService = new ApiService();
export default apiService;
