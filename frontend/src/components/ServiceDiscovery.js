import React, { useState, useEffect } from 'react';
import apiService from '../services/api';
import './ServiceDiscovery.css';

const ServiceDiscovery = ({ wasteType, onServiceSelect, onBack }) => {
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedService, setSelectedService] = useState(null);

  useEffect(() => {
    if (wasteType) {
      fetchNearbyServices();
    } else {
      setLoading(false);
      setError('No waste type specified. Please go back and classify your waste first.');
    }
  }, [wasteType]);

  const fetchNearbyServices = async () => {
    try {
      setLoading(true);
      const response = await apiService.findNearbyServices(wasteType);
      setServices(response.services || []);
      setError(null);
    } catch (err) {
      setError('Failed to load services. Please try again.');
      console.error('Error fetching services:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleServiceSelect = (service) => {
    setSelectedService(service);
    if (onServiceSelect) {
      onServiceSelect(service);
    }
  };

  const getServiceIcon = (type) => {
    const icons = {
      'NGO': '🤝',
      'E-Waste': '💻',
      'Composting': '🌱',
      'Recycling': '♻️',
      'Fertilizer': '🌾'
    };
    return icons[type] || '🏢';
  };

  const getServiceColor = (type) => {
    const colors = {
      'NGO': '#ff9800',
      'E-Waste': '#2196f3',
      'Composting': '#4caf50',
      'Recycling': '#00bcd4',
      'Fertilizer': '#8bc34a'
    };
    return colors[type] || '#757575';
  };

  if (loading) {
    return (
      <div className="service-discovery">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Finding services for {wasteType || 'unknown'} waste...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="service-discovery">
        <div className="error-container">
          <p>{error}</p>
          <div className="action-buttons">
            <button className="btn btn-primary" onClick={fetchNearbyServices}>
              Try Again
            </button>
            <button className="btn btn-secondary" onClick={onBack}>
              Go Back
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="service-discovery">
      <div className="header">
        <button className="back-btn" onClick={onBack}>
          ← Back
        </button>
        <h2>Services for {wasteType ? wasteType.toUpperCase() : 'UNKNOWN'} Waste</h2>
        <p>{services.length} services found near you</p>
      </div>

      <div className="services-grid">
        {services.map((service) => (
          <div
            key={service.id}
            className={`service-card ${selectedService?.id === service.id ? 'selected' : ''}`}
            onClick={() => handleServiceSelect(service)}
          >
            <div className="service-header">
              <div
                className="service-icon"
                style={{ color: getServiceColor(service.type) }}
              >
                {getServiceIcon(service.type)}
              </div>
              <div className="service-basic-info">
                <h3>{service.name}</h3>
                <span className="service-type">{service.type}</span>
              </div>
              {service.verified && (
                <div className="verified-badge">
                  ✅ Verified
                </div>
              )}
            </div>

            <div className="service-details">
              <div className="detail-row">
                <span className="detail-label">📍 Distance:</span>
                <span className="detail-value">{service.distance}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">🕒 Time:</span>
                <span className="detail-value">{service.estimated_time}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">⭐ Rating:</span>
                <span className="detail-value">{service.rating}/5</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">📦 Capacity:</span>
                <span className="detail-value">{service.capacity}</span>
              </div>
            </div>

            <div className="service-description">
              <p>{service.description}</p>
            </div>

            <div className="service-specialities">
              <h4>Specializes in:</h4>
              <div className="speciality-tags">
                {service.speciality.map((spec, index) => (
                  <span key={index} className="speciality-tag">
                    {spec}
                  </span>
                ))}
              </div>
            </div>

            <div className="contact-info">
              <div className="contact-item">
                <span className="contact-label">📞</span>
                <span className="contact-value">{service.contact.phone}</span>
              </div>
              <div className="contact-item">
                <span className="contact-label">✉️</span>
                <span className="contact-value">{service.contact.email}</span>
              </div>
            </div>

            <div className="operating-hours">
              <span className="hours-label">🕒 Hours:</span>
              <span className="hours-value">{service.operating_hours}</span>
            </div>

            {service.available_slots && (
              <div className="available-slots">
                <h4>Available Slots:</h4>
                <div className="slots-list">
                  {service.available_slots.map((slot, index) => (
                    <span key={index} className="slot-tag">
                      {slot}
                    </span>
                  ))}
                </div>
              </div>
            )}

            <div className="service-actions">
              <button
                className={`btn ${selectedService?.id === service.id ? 'btn-success' : 'btn-primary'}`}
                onClick={(e) => {
                  e.stopPropagation();
                  handleServiceSelect(service);
                }}
              >
                {selectedService?.id === service.id ? '✅ Selected' : '📅 Book Service'}
              </button>
              <button
                className="btn btn-outline"
                onClick={(e) => {
                  e.stopPropagation();
                  window.open(`tel:${service.contact.phone}`);
                }}
              >
                📞 Call
              </button>
            </div>
          </div>
        ))}
      </div>

      {services.length === 0 && (
        <div className="no-services">
          <div className="no-services-icon">😔</div>
          <h3>No Services Available</h3>
          <p>Sorry, no services are currently available for {wasteType || 'this type of'} waste in your area.</p>
          <button className="btn btn-primary" onClick={onBack}>
            Try Different Waste Type
          </button>
        </div>
      )}

      {selectedService && (
        <div className="selected-service-footer">
          <div className="selected-info">
            <span>Selected: {selectedService.name}</span>
          </div>
          <button
            className="btn btn-success btn-large"
            onClick={() => onServiceSelect && onServiceSelect(selectedService)}
          >
            Continue to Booking →
          </button>
        </div>
      )}
    </div>
  );
};

export default ServiceDiscovery;