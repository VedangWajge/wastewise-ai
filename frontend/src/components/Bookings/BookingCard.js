import React from 'react';
import './BookingCard.css';

const BookingCard = ({ booking, onClick, onPayment }) => {
  const getStatusIcon = (status) => {
    switch (status) {
      case 'pending': return '⏳';
      case 'confirmed': return '✅';
      case 'in_progress': return '🚛';
      case 'completed': return '✨';
      case 'cancelled': return '❌';
      default: return '📋';
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'pending': return '#f59e0b';
      case 'confirmed': return '#10b981';
      case 'in_progress': return '#3b82f6';
      case 'completed': return '#8b5cf6';
      case 'cancelled': return '#ef4444';
      default: return '#6b7280';
    }
  };

  const getWasteTypeIcon = (wasteType) => {
    switch (wasteType.toLowerCase()) {
      case 'plastic': return '🔴';
      case 'paper': return '📄';
      case 'glass': return '🟢';
      case 'metal': return '🔩';
      case 'organic': return '🌿';
      case 'e-waste': return '💻';
      default: return '🗑️';
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      weekday: 'short',
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const formatTime = (timeSlot) => {
    return timeSlot || 'Time TBD';
  };

  const getPaymentStatusIcon = (paymentStatus) => {
    switch (paymentStatus) {
      case 'paid': return '✓';
      case 'pending': return '⏳';
      case 'failed': return '✗';
      case 'refunded': return '↩️';
      default: return '⏳';
    }
  };

  const getPaymentStatusColor = (paymentStatus) => {
    switch (paymentStatus) {
      case 'paid': return '#10b981';
      case 'pending': return '#f59e0b';
      case 'failed': return '#ef4444';
      case 'refunded': return '#6b7280';
      default: return '#f59e0b';
    }
  };

  const handlePaymentClick = (e) => {
    e.stopPropagation();
    if (onPayment) {
      onPayment(booking);
    }
  };

  return (
    <div className="booking-card" onClick={onClick}>
      <div className="booking-header">
        <div className="booking-id">
          <span className="id-label">#{booking.id.slice(-8)}</span>
          <span
            className="status-badge"
            style={{ backgroundColor: getStatusColor(booking.status) }}
          >
            {getStatusIcon(booking.status)} {booking.status.replace('_', ' ')}
          </span>
        </div>
        <div className="booking-date">
          <span className="date-text">{formatDate(booking.scheduled_date)}</span>
          <span className="time-text">{formatTime(booking.scheduled_time_slot)}</span>
        </div>
      </div>

      <div className="booking-details">
        <div className="waste-info">
          <div className="waste-type">
            <span className="waste-icon">{getWasteTypeIcon(booking.waste_type)}</span>
            <span className="waste-text">
              {booking.waste_type} - {booking.quantity}
            </span>
          </div>
        </div>

        <div className="service-info">
          <div className="service-provider">
            <span className="provider-icon">🏢</span>
            <span className="provider-name">{booking.service_provider?.name || 'Provider TBD'}</span>
          </div>
          {booking.service_provider?.rating && (
            <div className="provider-rating">
              <span>⭐ {booking.service_provider.rating}/5</span>
            </div>
          )}
        </div>

        <div className="location-info">
          <span className="location-icon">📍</span>
          <span className="location-text">
            {booking.pickup_address.length > 50
              ? `${booking.pickup_address.substring(0, 50)}...`
              : booking.pickup_address}
          </span>
        </div>
      </div>

      <div className="booking-footer">
        <div className="booking-meta">
          <span className="created-date">
            Created: {new Date(booking.created_at).toLocaleDateString()}
          </span>
          {booking.estimated_cost && (
            <span className="booking-amount">
              ₹{booking.estimated_cost}
            </span>
          )}
        </div>

        {/* Payment Status */}
        {booking.payment_status && (
          <div className="payment-status-container">
            <span
              className="payment-status-badge"
              style={{ backgroundColor: getPaymentStatusColor(booking.payment_status) }}
            >
              {getPaymentStatusIcon(booking.payment_status)} Payment: {booking.payment_status}
            </span>
          </div>
        )}

        <div className="quick-actions">
          {/* Pay Now Button */}
          {booking.payment_status === 'pending' && booking.status !== 'cancelled' && (
            <button
              className="pay-now-btn"
              onClick={handlePaymentClick}
            >
              💳 Pay Now
            </button>
          )}

          {/* Other Action Hints */}
          {booking.payment_status === 'paid' && booking.status === 'pending' && (
            <span className="action-hint">✓ Paid - Click to manage</span>
          )}
          {booking.status === 'confirmed' && (
            <span className="action-hint">Track progress</span>
          )}
          {booking.status === 'completed' && !booking.rating && (
            <span className="action-hint">Rate service</span>
          )}
          {booking.status === 'completed' && booking.rating && (
            <span className="rating-display">★ {booking.rating}/5</span>
          )}
        </div>
      </div>

      <div className="card-hover-effect"></div>
    </div>
  );
};

export default BookingCard;