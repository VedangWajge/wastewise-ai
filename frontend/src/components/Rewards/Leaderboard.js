import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import apiService from '../../services/api';

const Leaderboard = () => {
  const { user, isAuthenticated } = useAuth();
  const [leaderboardData, setLeaderboardData] = useState([]);
  const [userRank, setUserRank] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [timeframe, setTimeframe] = useState('monthly');
  const [category, setCategory] = useState('points');

  useEffect(() => {
    fetchLeaderboard();
  }, [timeframe, category]); // eslint-disable-line react-hooks/exhaustive-deps

  const fetchLeaderboard = async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await apiService.getLeaderboard({
        timeframe,
        category,
        limit: 50
      });

      if (response.success) {
        setLeaderboardData(response.leaderboard || []);
        setUserRank(response.user_rank || null);
      }
    } catch (error) {
      console.error('Error fetching leaderboard:', error);
      setError('Failed to load leaderboard data');
    } finally {
      setLoading(false);
    }
  };

  const getRankIcon = (rank) => {
    switch (rank) {
      case 1:
        return '🥇';
      case 2:
        return '🥈';
      case 3:
        return '🥉';
      default:
        return `#${rank}`;
    }
  };

  const getRankClass = (rank) => {
    if (rank <= 3) return `rank-${rank}`;
    if (rank <= 10) return 'rank-top10';
    return 'rank-normal';
  };

  const formatValue = (value, type) => {
    switch (type) {
      case 'points':
        return `${value} pts`;
      case 'classifications':
        return `${value} items`;
      case 'waste_processed':
        return `${value} kg`;
      case 'carbon_saved':
        return `${value} kg CO₂`;
      default:
        return value;
    }
  };

  if (loading) {
    return (
      <div className="leaderboard">
        <div className="loading-state">
          <div className="loading-spinner"></div>
          <p>Loading leaderboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="leaderboard">
        <div className="error-state">
          <div className="error-icon">❌</div>
          <h3>Error Loading Leaderboard</h3>
          <p>{error}</p>
          <button className="retry-btn" onClick={fetchLeaderboard}>
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="leaderboard">
      <div className="leaderboard-header">
        <h3>🏆 Leaderboard</h3>
        <div className="leaderboard-controls">
          <select
            value={timeframe}
            onChange={(e) => setTimeframe(e.target.value)}
            className="timeframe-selector"
          >
            <option value="weekly">This Week</option>
            <option value="monthly">This Month</option>
            <option value="quarterly">This Quarter</option>
            <option value="yearly">This Year</option>
            <option value="all-time">All Time</option>
          </select>

          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="category-selector"
          >
            <option value="points">Points</option>
            <option value="classifications">Classifications</option>
            <option value="waste_processed">Waste Processed</option>
            <option value="carbon_saved">Carbon Saved</option>
          </select>
        </div>
      </div>

      {isAuthenticated && userRank && (
        <div className="user-rank-card">
          <div className="rank-info">
            <span className="rank-position">{getRankIcon(userRank.rank)}</span>
            <div className="rank-details">
              <span className="rank-text">Your Rank</span>
              <span className="rank-value">
                {formatValue(userRank.value, category)}
              </span>
            </div>
          </div>
          <div className="rank-progress">
            {userRank.rank > 1 && (
              <div className="next-rank">
                <span>Need {formatValue(userRank.gap_to_next || 0, category)} to reach #{userRank.rank - 1}</span>
              </div>
            )}
          </div>
        </div>
      )}

      <div className="leaderboard-list">
        {leaderboardData.length === 0 ? (
          <div className="no-data">
            <div className="no-data-icon">📊</div>
            <h4>No Data Available</h4>
            <p>Be the first to appear on the leaderboard!</p>
          </div>
        ) : (
          leaderboardData.map((entry, index) => (
            <div
              key={entry.user_id}
              className={`leaderboard-entry ${getRankClass(entry.rank)} ${
                isAuthenticated && entry.user_id === user?.id ? 'current-user' : ''
              }`}
            >
              <div className="entry-rank">
                <span className="rank-icon">{getRankIcon(entry.rank)}</span>
              </div>

              <div className="entry-user">
                <div className="user-avatar">
                  {entry.avatar_url ? (
                    <img src={entry.avatar_url} alt={entry.username} />
                  ) : (
                    <div className="avatar-placeholder">
                      {entry.username?.charAt(0)?.toUpperCase() || '?'}
                    </div>
                  )}
                </div>
                <div className="user-info">
                  <span className="username">
                    {entry.username || 'Anonymous User'}
                    {isAuthenticated && entry.user_id === user?.id && (
                      <span className="you-indicator">(You)</span>
                    )}
                  </span>
                  <span className="user-level">Level {entry.level || 1}</span>
                </div>
              </div>

              <div className="entry-stats">
                <div className="primary-stat">
                  <span className="stat-value">
                    {formatValue(entry.value, category)}
                  </span>
                </div>
                <div className="secondary-stats">
                  {entry.badges_count > 0 && (
                    <span className="badge-count">🏆 {entry.badges_count}</span>
                  )}
                  {entry.streak > 0 && (
                    <span className="streak">🔥 {entry.streak}</span>
                  )}
                </div>
              </div>

              <div className="entry-trend">
                {entry.trend && (
                  <span className={`trend ${entry.trend > 0 ? 'up' : 'down'}`}>
                    {entry.trend > 0 ? '↗️' : '↘️'} {Math.abs(entry.trend)}
                  </span>
                )}
              </div>
            </div>
          ))
        )}
      </div>

      <div className="leaderboard-footer">
        <div className="competition-info">
          <h4>🎯 Current Competition</h4>
          <p>Compete with other users to reduce waste and earn rewards!</p>
          <div className="competition-prizes">
            <div className="prize">🥇 1st Place: 1000 bonus points</div>
            <div className="prize">🥈 2nd Place: 500 bonus points</div>
            <div className="prize">🥉 3rd Place: 250 bonus points</div>
          </div>
        </div>

        {!isAuthenticated && (
          <div className="login-prompt">
            <p>Login to see your rank and compete with others!</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Leaderboard;