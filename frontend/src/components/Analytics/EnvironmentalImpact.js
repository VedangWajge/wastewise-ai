import React from 'react';

const EnvironmentalImpact = ({ data, period }) => {
  if (!data) {
    return (
      <div className="environmental-impact">
        <p>No environmental impact data available</p>
      </div>
    );
  }

  return (
    <div className="environmental-impact">
      <div className="impact-section">
        <h3>Environmental Impact - {period}</h3>

        <div className="impact-stats">
          <div className="impact-card carbon">
            <div className="impact-icon">🌱</div>
            <div className="impact-content">
              <h4>Carbon Footprint Reduced</h4>
              <div className="impact-value">{data.carbon_saved || 0} kg CO₂</div>
              <p>Equivalent to planting {Math.round((data.carbon_saved || 0) / 22)} trees</p>
            </div>
          </div>

          <div className="impact-card water">
            <div className="impact-icon">💧</div>
            <div className="impact-content">
              <h4>Water Saved</h4>
              <div className="impact-value">{data.water_saved || 0} L</div>
              <p>Enough for {Math.round((data.water_saved || 0) / 150)} showers</p>
            </div>
          </div>

          <div className="impact-card energy">
            <div className="impact-icon">⚡</div>
            <div className="impact-content">
              <h4>Energy Conserved</h4>
              <div className="impact-value">{data.energy_saved || 0} kWh</div>
              <p>Powers a home for {Math.round((data.energy_saved || 0) / 30)} days</p>
            </div>
          </div>

          <div className="impact-card landfill">
            <div className="impact-icon">🏔️</div>
            <div className="impact-content">
              <h4>Landfill Waste Diverted</h4>
              <div className="impact-value">{data.landfill_diverted || 0} kg</div>
              <p>Keeping waste out of landfills</p>
            </div>
          </div>
        </div>

        <div className="impact-comparison">
          <h4>Compared to Average User</h4>
          <div className="comparison-bars">
            <div className="comparison-item">
              <span>Carbon Reduction</span>
              <div className="comparison-bar">
                <div
                  className="comparison-fill positive"
                  style={{ width: `${Math.min(100, (data.carbon_saved || 0) / 10)}%` }}
                ></div>
              </div>
              <span>{((data.carbon_saved || 0) / 10 * 100).toFixed(0)}% above average</span>
            </div>
            <div className="comparison-item">
              <span>Recycling Rate</span>
              <div className="comparison-bar">
                <div
                  className="comparison-fill positive"
                  style={{ width: `${Math.min(100, (data.recycling_rate || 0))}%` }}
                ></div>
              </div>
              <span>{(data.recycling_rate || 0)}% recycling rate</span>
            </div>
          </div>
        </div>

        <div className="environmental-tips">
          <h4>🌍 Ways to Improve Your Impact</h4>
          <div className="tips-list">
            <div className="tip-item">
              <span className="tip-icon">♻️</span>
              <div className="tip-content">
                <h5>Increase Recycling</h5>
                <p>Try to recycle more materials to reduce landfill waste</p>
              </div>
            </div>
            <div className="tip-item">
              <span className="tip-icon">🗑️</span>
              <div className="tip-content">
                <h5>Reduce Waste Generation</h5>
                <p>Consider reducing single-use items and packaging</p>
              </div>
            </div>
            <div className="tip-item">
              <span className="tip-icon">🔄</span>
              <div className="tip-content">
                <h5>Reuse Items</h5>
                <p>Find creative ways to reuse items before disposing</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EnvironmentalImpact;