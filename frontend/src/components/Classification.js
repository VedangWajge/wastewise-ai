import React from 'react';
import './Classification.css';

const Classification = ({ result, isLoading, imagePreview, onNewClassification }) => {
  if (isLoading) {
    return (
      <div className="classification-container">
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Analyzing waste image...</p>
          <p className="loading-subtext">Using AI to identify waste type</p>
        </div>
      </div>
    );
  }

  if (!result) {
    return null;
  }

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

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return '#4caf50';
    if (confidence >= 0.6) return '#ff9800';
    return '#f44336';
  };

  return (
    <div className="classification-container">
      <div className="classification-header">
        <h2>Classification Result</h2>
        <button
          className="btn btn-primary"
          onClick={onNewClassification}
        >
          📸 Classify Another
        </button>
      </div>

      {imagePreview && (
        <div className="image-preview">
          <img src={imagePreview} alt="Analyzed waste" />
        </div>
      )}

      <div className="result-card">
        <div className="waste-type-section">
          <div className="waste-icon">
            {getWasteIcon(result.classification.waste_type)}
          </div>
          <div className="waste-info">
            <h3>{result.classification.waste_type.toUpperCase()}</h3>
            <div className="confidence-bar">
              <div
                className="confidence-fill"
                style={{
                  width: `${result.classification.confidence * 100}%`,
                  backgroundColor: getConfidenceColor(result.classification.confidence)
                }}
              ></div>
            </div>
            <p className="confidence-text">
              Confidence: {(result.classification.confidence * 100).toFixed(1)}%
            </p>
          </div>
        </div>

        <div className="recommendations-section">
          <h4>🎯 Disposal Recommendations</h4>
          <ul>
            {result.classification.recommendations.map((recommendation, index) => (
              <li key={index}>{recommendation}</li>
            ))}
          </ul>
        </div>

        <div className="environmental-section">
          <h4>🌍 Environmental Impact</h4>
          <p>{result.classification.environmental_impact}</p>
        </div>

        {result.classification.all_predictions && (
          <div className="predictions-section">
            <h4>📊 All Predictions</h4>
            <div className="prediction-bars">
              {Object.entries(result.classification.all_predictions)
                .sort(([,a], [,b]) => b - a)
                .map(([type, confidence]) => (
                  <div key={type} className="prediction-bar">
                    <span className="prediction-label">
                      {getWasteIcon(type)} {type}
                    </span>
                    <div className="prediction-bar-container">
                      <div
                        className="prediction-bar-fill"
                        style={{ width: `${confidence * 100}%` }}
                      ></div>
                    </div>
                    <span className="prediction-value">
                      {(confidence * 100).toFixed(1)}%
                    </span>
                  </div>
                ))}
            </div>
          </div>
        )}
      </div>

      <div className="classification-footer">
        <p className="timestamp">
          Classified at: {new Date(result.timestamp).toLocaleString()}
        </p>
      </div>
    </div>
  );
};

export default Classification;