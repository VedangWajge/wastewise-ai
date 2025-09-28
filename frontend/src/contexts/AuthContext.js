import React, { createContext, useContext, useState, useEffect } from 'react';
import apiService from '../services/api';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    // Check if user is already logged in on app start
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      if (apiService.isAuthenticated()) {
        const userData = apiService.getCurrentUser();
        if (userData) {
          setUser(userData);
          setIsAuthenticated(true);

          // Verify token is still valid by fetching fresh profile data
          try {
            const profileData = await apiService.getProfile();
            if (profileData.success) {
              setUser(profileData.user);
            }
          } catch (error) {
            // Token might be expired, clear auth state
            await logout();
          }
        }
      }
    } catch (error) {
      console.error('Auth status check error:', error);
      await logout();
    } finally {
      setLoading(false);
    }
  };

  const register = async (userData) => {
    try {
      setLoading(true);
      const response = await apiService.register(userData);

      if (response.success) {
        // Registration successful, but user needs to verify email
        return response;
      }

      throw new Error(response.message || 'Registration failed');
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const login = async (email, password, rememberMe = false) => {
    try {
      setLoading(true);
      const response = await apiService.login(email, password, rememberMe);

      if (response.success && response.user) {
        setUser(response.user);
        setIsAuthenticated(true);
        return response;
      }

      throw new Error(response.message || 'Login failed');
    } catch (error) {
      console.error('Login error:', error);
      await logout(); // Ensure clean state on failed login
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    try {
      await apiService.logout();
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      setUser(null);
      setIsAuthenticated(false);
      setLoading(false);
    }
  };

  const updateProfile = async (profileData) => {
    try {
      setLoading(true);
      const response = await apiService.updateProfile(profileData);

      if (response.success && response.user) {
        setUser(response.user);
        localStorage.setItem('user_data', JSON.stringify(response.user));
        return response;
      }

      throw new Error(response.message || 'Profile update failed');
    } catch (error) {
      console.error('Profile update error:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const changePassword = async (currentPassword, newPassword) => {
    try {
      setLoading(true);
      const response = await apiService.changePassword(currentPassword, newPassword);
      return response;
    } catch (error) {
      console.error('Password change error:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const refreshUserData = async () => {
    try {
      if (isAuthenticated) {
        const profileData = await apiService.getProfile();
        if (profileData.success) {
          setUser(profileData.user);
          localStorage.setItem('user_data', JSON.stringify(profileData.user));
        }
      }
    } catch (error) {
      console.error('User data refresh error:', error);
      // If refresh fails, user might need to re-login
      await logout();
    }
  };

  const hasRole = (role) => {
    return user && user.role === role;
  };

  const hasAnyRole = (roles) => {
    return user && roles.includes(user.role);
  };

  const value = {
    user,
    isAuthenticated,
    loading,
    register,
    login,
    logout,
    updateProfile,
    changePassword,
    refreshUserData,
    hasRole,
    hasAnyRole,
    checkAuthStatus,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;