import React from 'react';

const BookingDetails = ({ booking, onClose, onUpdate }) => {
  if (!booking) {
    return null;
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'confirmed':
        return '#4CAF50';
      case 'pending':
        return '#FF9800';
      case 'completed':
        return '#2196F3';
      case 'cancelled':
        return '#f44336';
      default:
        return '#757575';
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="booking-details-modal">
      <div className="modal-overlay" onClick={onClose}></div>
      <div className="modal-content">
        <div className="modal-header">
          <h2>Booking Details</h2>
          <button className="close-btn" onClick={onClose}>×</button>
        </div>

        <div className="booking-info">
          <div className="booking-header">
            <div className="booking-id">
              <strong>Booking #{booking.id}</strong>
            </div>
            <div
              className="booking-status"
              style={{ backgroundColor: getStatusColor(booking.status) }}
            >
              {booking.status?.toUpperCase()}
            </div>
          </div>

          <div className="booking-details-grid">
            <div className="detail-item">
              <span className="detail-label">Service Type:</span>
              <span className="detail-value">{booking.service_type || 'N/A'}</span>
            </div>

            <div className="detail-item">
              <span className="detail-label">Scheduled Date:</span>
              <span className="detail-value">
                {booking.scheduled_date ? formatDate(booking.scheduled_date) : 'N/A'}
              </span>
            </div>

            <div className="detail-item">
              <span className="detail-label">Location:</span>
              <span className="detail-value">{booking.location || 'N/A'}</span>
            </div>

            <div className="detail-item">
              <span className="detail-label">Waste Type:</span>
              <span className="detail-value">{booking.waste_type || 'N/A'}</span>
            </div>

            <div className="detail-item">
              <span className="detail-label">Estimated Weight:</span>
              <span className="detail-value">{booking.estimated_weight || 0} kg</span>
            </div>

            <div className="detail-item">
              <span className="detail-label">Cost:</span>
              <span className="detail-value">₹{booking.cost || 0}</span>
            </div>

            <div className="detail-item">
              <span className="detail-label">Created:</span>
              <span className="detail-value">
                {booking.created_at ? formatDate(booking.created_at) : 'N/A'}
              </span>
            </div>

            {booking.completed_at && (
              <div className="detail-item">
                <span className="detail-label">Completed:</span>
                <span className="detail-value">{formatDate(booking.completed_at)}</span>
              </div>
            )}
          </div>

          {booking.notes && (
            <div className="booking-notes">
              <h4>Additional Notes:</h4>
              <p>{booking.notes}</p>
            </div>
          )}

          {booking.driver_info && (
            <div className="driver-info">
              <h4>Driver Information:</h4>
              <div className="driver-details">
                <p><strong>Name:</strong> {booking.driver_info.name}</p>
                <p><strong>Phone:</strong> {booking.driver_info.phone}</p>
                <p><strong>Vehicle:</strong> {booking.driver_info.vehicle}</p>
              </div>
            </div>
          )}
        </div>

        <div className="modal-actions">
          {booking.status === 'pending' && (
            <button
              className="btn-cancel"
              onClick={() => onUpdate(booking.id, 'cancelled')}
            >
              Cancel Booking
            </button>
          )}

          {booking.status === 'confirmed' && (
            <button
              className="btn-reschedule"
              onClick={() => onUpdate(booking.id, 'reschedule')}
            >
              Reschedule
            </button>
          )}

          <button className="btn-close" onClick={onClose}>
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default BookingDetails;