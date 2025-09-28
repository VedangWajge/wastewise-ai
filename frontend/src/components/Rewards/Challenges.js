import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import apiService from '../../services/api';

const Challenges = () => {
  const { isAuthenticated } = useAuth();
  const [challenges, setChallenges] = useState([]);
  const [userChallenges, setUserChallenges] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('available');

  useEffect(() => {
    fetchChallenges();
    if (isAuthenticated) {
      fetchUserChallenges();
    }
  }, [isAuthenticated]);

  const fetchChallenges = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiService.getChallenges();
      if (response.success) {
        setChallenges(response.challenges || []);
      }
    } catch (error) {
      console.error('Error fetching challenges:', error);
      setError('Failed to load challenges');
    } finally {
      setLoading(false);
    }
  };

  const fetchUserChallenges = async () => {
    try {
      const response = await apiService.getUserChallenges();
      if (response.success) {
        setUserChallenges(response.user_challenges || []);
      }
    } catch (error) {
      console.error('Error fetching user challenges:', error);
    }
  };

  const handleJoinChallenge = async (challengeId) => {
    if (!isAuthenticated) {
      alert('Please login to join challenges');
      return;
    }

    try {
      const response = await apiService.joinChallenge(challengeId);
      if (response.success) {
        alert('Successfully joined the challenge!');
        fetchUserChallenges();
      } else {
        alert(response.message || 'Failed to join challenge');
      }
    } catch (error) {
      console.error('Error joining challenge:', error);
      alert('Failed to join challenge. Please try again.');
    }
  };

  const getChallengeProgress = (challengeId) => {
    const userChallenge = userChallenges.find(uc => uc.challenge_id === challengeId);
    return userChallenge || null;
  };

  const isJoined = (challengeId) => {
    return userChallenges.some(uc => uc.challenge_id === challengeId);
  };

  const formatTimeRemaining = (endDate) => {
    const now = new Date();
    const end = new Date(endDate);
    const diff = end - now;

    if (diff <= 0) return 'Expired';

    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));

    if (days > 0) return `${days} days left`;
    if (hours > 0) return `${hours} hours left`;
    return 'Less than 1 hour left';
  };

  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'easy':
        return '#4CAF50';
      case 'medium':
        return '#FF9800';
      case 'hard':
        return '#f44336';
      default:
        return '#757575';
    }
  };

  const getChallengeIcon = (type) => {
    switch (type) {
      case 'classification':
        return '📸';
      case 'booking':
        return '📅';
      case 'recycling':
        return '♻️';
      case 'streak':
        return '🔥';
      case 'environmental':
        return '🌱';
      default:
        return '🎯';
    }
  };

  const availableChallenges = challenges.filter(challenge => {
    const now = new Date();
    const end = new Date(challenge.end_date);
    return end > now && (!isAuthenticated || !isJoined(challenge.id));
  });

  const activeChallenges = challenges.filter(challenge => {
    return isAuthenticated && isJoined(challenge.id) && !getChallengeProgress(challenge.id)?.completed;
  });

  const completedChallenges = challenges.filter(challenge => {
    return isAuthenticated && getChallengeProgress(challenge.id)?.completed;
  });

  const renderChallengeCard = (challenge, showProgress = false) => {
    const progress = getChallengeProgress(challenge.id);
    const progressPercentage = progress
      ? Math.min(100, (progress.current_progress / challenge.target) * 100)
      : 0;

    return (
      <div key={challenge.id} className="challenge-card">
        <div className="challenge-header">
          <div className="challenge-icon">
            {getChallengeIcon(challenge.type)}
          </div>
          <div className="challenge-info">
            <h4 className="challenge-name">{challenge.name}</h4>
            <p className="challenge-description">{challenge.description}</p>
          </div>
          <div
            className="difficulty-badge"
            style={{ backgroundColor: getDifficultyColor(challenge.difficulty) }}
          >
            {challenge.difficulty?.toUpperCase()}
          </div>
        </div>

        <div className="challenge-details">
          <div className="challenge-target">
            <span className="target-label">Target:</span>
            <span className="target-value">
              {challenge.target} {challenge.unit || 'items'}
            </span>
          </div>

          <div className="challenge-reward">
            <span className="reward-label">Reward:</span>
            <span className="reward-value">⭐ {challenge.reward_points} points</span>
          </div>

          <div className="challenge-duration">
            <span className="duration-label">Duration:</span>
            <span className="duration-value">{challenge.duration_days} days</span>
          </div>

          <div className="challenge-deadline">
            <span className="deadline-label">Ends:</span>
            <span className="deadline-value">{formatTimeRemaining(challenge.end_date)}</span>
          </div>
        </div>

        {showProgress && progress && (
          <div className="challenge-progress">
            <div className="progress-header">
              <span className="progress-label">Progress</span>
              <span className="progress-text">
                {progress.current_progress} / {challenge.target}
              </span>
            </div>
            <div className="progress-bar">
              <div
                className="progress-fill"
                style={{ width: `${progressPercentage}%` }}
              ></div>
            </div>
            <span className="progress-percentage">{progressPercentage.toFixed(0)}%</span>
          </div>
        )}

        <div className="challenge-actions">
          {!isAuthenticated ? (
            <button className="btn-login">Login to Join</button>
          ) : !isJoined(challenge.id) ? (
            <button
              className="btn-join"
              onClick={() => handleJoinChallenge(challenge.id)}
            >
              Join Challenge
            </button>
          ) : progress?.completed ? (
            <button className="btn-completed" disabled>
              ✅ Completed
            </button>
          ) : (
            <button className="btn-active" disabled>
              🎯 In Progress
            </button>
          )}
        </div>

        {challenge.participants_count && (
          <div className="challenge-participants">
            👥 {challenge.participants_count} participants
          </div>
        )}
      </div>
    );
  };

  if (loading) {
    return (
      <div className="challenges">
        <div className="loading-state">
          <div className="loading-spinner"></div>
          <p>Loading challenges...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="challenges">
        <div className="error-state">
          <div className="error-icon">❌</div>
          <h3>Error Loading Challenges</h3>
          <p>{error}</p>
          <button className="retry-btn" onClick={fetchChallenges}>
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="challenges">
      <div className="challenges-header">
        <h3>🎯 Challenges</h3>
        <p>Complete challenges to earn points and unlock achievements</p>
      </div>

      <div className="challenges-navigation">
        <button
          className={`nav-tab ${activeTab === 'available' ? 'active' : ''}`}
          onClick={() => setActiveTab('available')}
        >
          <span className="tab-icon">🎯</span>
          <span className="tab-label">Available ({availableChallenges.length})</span>
        </button>

        {isAuthenticated && (
          <>
            <button
              className={`nav-tab ${activeTab === 'active' ? 'active' : ''}`}
              onClick={() => setActiveTab('active')}
            >
              <span className="tab-icon">🔥</span>
              <span className="tab-label">Active ({activeChallenges.length})</span>
            </button>

            <button
              className={`nav-tab ${activeTab === 'completed' ? 'active' : ''}`}
              onClick={() => setActiveTab('completed')}
            >
              <span className="tab-icon">✅</span>
              <span className="tab-label">Completed ({completedChallenges.length})</span>
            </button>
          </>
        )}
      </div>

      <div className="challenges-content">
        {activeTab === 'available' && (
          <div className="challenges-grid">
            {availableChallenges.length === 0 ? (
              <div className="no-challenges">
                <div className="no-challenges-icon">🎯</div>
                <h4>No Available Challenges</h4>
                <p>Check back later for new challenges!</p>
              </div>
            ) : (
              availableChallenges.map(challenge => renderChallengeCard(challenge))
            )}
          </div>
        )}

        {activeTab === 'active' && (
          <div className="challenges-grid">
            {activeChallenges.length === 0 ? (
              <div className="no-challenges">
                <div className="no-challenges-icon">🔥</div>
                <h4>No Active Challenges</h4>
                <p>Join a challenge to start earning points!</p>
              </div>
            ) : (
              activeChallenges.map(challenge => renderChallengeCard(challenge, true))
            )}
          </div>
        )}

        {activeTab === 'completed' && (
          <div className="challenges-grid">
            {completedChallenges.length === 0 ? (
              <div className="no-challenges">
                <div className="no-challenges-icon">✅</div>
                <h4>No Completed Challenges</h4>
                <p>Complete your first challenge to see it here!</p>
              </div>
            ) : (
              completedChallenges.map(challenge => renderChallengeCard(challenge, true))
            )}
          </div>
        )}
      </div>

      <div className="challenges-info">
        <h4>💡 Challenge Tips</h4>
        <div className="tips-list">
          <div className="tip-item">
            <span className="tip-icon">🎯</span>
            <span className="tip-text">Join challenges early to have more time to complete them</span>
          </div>
          <div className="tip-item">
            <span className="tip-icon">📈</span>
            <span className="tip-text">Focus on easier challenges first to build momentum</span>
          </div>
          <div className="tip-item">
            <span className="tip-icon">🔄</span>
            <span className="tip-text">Daily activity helps you complete streak challenges</span>
          </div>
          <div className="tip-item">
            <span className="tip-icon">🏆</span>
            <span className="tip-text">Completing challenges unlocks special badges</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Challenges;