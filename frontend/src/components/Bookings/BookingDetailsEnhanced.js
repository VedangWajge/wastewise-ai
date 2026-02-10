import React, { useState } from 'react';
import './BookingDetailsEnhanced.css';

const BookingDetailsEnhanced = ({ booking, onBack, onCancel, onReschedule, onRate, onPayment }) => {
  const [showCancelDialog, setShowCancelDialog] = useState(false);
  const [showRescheduleDialog, setShowRescheduleDialog] = useState(false);
  const [showRatingDialog, setShowRatingDialog] = useState(false);
  const [cancelReason, setCancelReason] = useState('');
  const [ratingData, setRatingData] = useState({ rating: 5, review: '' });
  const [rescheduleData, setRescheduleData] = useState({ date: '', time_slot: '' });
  const [loading, setLoading] = useState(false);

  if (!booking) {
    return null;
  }

  const getStatusColor = (status) => {
    switch (status) {
      case 'confirmed': return '#4CAF50';
      case 'pending': return '#FF9800';
      case 'in_progress': return '#2196F3';
      case 'completed': return '#8b5cf6';
      case 'cancelled': return '#f44336';
      default: return '#757575';
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

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  const formatDateTime = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const handleCancelBooking = async () => {
    if (!cancelReason.trim()) {
      alert('Please provide a cancellation reason');
      return;
    }

    setLoading(true);
    try {
      await onCancel(booking.id, cancelReason);
      setShowCancelDialog(false);
      alert('Booking cancelled successfully');
    } catch (error) {
      alert(error.message || 'Failed to cancel booking');
    } finally {
      setLoading(false);
    }
  };

  const handleReschedule = async () => {
    if (!rescheduleData.date || !rescheduleData.time_slot) {
      alert('Please select both date and time slot');
      return;
    }

    setLoading(true);
    try {
      await onReschedule(booking.id, rescheduleData.date, rescheduleData.time_slot);
      setShowRescheduleDialog(false);
      alert('Booking rescheduled successfully');
    } catch (error) {
      alert(error.message || 'Failed to reschedule booking');
    } finally {
      setLoading(false);
    }
  };

  const handleRating = async () => {
    if (!ratingData.rating) {
      alert('Please select a rating');
      return;
    }

    setLoading(true);
    try {
      await onRate(booking.id, ratingData);
      setShowRatingDialog(false);
      alert('Thank you for your feedback!');
    } catch (error) {
      alert(error.message || 'Failed to submit rating');
    } finally {
      setLoading(false);
    }
  };

  const handlePaymentClick = () => {
    if (onPayment) {
      onPayment(booking);
    }
  };

  const getMinRescheduleDate = () => {
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    return tomorrow.toISOString().split('T')[0];
  };

  return (
    <div className="booking-details-container">
      <div className="booking-details-header">
        <button className="back-button" onClick={onBack}>
          ← Back to Bookings
        </button>
        <h2>Booking Details</h2>
      </div>

      <div className="booking-details-content">
        {/* Status and Payment Overview */}
        <div className="details-overview">
          <div className="overview-card">
            <div className="overview-label">Booking ID</div>
            <div className="overview-value">#{booking.id.slice(-8)}</div>
          </div>
          <div className="overview-card">
            <div className="overview-label">Status</div>
            <div className="overview-value">
              <span
                className="status-pill"
                style={{ backgroundColor: getStatusColor(booking.status) }}
              >
                {booking.status.replace('_', ' ').toUpperCase()}
              </span>
            </div>
          </div>
          <div className="overview-card">
            <div className="overview-label">Payment Status</div>
            <div className="overview-value">
              <span
                className="status-pill"
                style={{ backgroundColor: getPaymentStatusColor(booking.payment_status || 'pending') }}
              >
                {(booking.payment_status || 'pending').toUpperCase()}
              </span>
            </div>
          </div>
          <div className="overview-card">
            <div className="overview-label">Amount</div>
            <div className="overview-value amount">₹{booking.estimated_cost || 0}</div>
          </div>
        </div>

        {/* Payment Action Button */}
        {booking.payment_status === 'pending' && booking.status !== 'cancelled' && (
          <div className="payment-action-section">
            <div className="payment-alert">
              <span className="alert-icon">⚠️</span>
              <span>Payment is pending for this booking</span>
            </div>
            <button className="pay-now-button-large" onClick={handlePaymentClick}>
              💳 Pay ₹{booking.estimated_cost || 0} Now
            </button>
          </div>
        )}

        {/* Waste Details */}
        <div className="details-section">
          <h3>📦 Waste Details</h3>
          <div className="details-grid">
            <div className="detail-row">
              <span className="detail-label">Waste Type:</span>
              <span className="detail-value">{booking.waste_type || 'N/A'}</span>
            </div>
            <div className="detail-row">
              <span className="detail-label">Quantity:</span>
              <span className="detail-value">{booking.quantity || 'N/A'}</span>
            </div>
            {booking.special_instructions && (
              <div className="detail-row full-width">
                <span className="detail-label">Special Instructions:</span>
                <span className="detail-value">{booking.special_instructions}</span>
              </div>
            )}
          </div>
        </div>

        {/* Schedule Details */}
        <div className="details-section">
          <h3>📅 Schedule Details</h3>
          <div className="details-grid">
            <div className="detail-row">
              <span className="detail-label">Scheduled Date:</span>
              <span className="detail-value">{formatDate(booking.scheduled_date)}</span>
            </div>
            <div className="detail-row">
              <span className="detail-label">Time Slot:</span>
              <span className="detail-value">{booking.scheduled_time_slot || 'N/A'}</span>
            </div>
          </div>
        </div>

        {/* Pickup Details */}
        <div className="details-section">
          <h3>📍 Pickup Details</h3>
          <div className="details-grid">
            <div className="detail-row full-width">
              <span className="detail-label">Address:</span>
              <span className="detail-value">{booking.pickup_address || 'N/A'}</span>
            </div>
            <div className="detail-row">
              <span className="detail-label">Contact Person:</span>
              <span className="detail-value">{booking.contact_person || 'N/A'}</span>
            </div>
            <div className="detail-row">
              <span className="detail-label">Contact Phone:</span>
              <span className="detail-value">{booking.contact_phone || 'N/A'}</span>
            </div>
          </div>
        </div>

        {/* Service Provider Details */}
        {booking.service_provider && (
          <div className="details-section">
            <h3>🏢 Service Provider</h3>
            <div className="details-grid">
              <div className="detail-row">
                <span className="detail-label">Name:</span>
                <span className="detail-value">{booking.service_provider.name}</span>
              </div>
              {booking.service_provider.phone && (
                <div className="detail-row">
                  <span className="detail-label">Phone:</span>
                  <span className="detail-value">{booking.service_provider.phone}</span>
                </div>
              )}
              {booking.service_provider.rating && (
                <div className="detail-row">
                  <span className="detail-label">Rating:</span>
                  <span className="detail-value">⭐ {booking.service_provider.rating}/5</span>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Booking Timeline */}
        <div className="details-section">
          <h3>🕐 Timeline</h3>
          <div className="timeline">
            <div className="timeline-item">
              <div className="timeline-icon">✓</div>
              <div className="timeline-content">
                <div className="timeline-title">Booking Created</div>
                <div className="timeline-date">{formatDateTime(booking.created_at)}</div>
              </div>
            </div>
            {booking.payment_date && (
              <div className="timeline-item">
                <div className="timeline-icon">💳</div>
                <div className="timeline-content">
                  <div className="timeline-title">Payment Completed</div>
                  <div className="timeline-date">{formatDateTime(booking.payment_date)}</div>
                </div>
              </div>
            )}
            {booking.completed_at && (
              <div className="timeline-item">
                <div className="timeline-icon">✨</div>
                <div className="timeline-content">
                  <div className="timeline-title">Service Completed</div>
                  <div className="timeline-date">{formatDateTime(booking.completed_at)}</div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="details-actions">
          {booking.status === 'pending' && booking.payment_status !== 'paid' && (
            <>
              <button
                className="action-button secondary"
                onClick={() => setShowRescheduleDialog(true)}
              >
                📅 Reschedule
              </button>
              <button
                className="action-button danger"
                onClick={() => setShowCancelDialog(true)}
              >
                ❌ Cancel Booking
              </button>
            </>
          )}

          {booking.status === 'completed' && !booking.rating && (
            <button
              className="action-button primary"
              onClick={() => setShowRatingDialog(true)}
            >
              ⭐ Rate Service
            </button>
          )}
        </div>
      </div>

      {/* Cancel Dialog */}
      {showCancelDialog && (
        <div className="modal-overlay" onClick={() => setShowCancelDialog(false)}>
          <div className="modal-dialog" onClick={(e) => e.stopPropagation()}>
            <h3>Cancel Booking</h3>
            <p>Please provide a reason for cancellation:</p>
            <textarea
              value={cancelReason}
              onChange={(e) => setCancelReason(e.target.value)}
              placeholder="e.g., Change of plans, Found another service, etc."
              rows="4"
            />
            <div className="modal-actions">
              <button
                className="action-button secondary"
                onClick={() => setShowCancelDialog(false)}
              >
                Back
              </button>
              <button
                className="action-button danger"
                onClick={handleCancelBooking}
                disabled={loading}
              >
                {loading ? 'Cancelling...' : 'Confirm Cancellation'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Reschedule Dialog */}
      {showRescheduleDialog && (
        <div className="modal-overlay" onClick={() => setShowRescheduleDialog(false)}>
          <div className="modal-dialog" onClick={(e) => e.stopPropagation()}>
            <h3>Reschedule Booking</h3>
            <div className="form-group">
              <label>New Date:</label>
              <input
                type="date"
                value={rescheduleData.date}
                onChange={(e) => setRescheduleData({ ...rescheduleData, date: e.target.value })}
                min={getMinRescheduleDate()}
              />
            </div>
            <div className="form-group">
              <label>New Time Slot:</label>
              <select
                value={rescheduleData.time_slot}
                onChange={(e) => setRescheduleData({ ...rescheduleData, time_slot: e.target.value })}
              >
                <option value="">Select time slot</option>
                <option value="9:00 AM - 11:00 AM">9:00 AM - 11:00 AM</option>
                <option value="11:00 AM - 1:00 PM">11:00 AM - 1:00 PM</option>
                <option value="1:00 PM - 3:00 PM">1:00 PM - 3:00 PM</option>
                <option value="3:00 PM - 5:00 PM">3:00 PM - 5:00 PM</option>
                <option value="5:00 PM - 7:00 PM">5:00 PM - 7:00 PM</option>
              </select>
            </div>
            <div className="modal-actions">
              <button
                className="action-button secondary"
                onClick={() => setShowRescheduleDialog(false)}
              >
                Back
              </button>
              <button
                className="action-button primary"
                onClick={handleReschedule}
                disabled={loading}
              >
                {loading ? 'Rescheduling...' : 'Confirm Reschedule'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Rating Dialog */}
      {showRatingDialog && (
        <div className="modal-overlay" onClick={() => setShowRatingDialog(false)}>
          <div className="modal-dialog" onClick={(e) => e.stopPropagation()}>
            <h3>Rate Service</h3>
            <div className="form-group">
              <label>Your Rating:</label>
              <div className="rating-input">
                {[1, 2, 3, 4, 5].map((star) => (
                  <span
                    key={star}
                    className={`star-input ${star <= ratingData.rating ? 'filled' : ''}`}
                    onClick={() => setRatingData({ ...ratingData, rating: star })}
                  >
                    ★
                  </span>
                ))}
              </div>
            </div>
            <div className="form-group">
              <label>Review (optional):</label>
              <textarea
                value={ratingData.review}
                onChange={(e) => setRatingData({ ...ratingData, review: e.target.value })}
                placeholder="Share your experience..."
                rows="4"
              />
            </div>
            <div className="modal-actions">
              <button
                className="action-button secondary"
                onClick={() => setShowRatingDialog(false)}
              >
                Back
              </button>
              <button
                className="action-button primary"
                onClick={handleRating}
                disabled={loading}
              >
                {loading ? 'Submitting...' : 'Submit Rating'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default BookingDetailsEnhanced;
