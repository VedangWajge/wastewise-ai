import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import apiService from '../../services/api';
import './Profile.css';

const Profile = ({ setCurrentView }) => {
  const { user, isAuthenticated } = useAuth();
  const [activeSection, setActiveSection] = useState('overview');
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (isAuthenticated) {
      fetchUserStats();
    }
  }, [isAuthenticated]);

  const fetchUserStats = async () => {
    try {
      setLoading(true);
      // Fetch user's stats
      const [bookingsResponse, paymentsResponse, rewardsResponse] = await Promise.all([
        apiService.getBookings().catch(() => ({ bookings: [] })),
        apiService.getPaymentHistory().catch(() => ({ payments: [] })),
        apiService.getRewards().catch(() => ({ points: 0 }))
      ]);

      // Extract reward points - handle both object and number formats
      let rewardPoints = 0;
      if (rewardsResponse) {
        if (typeof rewardsResponse.points === 'number') {
          rewardPoints = rewardsResponse.points;
        } else if (typeof rewardsResponse.points === 'object' && rewardsResponse.points !== null) {
          // Handle object format: {current_balance, total_earned, etc.}
          rewardPoints = rewardsResponse.points.current_balance ||
                        rewardsResponse.points.total_earned ||
                        0;
        } else if (typeof rewardsResponse === 'number') {
          rewardPoints = rewardsResponse;
        }
      }

      setStats({
        totalBookings: bookingsResponse.bookings?.length || 0,
        pendingPayments: bookingsResponse.bookings?.filter(b => b.payment_status === 'pending').length || 0,
        completedBookings: bookingsResponse.bookings?.filter(b => b.status === 'completed').length || 0,
        totalPaid: paymentsResponse.payments?.reduce((sum, p) => p.status === 'completed' ? sum + p.amount : sum, 0) || 0,
        rewardPoints: rewardPoints
      });
    } catch (error) {
      console.error('Error fetching stats:', error);
      // Set default stats on error
      setStats({
        totalBookings: 0,
        pendingPayments: 0,
        completedBookings: 0,
        totalPaid: 0,
        rewardPoints: 0
      });
    } finally {
      setLoading(false);
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="profile-container">
        <div className="auth-required">
          <div className="auth-icon">👤</div>
          <h3>Login Required</h3>
          <p>Please login to view your profile</p>
          <button className="login-btn" onClick={() => setCurrentView('login')}>
            Go to Login
          </button>
        </div>
      </div>
    );
  }

  const sections = [
    { id: 'overview', label: 'Overview', icon: '📊' },
    { id: 'bookings', label: 'My Bookings', icon: '📅' },
    { id: 'payments', label: 'Payments', icon: '💳' },
    { id: 'rewards', label: 'Rewards', icon: '🎁' },
    { id: 'settings', label: 'Settings', icon: '⚙️' }
  ];

  return (
    <div className="profile-container">
      <div className="profile-header">
        <div className="profile-avatar">
          <div className="avatar-circle">
            {user?.full_name?.charAt(0).toUpperCase() || '👤'}
          </div>
        </div>
        <div className="profile-info">
          <h2>{user?.full_name || 'User'}</h2>
          <p className="user-email">{user?.email}</p>
          <span className="user-role-badge">{user?.role || 'User'}</span>
        </div>
      </div>

      <div className="profile-navigation">
        {sections.map(section => (
          <button
            key={section.id}
            className={`profile-nav-btn ${activeSection === section.id ? 'active' : ''}`}
            onClick={() => {
              if (section.id === 'bookings') {
                setCurrentView('bookings');
              } else if (section.id === 'payments') {
                setCurrentView('payment');
              } else if (section.id === 'rewards') {
                setCurrentView('rewards');
              } else {
                setActiveSection(section.id);
              }
            }}
          >
            <span className="nav-icon">{section.icon}</span>
            <span className="nav-label">{section.label}</span>
          </button>
        ))}
      </div>

      <div className="profile-content">
        {activeSection === 'overview' && (
          <div className="overview-section">
            <h3>Account Overview</h3>

            {loading ? (
              <div className="loading-spinner">Loading stats...</div>
            ) : (
              <div className="stats-grid">
                <div className="stat-card">
                  <div className="stat-icon">📅</div>
                  <div className="stat-info">
                    <div className="stat-value">{stats?.totalBookings || 0}</div>
                    <div className="stat-label">Total Bookings</div>
                  </div>
                </div>

                <div className="stat-card">
                  <div className="stat-icon">✅</div>
                  <div className="stat-info">
                    <div className="stat-value">{stats?.completedBookings || 0}</div>
                    <div className="stat-label">Completed</div>
                  </div>
                </div>

                <div className="stat-card warning">
                  <div className="stat-icon">⏳</div>
                  <div className="stat-info">
                    <div className="stat-value">{stats?.pendingPayments || 0}</div>
                    <div className="stat-label">Pending Payments</div>
                  </div>
                  {stats?.pendingPayments > 0 && (
                    <button
                      className="action-btn"
                      onClick={() => setCurrentView('payment')}
                    >
                      Pay Now
                    </button>
                  )}
                </div>

                <div className="stat-card success">
                  <div className="stat-icon">💰</div>
                  <div className="stat-info">
                    <div className="stat-value">₹{stats?.totalPaid || 0}</div>
                    <div className="stat-label">Total Paid</div>
                  </div>
                </div>

                <div className="stat-card highlight">
                  <div className="stat-icon">🎁</div>
                  <div className="stat-info">
                    <div className="stat-value">{stats?.rewardPoints || 0}</div>
                    <div className="stat-label">Reward Points</div>
                  </div>
                  <button
                    className="action-btn"
                    onClick={() => setCurrentView('rewards')}
                  >
                    View Rewards
                  </button>
                </div>
              </div>
            )}

            <div className="quick-actions">
              <h4>Quick Actions</h4>
              <div className="actions-grid">
                <button className="action-card" onClick={() => setCurrentView('home')}>
                  <span className="action-icon">📸</span>
                  <span className="action-label">Classify Waste</span>
                </button>
                <button className="action-card" onClick={() => setCurrentView('bookings')}>
                  <span className="action-icon">📅</span>
                  <span className="action-label">View Bookings</span>
                </button>
                <button className="action-card" onClick={() => setCurrentView('payment')}>
                  <span className="action-icon">💳</span>
                  <span className="action-label">Make Payment</span>
                </button>
                <button className="action-card" onClick={() => setCurrentView('marketplace')}>
                  <span className="action-icon">🛒</span>
                  <span className="action-label">Marketplace</span>
                </button>
              </div>
            </div>
          </div>
        )}

        {activeSection === 'settings' && (
          <div className="settings-section">
            <h3>Account Settings</h3>
            <div className="settings-card">
              <div className="setting-item">
                <div className="setting-label">
                  <span className="setting-icon">👤</span>
                  <span>Full Name</span>
                </div>
                <div className="setting-value">{user?.full_name}</div>
              </div>

              <div className="setting-item">
                <div className="setting-label">
                  <span className="setting-icon">📧</span>
                  <span>Email</span>
                </div>
                <div className="setting-value">{user?.email}</div>
              </div>

              <div className="setting-item">
                <div className="setting-label">
                  <span className="setting-icon">📱</span>
                  <span>Phone</span>
                </div>
                <div className="setting-value">{user?.phone || 'Not provided'}</div>
              </div>

              <div className="setting-item">
                <div className="setting-label">
                  <span className="setting-icon">🏷️</span>
                  <span>Role</span>
                </div>
                <div className="setting-value">{user?.role}</div>
              </div>

              <div className="setting-item">
                <div className="setting-label">
                  <span className="setting-icon">📅</span>
                  <span>Member Since</span>
                </div>
                <div className="setting-value">
                  {user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}
                </div>
              </div>
            </div>

            <div className="settings-actions">
              <button className="settings-btn secondary">
                Edit Profile
              </button>
              <button className="settings-btn secondary">
                Change Password
              </button>
              <button className="settings-btn danger">
                Delete Account
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Profile;
