import React, { useState, useEffect } from 'react';
import apiService from '../services/api';
import './Dashboard.css';

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchStatistics();
  }, []);

  const fetchStatistics = async () => {
    try {
      setLoading(true);
      const data = await apiService.getStatistics();
      setStats(data);
      setError(null);
    } catch (err) {
      setError('Failed to load statistics');
      console.error('Error fetching statistics:', err);
    } finally {
      setLoading(false);
    }
  };

  const getWasteIcon = (wasteType) => {
    const icons = {
      plastic: '♻️',
      organic: '🌱',
      paper: '📄',
      glass: '🗞️',
      metal: '🔧'
    };
    return icons[wasteType] || '🗑️';
  };

  const getWasteColor = (wasteType) => {
    const colors = {
      plastic: '#2196f3',
      organic: '#4caf50',
      paper: '#ff9800',
      glass: '#00bcd4',
      metal: '#607d8b'
    };
    return colors[wasteType] || '#9e9e9e';
  };

  if (loading) {
    return (
      <div className="dashboard-container">
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Loading statistics...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-container">
        <div className="error-message">
          <p>{error}</p>
          <button className="btn btn-primary" onClick={fetchStatistics}>
            Try Again
          </button>
        </div>
      </div>
    );
  }

  const totalWaste = Object.values(stats.waste_breakdown).reduce((sum, count) => sum + count, 0);

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>📊 Waste Classification Dashboard</h1>
        <p>Track your environmental impact with AI-powered waste analysis</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card highlight">
          <div className="stat-icon">🎯</div>
          <div className="stat-content">
            <h3>Total Classifications</h3>
            <p className="stat-number">{stats.total_classifications}</p>
            <span className="stat-label">Items analyzed</span>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">♻️</div>
          <div className="stat-content">
            <h3>Recycling Rate</h3>
            <p className="stat-number">{stats.recycling_rate}%</p>
            <span className="stat-label">Successfully recycled</span>
          </div>
        </div>
      </div>

      <div className="waste-breakdown-section">
        <h2>🗑️ Waste Type Breakdown</h2>
        <div className="waste-grid">
          {Object.entries(stats.waste_breakdown).map(([type, count]) => {
            const percentage = ((count / totalWaste) * 100).toFixed(1);
            return (
              <div key={type} className="waste-card">
                <div className="waste-card-header">
                  <span className="waste-card-icon">
                    {getWasteIcon(type)}
                  </span>
                  <h3>{type.charAt(0).toUpperCase() + type.slice(1)}</h3>
                </div>
                <div className="waste-card-content">
                  <p className="waste-count">{count}</p>
                  <p className="waste-percentage">{percentage}%</p>
                  <div className="waste-progress">
                    <div
                      className="waste-progress-fill"
                      style={{
                        width: `${percentage}%`,
                        backgroundColor: getWasteColor(type)
                      }}
                    ></div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      <div className="environmental-impact-section">
        <h2>🌍 Environmental Impact</h2>
        <div className="impact-grid">
          <div className="impact-card">
            <div className="impact-icon">🌱</div>
            <h3>CO₂ Saved</h3>
            <p className="impact-value">{stats.environmental_impact.co2_saved}</p>
            <span className="impact-description">Carbon footprint reduced</span>
          </div>

          <div className="impact-card">
            <div className="impact-icon">💧</div>
            <h3>Water Saved</h3>
            <p className="impact-value">{stats.environmental_impact.water_saved}</p>
            <span className="impact-description">Water conservation achieved</span>
          </div>

          <div className="impact-card">
            <div className="impact-icon">⚡</div>
            <h3>Energy Saved</h3>
            <p className="impact-value">{stats.environmental_impact.energy_saved}</p>
            <span className="impact-description">Energy conservation impact</span>
          </div>
        </div>
      </div>

      <div className="dashboard-footer">
        <button className="btn btn-primary" onClick={fetchStatistics}>
          🔄 Refresh Data
        </button>
        <p className="last-updated">
          Last updated: {new Date().toLocaleString()}
        </p>
      </div>
    </div>
  );
};

export default Dashboard;