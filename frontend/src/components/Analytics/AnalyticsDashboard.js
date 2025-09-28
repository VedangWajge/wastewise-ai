import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import apiService from '../../services/api';
import PersonalAnalytics from './PersonalAnalytics';
import EnvironmentalImpact from './EnvironmentalImpact';
import WasteTrends from './WasteTrends';
import './AnalyticsDashboard.css';

const AnalyticsDashboard = () => {
  const { user, isAuthenticated } = useAuth();
  const [activeTab, setActiveTab] = useState('overview');
  const [analyticsData, setAnalyticsData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [period, setPeriod] = useState('month');

  useEffect(() => {
    if (isAuthenticated) {
      fetchAnalyticsData();
    }
  }, [isAuthenticated, period]);

  const fetchAnalyticsData = async () => {
    try {
      setLoading(true);
      setError(null);

      const [personalResponse, insightsResponse] = await Promise.all([
        apiService.getPersonalAnalytics(period, true),
        apiService.getAIInsights()
      ]);

      if (personalResponse.success) {
        setAnalyticsData({
          personal: personalResponse.analytics,
          insights: insightsResponse.success ? insightsResponse.insights : null
        });
      }
    } catch (error) {
      console.error('Error fetching analytics:', error);
      setError(error.message || 'Failed to load analytics data');
    } finally {
      setLoading(false);
    }
  };

  const handleExportData = async () => {
    try {
      const response = await apiService.exportAnalyticsData({
        type: 'personal',
        format: 'json',
        period: period,
        include_charts: false
      });

      if (response.success) {
        // Create and download file
        const blob = new Blob([JSON.stringify(response.data, null, 2)], {
          type: 'application/json'
        });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `wastewise-analytics-${period}-${Date.now()}.json`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);
      }
    } catch (error) {
      console.error('Export error:', error);
      alert('Failed to export data. Please try again.');
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="analytics-dashboard">
        <div className="auth-required">
          <div className="auth-icon">📊</div>
          <h3>Login Required</h3>
          <p>Please login to view your analytics and environmental impact</p>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="analytics-dashboard">
        <div className="loading-state">
          <div className="loading-spinner"></div>
          <p>Loading your analytics...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="analytics-dashboard">
        <div className="error-state">
          <div className="error-icon">❌</div>
          <h3>Error Loading Analytics</h3>
          <p>{error}</p>
          <button className="retry-btn" onClick={fetchAnalyticsData}>
            Try Again
          </button>
        </div>
      </div>
    );
  }

  const tabs = [
    { id: 'overview', label: 'Overview', icon: '📊' },
    { id: 'personal', label: 'Personal Stats', icon: '👤' },
    { id: 'impact', label: 'Environmental Impact', icon: '🌍' },
    { id: 'trends', label: 'Waste Trends', icon: '📈' },
  ];

  const periods = [
    { value: 'week', label: 'This Week' },
    { value: 'month', label: 'This Month' },
    { value: 'quarter', label: 'This Quarter' },
    { value: 'year', label: 'This Year' },
  ];

  const renderOverview = () => {
    if (!analyticsData?.personal) return null;

    const stats = analyticsData.personal;

    return (
      <div className="overview-tab">
        <div className="stats-grid">
          <div className="stat-card primary">
            <div className="stat-icon">♻️</div>
            <div className="stat-content">
              <span className="stat-number">{stats.total_classifications || 0}</span>
              <span className="stat-label">Waste Items Classified</span>
              <span className="stat-trend">
                {stats.classification_trend > 0 ? '+' : ''}{stats.classification_trend || 0}% vs last {period}
              </span>
            </div>
          </div>

          <div className="stat-card success">
            <div className="stat-icon">📅</div>
            <div className="stat-content">
              <span className="stat-number">{stats.total_bookings || 0}</span>
              <span className="stat-label">Services Booked</span>
              <span className="stat-trend">
                {stats.booking_trend > 0 ? '+' : ''}{stats.booking_trend || 0}% vs last {period}
              </span>
            </div>
          </div>

          <div className="stat-card warning">
            <div className="stat-icon">⚖️</div>
            <div className="stat-content">
              <span className="stat-number">{stats.total_waste_processed || 0} kg</span>
              <span className="stat-label">Waste Processed</span>
              <span className="stat-trend">
                {stats.waste_trend > 0 ? '+' : ''}{stats.waste_trend || 0}% vs last {period}
              </span>
            </div>
          </div>

          <div className="stat-card info">
            <div className="stat-icon">🌱</div>
            <div className="stat-content">
              <span className="stat-number">{stats.carbon_saved || 0} kg</span>
              <span className="stat-label">CO₂ Saved</span>
              <span className="stat-trend">Environmental Impact</span>
            </div>
          </div>
        </div>

        <div className="overview-charts">
          <div className="chart-card">
            <h3>Waste Classification Over Time</h3>
            <div className="simple-chart">
              {stats.daily_classifications?.map((day, index) => (
                <div key={index} className="chart-bar">
                  <div
                    className="bar-fill"
                    style={{
                      height: `${(day.count / Math.max(...stats.daily_classifications.map(d => d.count))) * 100}%`
                    }}
                  ></div>
                  <span className="bar-label">{day.date}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="chart-card">
            <h3>Waste Type Distribution</h3>
            <div className="waste-distribution">
              {stats.waste_type_distribution?.map(type => (
                <div key={type.name} className="distribution-item">
                  <div className="type-info">
                    <span className="type-icon">{type.icon}</span>
                    <span className="type-name">{type.name}</span>
                  </div>
                  <div className="type-bar">
                    <div
                      className="type-fill"
                      style={{ width: `${type.percentage}%` }}
                    ></div>
                  </div>
                  <span className="type-percentage">{type.percentage}%</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {analyticsData.insights && (
          <div className="ai-insights">
            <h3>🤖 AI Insights</h3>
            <div className="insights-grid">
              {analyticsData.insights.map((insight, index) => (
                <div key={index} className="insight-card">
                  <div className="insight-icon">{insight.icon}</div>
                  <div className="insight-content">
                    <h4>{insight.title}</h4>
                    <p>{insight.description}</p>
                    {insight.action && (
                      <button className="insight-action">{insight.action}</button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="achievements-section">
          <h3>🏆 Recent Achievements</h3>
          <div className="achievements-list">
            {stats.recent_achievements?.map(achievement => (
              <div key={achievement.id} className="achievement-item">
                <span className="achievement-icon">{achievement.icon}</span>
                <div className="achievement-content">
                  <span className="achievement-title">{achievement.title}</span>
                  <span className="achievement-date">
                    {new Date(achievement.earned_at).toLocaleDateString()}
                  </span>
                </div>
                <span className="achievement-points">+{achievement.points}</span>
              </div>
            ))}
            {(!stats.recent_achievements || stats.recent_achievements.length === 0) && (
              <p className="no-achievements">
                Start classifying waste and booking services to earn achievements!
              </p>
            )}
          </div>
        </div>
      </div>
    );
  };

  const renderTabContent = () => {
    switch (activeTab) {
      case 'overview':
        return renderOverview();
      case 'personal':
        return <PersonalAnalytics data={analyticsData?.personal} period={period} />;
      case 'impact':
        return <EnvironmentalImpact data={analyticsData?.personal} period={period} />;
      case 'trends':
        return <WasteTrends data={analyticsData?.personal} period={period} />;
      default:
        return null;
    }
  };

  return (
    <div className="analytics-dashboard">
      <div className="analytics-header">
        <div className="header-content">
          <h1>📊 Analytics Dashboard</h1>
          <p>Track your waste management progress and environmental impact</p>
        </div>
        <div className="header-controls">
          <select
            value={period}
            onChange={(e) => setPeriod(e.target.value)}
            className="period-selector"
          >
            {periods.map(p => (
              <option key={p.value} value={p.value}>{p.label}</option>
            ))}
          </select>
          <button className="export-btn" onClick={handleExportData}>
            📥 Export Data
          </button>
        </div>
      </div>

      <div className="analytics-navigation">
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

      <div className="analytics-content">
        {renderTabContent()}
      </div>
    </div>
  );
};

export default AnalyticsDashboard;