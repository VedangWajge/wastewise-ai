import React from 'react';
import './PointsDisplay.css';

const PointsDisplay = ({ userPoints }) => {
  if (!userPoints) {
    return (
      <div className="points-display">
        <div className="loading-state">
          <div className="loading-spinner"></div>
          <p>Loading points data...</p>
        </div>
      </div>
    );
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="points-display">
      <div className="points-summary-card">
        <div className="summary-header">
          <h2>💎 Your Points Summary</h2>
        </div>

        <div className="summary-stats">
          <div className="stat-card current-balance">
            <div className="stat-icon">💰</div>
            <div className="stat-content">
              <span className="stat-number">{userPoints.current_balance}</span>
              <span className="stat-label">Available Points</span>
            </div>
          </div>

          <div className="stat-card weekly-earned">
            <div className="stat-icon">📅</div>
            <div className="stat-content">
              <span className="stat-number">{userPoints.weekly_earned}</span>
              <span className="stat-label">This Week</span>
            </div>
          </div>

          <div className="stat-card total-earned">
            <div className="stat-icon">🏆</div>
            <div className="stat-content">
              <span className="stat-number">{userPoints.total_earned}</span>
              <span className="stat-label">Total Earned</span>
            </div>
          </div>

          <div className="stat-card total-spent">
            <div className="stat-icon">🛒</div>
            <div className="stat-content">
              <span className="stat-number">{userPoints.total_spent}</span>
              <span className="stat-label">Total Spent</span>
            </div>
          </div>
        </div>
      </div>

      <div className="earning-opportunities">
        <h3>🌟 Ways to Earn Points</h3>
        <div className="opportunities-grid">
          <div className="opportunity-card">
            <div className="opportunity-icon">📸</div>
            <div className="opportunity-content">
              <h4>Classify Waste</h4>
              <p>Earn 10 points for each waste classification</p>
              <span className="points-reward">+10 points</span>
            </div>
          </div>

          <div className="opportunity-card">
            <div className="opportunity-icon">📅</div>
            <div className="opportunity-content">
              <h4>Book Collection</h4>
              <p>Get 25 points when you book a waste collection service</p>
              <span className="points-reward">+25 points</span>
            </div>
          </div>

          <div className="opportunity-card">
            <div className="opportunity-icon">✅</div>
            <div className="opportunity-content">
              <h4>Complete Booking</h4>
              <p>Earn 50 points when your booking is completed</p>
              <span className="points-reward">+50 points</span>
            </div>
          </div>

          <div className="opportunity-card">
            <div className="opportunity-icon">⭐</div>
            <div className="opportunity-content">
              <h4>Rate Service</h4>
              <p>Get 15 points for rating a completed service</p>
              <span className="points-reward">+15 points</span>
            </div>
          </div>

          <div className="opportunity-card">
            <div className="opportunity-icon">🎯</div>
            <div className="opportunity-content">
              <h4>Complete Challenges</h4>
              <p>Earn bonus points by completing weekly challenges</p>
              <span className="points-reward">+100-500 points</span>
            </div>
          </div>

          <div className="opportunity-card">
            <div className="opportunity-icon">📊</div>
            <div className="opportunity-content">
              <h4>Daily Login</h4>
              <p>Get 5 points for logging in daily</p>
              <span className="points-reward">+5 points</span>
            </div>
          </div>
        </div>
      </div>

      {userPoints.recent_transactions && userPoints.recent_transactions.length > 0 && (
        <div className="recent-transactions">
          <h3>📋 Recent Transactions</h3>
          <div className="transactions-list">
            {userPoints.recent_transactions.map(transaction => (
              <div key={transaction.id} className="transaction-item">
                <div className="transaction-icon">
                  {transaction.type === 'earned' ? '💰' : '🛒'}
                </div>
                <div className="transaction-content">
                  <div className="transaction-reason">{transaction.reason}</div>
                  <div className="transaction-date">{formatDate(transaction.created_at)}</div>
                </div>
                <div className={`transaction-points ${transaction.type}`}>
                  {transaction.type === 'earned' ? '+' : '-'}{transaction.points}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="points-tips">
        <h3>💡 Tips to Maximize Points</h3>
        <div className="tips-list">
          <div className="tip-item">
            <span className="tip-icon">🔥</span>
            <span className="tip-text">Classify waste regularly to build up streaks and earn bonus points</span>
          </div>
          <div className="tip-item">
            <span className="tip-icon">🎯</span>
            <span className="tip-text">Focus on completing weekly challenges for maximum rewards</span>
          </div>
          <div className="tip-item">
            <span className="tip-icon">⭐</span>
            <span className="tip-text">Always rate your services to help the community and earn points</span>
          </div>
          <div className="tip-item">
            <span className="tip-icon">📱</span>
            <span className="tip-text">Check in daily to maintain your login streak</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PointsDisplay;