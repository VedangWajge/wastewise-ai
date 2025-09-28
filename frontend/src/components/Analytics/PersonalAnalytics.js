import React from 'react';

const PersonalAnalytics = ({ data, period }) => {
  if (!data) {
    return (
      <div className="personal-analytics">
        <p>No analytics data available</p>
      </div>
    );
  }

  return (
    <div className="personal-analytics">
      <div className="analytics-section">
        <h3>Personal Statistics - {period}</h3>

        <div className="stats-cards">
          <div className="stat-card">
            <h4>Total Classifications</h4>
            <div className="stat-value">{data.total_classifications || 0}</div>
          </div>

          <div className="stat-card">
            <h4>Total Bookings</h4>
            <div className="stat-value">{data.total_bookings || 0}</div>
          </div>

          <div className="stat-card">
            <h4>Waste Processed</h4>
            <div className="stat-value">{data.total_waste_processed || 0} kg</div>
          </div>

          <div className="stat-card">
            <h4>Points Earned</h4>
            <div className="stat-value">{data.total_points || 0}</div>
          </div>
        </div>

        <div className="detailed-stats">
          <h4>Activity Breakdown</h4>
          <div className="activity-list">
            {data.recent_activities?.map((activity, index) => (
              <div key={index} className="activity-item">
                <span className="activity-type">{activity.type}</span>
                <span className="activity-date">{activity.date}</span>
                <span className="activity-points">+{activity.points}</span>
              </div>
            )) || <p>No recent activities</p>}
          </div>
        </div>
      </div>
    </div>
  );
};

export default PersonalAnalytics;