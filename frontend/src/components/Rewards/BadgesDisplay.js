import React from 'react';

const BadgesDisplay = ({ badges = [], earnedBadges = [] }) => {
  const getBadgeStatus = (badge) => {
    return earnedBadges.some(earned => earned.badge_id === badge.id);
  };

  const getBadgeProgress = (badge) => {
    const earned = earnedBadges.find(earned => earned.badge_id === badge.id);
    if (earned) return 100;

    // Calculate progress based on current user stats (would come from props)
    return Math.min(100, ((badge.current_progress || 0) / badge.requirement) * 100);
  };

  const formatRequirement = (badge) => {
    switch (badge.type) {
      case 'classification':
        return `Classify ${badge.requirement} waste items`;
      case 'booking':
        return `Book ${badge.requirement} waste collection services`;
      case 'recycling':
        return `Recycle ${badge.requirement} kg of waste`;
      case 'streak':
        return `${badge.requirement} day streak of activity`;
      default:
        return badge.description || 'Complete the challenge';
    }
  };

  return (
    <div className="badges-display">
      <div className="badges-header">
        <h3>🏆 Badges & Achievements</h3>
        <div className="badges-stats">
          <span className="earned-count">
            {earnedBadges.length} of {badges.length} badges earned
          </span>
        </div>
      </div>

      <div className="badges-grid">
        {badges.map(badge => {
          const isEarned = getBadgeStatus(badge);
          const progress = getBadgeProgress(badge);

          return (
            <div
              key={badge.id}
              className={`badge-card ${isEarned ? 'earned' : 'locked'}`}
            >
              <div className="badge-icon-container">
                <div className="badge-icon">
                  {isEarned ? badge.icon : '🔒'}
                </div>
                {isEarned && (
                  <div className="earned-indicator">✅</div>
                )}
              </div>

              <div className="badge-info">
                <h4 className="badge-name">{badge.name}</h4>
                <p className="badge-description">
                  {formatRequirement(badge)}
                </p>

                {!isEarned && (
                  <div className="badge-progress">
                    <div className="progress-bar">
                      <div
                        className="progress-fill"
                        style={{ width: `${progress}%` }}
                      ></div>
                    </div>
                    <span className="progress-text">
                      {badge.current_progress || 0} / {badge.requirement}
                    </span>
                  </div>
                )}

                {isEarned && (
                  <div className="badge-earned-info">
                    <span className="points-earned">+{badge.points} points</span>
                    <span className="earned-date">
                      Earned: {new Date(earnedBadges.find(e => e.badge_id === badge.id)?.earned_at).toLocaleDateString()}
                    </span>
                  </div>
                )}
              </div>

              <div className="badge-rarity">
                <span className={`rarity-indicator ${badge.rarity || 'common'}`}>
                  {badge.rarity?.toUpperCase() || 'COMMON'}
                </span>
              </div>
            </div>
          );
        })}
      </div>

      {badges.length === 0 && (
        <div className="no-badges">
          <div className="no-badges-icon">🏆</div>
          <h4>No Badges Available</h4>
          <p>Start using WasteWise to unlock achievements!</p>
        </div>
      )}

      <div className="badges-categories">
        <h4>Badge Categories</h4>
        <div className="categories-list">
          <div className="category-item">
            <span className="category-icon">📸</span>
            <div className="category-info">
              <span className="category-name">Classification Master</span>
              <span className="category-desc">Badges for waste classification</span>
            </div>
          </div>
          <div className="category-item">
            <span className="category-icon">📅</span>
            <div className="category-info">
              <span className="category-name">Service Champion</span>
              <span className="category-desc">Badges for booking services</span>
            </div>
          </div>
          <div className="category-item">
            <span className="category-icon">♻️</span>
            <div className="category-info">
              <span className="category-name">Eco Warrior</span>
              <span className="category-desc">Badges for environmental impact</span>
            </div>
          </div>
          <div className="category-item">
            <span className="category-icon">🔥</span>
            <div className="category-info">
              <span className="category-name">Streak Legend</span>
              <span className="category-desc">Badges for consistent activity</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BadgesDisplay;