import React from 'react';

const WasteTrends = ({ data, period }) => {
  if (!data) {
    return (
      <div className="waste-trends">
        <p>No waste trends data available</p>
      </div>
    );
  }

  return (
    <div className="waste-trends">
      <div className="trends-section">
        <h3>Waste Trends - {period}</h3>

        <div className="trend-overview">
          <div className="trend-card">
            <h4>Total Waste Trend</h4>
            <div className="trend-chart">
              <div className="trend-value">
                {data.waste_trend > 0 ? '📈' : '📉'} {Math.abs(data.waste_trend || 0)}%
              </div>
              <p className={data.waste_trend > 0 ? 'trend-up' : 'trend-down'}>
                {data.waste_trend > 0 ? 'Increase' : 'Decrease'} from last {period}
              </p>
            </div>
          </div>

          <div className="trend-card">
            <h4>Classification Trend</h4>
            <div className="trend-chart">
              <div className="trend-value">
                {data.classification_trend > 0 ? '📈' : '📉'} {Math.abs(data.classification_trend || 0)}%
              </div>
              <p className={data.classification_trend > 0 ? 'trend-up' : 'trend-down'}>
                {data.classification_trend > 0 ? 'More' : 'Fewer'} classifications
              </p>
            </div>
          </div>

          <div className="trend-card">
            <h4>Recycling Rate</h4>
            <div className="trend-chart">
              <div className="trend-value">
                ♻️ {data.recycling_rate || 0}%
              </div>
              <p>Of total waste recycled</p>
            </div>
          </div>
        </div>

        <div className="daily-trends">
          <h4>Daily Classification Activity</h4>
          <div className="daily-chart">
            {data.daily_classifications?.map((day, index) => (
              <div key={index} className="day-bar">
                <div
                  className="bar"
                  style={{
                    height: `${Math.max(10, (day.count / Math.max(...data.daily_classifications.map(d => d.count))) * 100)}%`
                  }}
                ></div>
                <span className="day-label">{day.date}</span>
                <span className="day-count">{day.count}</span>
              </div>
            )) || <p>No daily data available</p>}
          </div>
        </div>

        <div className="waste-categories">
          <h4>Waste Type Distribution</h4>
          <div className="category-breakdown">
            {data.waste_type_distribution?.map((type, index) => (
              <div key={index} className="category-item">
                <div className="category-header">
                  <span className="category-icon">{type.icon}</span>
                  <span className="category-name">{type.name}</span>
                  <span className="category-percentage">{type.percentage}%</span>
                </div>
                <div className="category-bar">
                  <div
                    className="category-fill"
                    style={{
                      width: `${type.percentage}%`,
                      backgroundColor: type.color || '#4CAF50'
                    }}
                  ></div>
                </div>
                <div className="category-details">
                  <span>{type.count || 0} items</span>
                  <span>{type.weight || 0} kg</span>
                </div>
              </div>
            )) || <p>No waste type data available</p>}
          </div>
        </div>

        <div className="trend-insights">
          <h4>📊 Trend Insights</h4>
          <div className="insights-list">
            <div className="insight-item">
              <span className="insight-icon">
                {data.classification_trend > 0 ? '🔝' : '🔻'}
              </span>
              <div className="insight-text">
                <strong>Classification Activity:</strong>
                {data.classification_trend > 0
                  ? ` You've been more active in waste classification this ${period}`
                  : ` Your classification activity has decreased this ${period}`
                }
              </div>
            </div>

            <div className="insight-item">
              <span className="insight-icon">♻️</span>
              <div className="insight-text">
                <strong>Recycling Performance:</strong>
                {(data.recycling_rate || 0) > 70
                  ? ' Excellent recycling rate! Keep up the great work'
                  : ' There\'s room to improve your recycling habits'
                }
              </div>
            </div>

            <div className="insight-item">
              <span className="insight-icon">🎯</span>
              <div className="insight-text">
                <strong>Goal Progress:</strong>
                {data.goal_progress
                  ? ` You're ${data.goal_progress}% towards your waste reduction goal`
                  : ' Set a waste reduction goal to track your progress'
                }
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WasteTrends;