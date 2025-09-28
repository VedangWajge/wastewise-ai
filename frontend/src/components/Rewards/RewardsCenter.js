import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import apiService from '../../services/api';
import PointsDisplay from './PointsDisplay';
import BadgesDisplay from './BadgesDisplay';
import Leaderboard from './Leaderboard';
import RewardCatalog from './RewardCatalog';
import Challenges from './Challenges';
import './RewardsCenter.css';

const RewardsCenter = () => {
  const { user, isAuthenticated } = useAuth();
  const [activeTab, setActiveTab] = useState('overview');
  const [userPoints, setUserPoints] = useState(null);
  const [userBadges, setUserBadges] = useState([]);
  const [challenges, setChallenges] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (isAuthenticated) {
      fetchRewardsData();
    }
  }, [isAuthenticated]);

  const fetchRewardsData = async () => {
    try {
      setLoading(true);
      setError(null);

      const [pointsResponse, badgesResponse, challengesResponse] = await Promise.all([
        apiService.getUserPoints(),
        apiService.getUserBadges(),
        apiService.getChallenges()
      ]);

      if (pointsResponse.success) {
        setUserPoints(pointsResponse.points);
      }

      if (badgesResponse.success) {
        setUserBadges(badgesResponse.badges);
      }

      if (challengesResponse.success) {
        setChallenges(challengesResponse.challenges);
      }
    } catch (error) {
      console.error('Error fetching rewards data:', error);
      setError(error.message || 'Failed to load rewards data');
    } finally {
      setLoading(false);
    }
  };

  const handleRewardRedeem = async (rewardId, quantity) => {
    try {
      const response = await apiService.redeemReward(rewardId, quantity);
      if (response.success) {
        // Refresh points data
        const pointsResponse = await apiService.getUserPoints();
        if (pointsResponse.success) {
          setUserPoints(pointsResponse.points);
        }
        return response;
      }
    } catch (error) {
      console.error('Error redeeming reward:', error);
      throw error;
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="rewards-center">
        <div className="auth-required">
          <div className="auth-icon">🎁</div>
          <h3>Login Required</h3>
          <p>Please login to access the rewards center and start earning points!</p>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="rewards-center">
        <div className="loading-state">
          <div className="loading-spinner"></div>
          <p>Loading your rewards...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="rewards-center">
        <div className="error-state">
          <div className="error-icon">❌</div>
          <h3>Error Loading Rewards</h3>
          <p>{error}</p>
          <button className="retry-btn" onClick={fetchRewardsData}>
            Try Again
          </button>
        </div>
      </div>
    );
  }

  const tabs = [
    { id: 'overview', label: 'Overview', icon: '🏠' },
    { id: 'points', label: 'Points', icon: '💎' },
    { id: 'badges', label: 'Badges', icon: '🏆' },
    { id: 'challenges', label: 'Challenges', icon: '🎯' },
    { id: 'leaderboard', label: 'Leaderboard', icon: '👑' },
    { id: 'catalog', label: 'Rewards', icon: '🛍️' },
  ];

  const renderTabContent = () => {
    switch (activeTab) {
      case 'overview':
        return (
          <div className="overview-tab">
            <div className="overview-grid">
              <div className="overview-card points-card">
                <div className="card-header">
                  <h3>💎 Your Points</h3>
                  <span className="card-icon">💰</span>
                </div>
                <div className="card-content">
                  <div className="points-summary">
                    <div className="current-points">
                      <span className="points-number">{userPoints?.current_balance || 0}</span>
                      <span className="points-label">Available Points</span>
                    </div>
                    <div className="points-stats">
                      <div className="stat">
                        <span className="stat-value">{userPoints?.weekly_earned || 0}</span>
                        <span className="stat-label">This Week</span>
                      </div>
                      <div className="stat">
                        <span className="stat-value">{userPoints?.total_earned || 0}</span>
                        <span className="stat-label">Total Earned</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div className="overview-card badges-card">
                <div className="card-header">
                  <h3>🏆 Achievements</h3>
                  <span className="card-icon">⭐</span>
                </div>
                <div className="card-content">
                  <div className="badges-preview">
                    {userBadges.slice(0, 6).map(badge => (
                      <div key={badge.id} className="badge-preview">
                        <span className="badge-emoji">{badge.icon}</span>
                        <span className="badge-name">{badge.name}</span>
                      </div>
                    ))}
                    {userBadges.length === 0 && (
                      <p className="no-badges">Start earning badges by completing activities!</p>
                    )}
                  </div>
                </div>
              </div>

              <div className="overview-card challenges-card">
                <div className="card-header">
                  <h3>🎯 Active Challenges</h3>
                  <span className="card-icon">🚀</span>
                </div>
                <div className="card-content">
                  <div className="challenges-preview">
                    {challenges.filter(c => c.status === 'active').slice(0, 3).map(challenge => (
                      <div key={challenge.id} className="challenge-preview">
                        <div className="challenge-info">
                          <span className="challenge-title">{challenge.title}</span>
                          <span className="challenge-reward">+{challenge.reward_points} points</span>
                        </div>
                        <div className="challenge-progress">
                          <div
                            className="progress-bar"
                            style={{
                              width: `${(challenge.current_progress / challenge.target) * 100}%`
                            }}
                          ></div>
                        </div>
                      </div>
                    ))}
                    {challenges.filter(c => c.status === 'active').length === 0 && (
                      <p className="no-challenges">No active challenges right now</p>
                    )}
                  </div>
                </div>
              </div>
            </div>

            <div className="quick-actions">
              <h3>Quick Actions</h3>
              <div className="actions-grid">
                <button
                  className="action-btn"
                  onClick={() => setActiveTab('catalog')}
                >
                  <span className="action-icon">🛍️</span>
                  <span className="action-label">Browse Rewards</span>
                </button>
                <button
                  className="action-btn"
                  onClick={() => setActiveTab('challenges')}
                >
                  <span className="action-icon">🎯</span>
                  <span className="action-label">View Challenges</span>
                </button>
                <button
                  className="action-btn"
                  onClick={() => setActiveTab('leaderboard')}
                >
                  <span className="action-icon">👑</span>
                  <span className="action-label">Check Ranking</span>
                </button>
                <button
                  className="action-btn"
                  onClick={() => window.location.hash = 'classify'}
                >
                  <span className="action-icon">📸</span>
                  <span className="action-label">Classify Waste</span>
                </button>
              </div>
            </div>
          </div>
        );

      case 'points':
        return <PointsDisplay userPoints={userPoints} />;

      case 'badges':
        return <BadgesDisplay userBadges={userBadges} />;

      case 'challenges':
        return <Challenges challenges={challenges} onUpdate={fetchRewardsData} />;

      case 'leaderboard':
        return <Leaderboard />;

      case 'catalog':
        return <RewardCatalog onRedeem={handleRewardRedeem} userPoints={userPoints} />;

      default:
        return null;
    }
  };

  return (
    <div className="rewards-center">
      <div className="rewards-header">
        <div className="header-content">
          <h1>🎁 Rewards Center</h1>
          <p>Earn points, unlock badges, and redeem amazing rewards for your eco-friendly actions!</p>
        </div>
        <div className="user-level">
          <div className="level-info">
            <span className="level-label">Level {userPoints?.level || 1}</span>
            <span className="level-progress">
              {userPoints?.points_to_next_level || 0} points to next level
            </span>
          </div>
          <div className="level-bar">
            <div
              className="level-fill"
              style={{
                width: `${userPoints?.level_progress || 0}%`
              }}
            ></div>
          </div>
        </div>
      </div>

      <div className="rewards-navigation">
        {tabs.map(tab => (
          <button
            key={tab.id}
            className={`nav-tab ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
          >
            <span className="tab-icon">{tab.icon}</span>
            <span className="tab-label">{tab.label}</span>
          </button>
        ))}
      </div>

      <div className="rewards-content">
        {renderTabContent()}
      </div>
    </div>
  );
};

export default RewardsCenter;