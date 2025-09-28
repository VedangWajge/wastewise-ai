import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import apiService from '../../services/api';

const RewardCatalog = () => {
  const { isAuthenticated } = useAuth();
  const [rewards, setRewards] = useState([]);
  const [userPoints, setUserPoints] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState('all');
  const [redeeming, setRedeeming] = useState(null);

  useEffect(() => {
    fetchRewards();
    if (isAuthenticated) {
      fetchUserPoints();
    }
  }, [isAuthenticated]);

  const fetchRewards = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiService.getRewardCatalog();
      if (response.success) {
        setRewards(response.rewards || []);
      }
    } catch (error) {
      console.error('Error fetching rewards:', error);
      setError('Failed to load reward catalog');
    } finally {
      setLoading(false);
    }
  };

  const fetchUserPoints = async () => {
    try {
      const response = await apiService.getUserPoints();
      if (response.success) {
        setUserPoints(response.points || 0);
      }
    } catch (error) {
      console.error('Error fetching user points:', error);
    }
  };

  const handleRedeem = async (rewardId) => {
    if (!isAuthenticated) {
      alert('Please login to redeem rewards');
      return;
    }

    const reward = rewards.find(r => r.id === rewardId);
    if (!reward) return;

    if (userPoints < reward.points_required) {
      alert(`You need ${reward.points_required - userPoints} more points to redeem this reward`);
      return;
    }

    if (!window.confirm(`Redeem "${reward.name}" for ${reward.points_required} points?`)) {
      return;
    }

    try {
      setRedeeming(rewardId);
      const response = await apiService.redeemReward(rewardId);

      if (response.success) {
        alert('Reward redeemed successfully! Check your email for details.');
        setUserPoints(prev => prev - reward.points_required);
        // Update reward availability
        setRewards(prev => prev.map(r =>
          r.id === rewardId
            ? { ...r, stock: Math.max(0, (r.stock || 1) - 1) }
            : r
        ));
      } else {
        alert(response.message || 'Failed to redeem reward');
      }
    } catch (error) {
      console.error('Error redeeming reward:', error);
      alert('Failed to redeem reward. Please try again.');
    } finally {
      setRedeeming(null);
    }
  };

  const canAfford = (pointsRequired) => {
    return userPoints >= pointsRequired;
  };

  const isAvailable = (reward) => {
    return reward.is_active && (reward.stock === null || reward.stock > 0);
  };

  const filteredRewards = rewards.filter(reward => {
    if (filter === 'all') return true;
    if (filter === 'affordable') return canAfford(reward.points_required);
    if (filter === 'digital') return reward.type === 'digital';
    if (filter === 'physical') return reward.type === 'physical';
    if (filter === 'discount') return reward.type === 'discount';
    return true;
  });

  const categories = [
    { value: 'all', label: 'All Rewards', icon: '🎁' },
    { value: 'affordable', label: 'Affordable', icon: '💰' },
    { value: 'digital', label: 'Digital', icon: '📱' },
    { value: 'physical', label: 'Physical', icon: '📦' },
    { value: 'discount', label: 'Discounts', icon: '🏷️' }
  ];

  if (loading) {
    return (
      <div className="reward-catalog">
        <div className="loading-state">
          <div className="loading-spinner"></div>
          <p>Loading reward catalog...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="reward-catalog">
        <div className="error-state">
          <div className="error-icon">❌</div>
          <h3>Error Loading Rewards</h3>
          <p>{error}</p>
          <button className="retry-btn" onClick={fetchRewards}>
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="reward-catalog">
      <div className="catalog-header">
        <div className="header-content">
          <h3>🎁 Reward Catalog</h3>
          <p>Redeem your points for amazing rewards</p>
        </div>
        {isAuthenticated && (
          <div className="user-points">
            <div className="points-display">
              <span className="points-icon">⭐</span>
              <span className="points-amount">{userPoints}</span>
              <span className="points-label">Points</span>
            </div>
          </div>
        )}
      </div>

      <div className="catalog-filters">
        {categories.map(category => (
          <button
            key={category.value}
            className={`filter-btn ${filter === category.value ? 'active' : ''}`}
            onClick={() => setFilter(category.value)}
          >
            <span className="filter-icon">{category.icon}</span>
            <span className="filter-label">{category.label}</span>
          </button>
        ))}
      </div>

      <div className="rewards-grid">
        {filteredRewards.length === 0 ? (
          <div className="no-rewards">
            <div className="no-rewards-icon">🎁</div>
            <h4>No Rewards Available</h4>
            <p>Check back later for new rewards!</p>
          </div>
        ) : (
          filteredRewards.map(reward => (
            <div
              key={reward.id}
              className={`reward-card ${!isAvailable(reward) ? 'unavailable' : ''} ${
                !canAfford(reward.points_required) ? 'unaffordable' : ''
              }`}
            >
              <div className="reward-image">
                {reward.image_url ? (
                  <img src={reward.image_url} alt={reward.name} />
                ) : (
                  <div className="image-placeholder">
                    <span className="placeholder-icon">
                      {reward.type === 'digital' ? '📱' :
                       reward.type === 'discount' ? '🏷️' : '📦'}
                    </span>
                  </div>
                )}
                {!isAvailable(reward) && (
                  <div className="unavailable-overlay">
                    <span>Out of Stock</span>
                  </div>
                )}
              </div>

              <div className="reward-info">
                <div className="reward-header">
                  <h4 className="reward-name">{reward.name}</h4>
                  <div className="reward-type">
                    <span className={`type-badge ${reward.type}`}>
                      {reward.type?.toUpperCase()}
                    </span>
                  </div>
                </div>

                <p className="reward-description">{reward.description}</p>

                <div className="reward-details">
                  <div className="points-required">
                    <span className="points-icon">⭐</span>
                    <span className="points-text">{reward.points_required} Points</span>
                  </div>

                  {reward.value && (
                    <div className="reward-value">
                      <span className="value-label">Value:</span>
                      <span className="value-amount">₹{reward.value}</span>
                    </div>
                  )}

                  {reward.stock !== null && (
                    <div className="stock-info">
                      <span className="stock-label">Stock:</span>
                      <span className="stock-amount">{reward.stock} left</span>
                    </div>
                  )}

                  {reward.expiry_date && (
                    <div className="expiry-info">
                      <span className="expiry-label">Expires:</span>
                      <span className="expiry-date">
                        {new Date(reward.expiry_date).toLocaleDateString()}
                      </span>
                    </div>
                  )}
                </div>

                <div className="reward-actions">
                  {!isAuthenticated ? (
                    <button className="btn-login">
                      Login to Redeem
                    </button>
                  ) : !isAvailable(reward) ? (
                    <button className="btn-unavailable" disabled>
                      Out of Stock
                    </button>
                  ) : !canAfford(reward.points_required) ? (
                    <button className="btn-unaffordable" disabled>
                      Need {reward.points_required - userPoints} More Points
                    </button>
                  ) : (
                    <button
                      className="btn-redeem"
                      onClick={() => handleRedeem(reward.id)}
                      disabled={redeeming === reward.id}
                    >
                      {redeeming === reward.id ? 'Redeeming...' : 'Redeem Now'}
                    </button>
                  )}
                </div>
              </div>

              {reward.popular && (
                <div className="popular-badge">
                  🔥 Popular
                </div>
              )}

              {reward.limited_time && (
                <div className="limited-badge">
                  ⏰ Limited Time
                </div>
              )}
            </div>
          ))
        )}
      </div>

      <div className="catalog-footer">
        <div className="earning-tips">
          <h4>💡 How to Earn More Points</h4>
          <div className="tips-list">
            <div className="tip-item">
              <span className="tip-icon">📸</span>
              <span className="tip-text">Classify waste items: +10 points each</span>
            </div>
            <div className="tip-item">
              <span className="tip-icon">📅</span>
              <span className="tip-text">Book waste collection: +50 points</span>
            </div>
            <div className="tip-item">
              <span className="tip-icon">🔄</span>
              <span className="tip-text">Complete services: +100 points</span>
            </div>
            <div className="tip-item">
              <span className="tip-icon">🏆</span>
              <span className="tip-text">Earn achievements: +25-500 points</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RewardCatalog;