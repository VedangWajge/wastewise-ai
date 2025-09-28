import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import apiService from '../../services/api';
import BookingCard from './BookingCard';
import BookingDetails from './BookingDetails';
import './BookingManagement.css';

const BookingManagement = () => {
  const { user, isAuthenticated } = useAuth();
  const [bookings, setBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState('all');
  const [selectedBooking, setSelectedBooking] = useState(null);
  const [showDetails, setShowDetails] = useState(false);

  useEffect(() => {
    if (isAuthenticated) {
      fetchBookings();
    }
  }, [isAuthenticated, filter]);

  const fetchBookings = async () => {
    try {
      setLoading(true);
      setError(null);

      const status = filter === 'all' ? null : filter;
      const response = await apiService.getUserBookings(status);

      if (response.success) {
        setBookings(response.bookings || []);
      }
    } catch (error) {
      console.error('Error fetching bookings:', error);
      setError(error.message || 'Failed to load bookings');
    } finally {
      setLoading(false);
    }
  };

  const handleBookingClick = (booking) => {
    setSelectedBooking(booking);
    setShowDetails(true);
  };

  const handleCancelBooking = async (bookingId, reason) => {
    try {
      const response = await apiService.cancelBooking(bookingId, reason);
      if (response.success) {
        // Refresh bookings list
        fetchBookings();
        // Update selected booking if it's the one being cancelled
        if (selectedBooking && selectedBooking.id === bookingId) {
          setSelectedBooking({ ...selectedBooking, status: 'cancelled' });
        }
      }
    } catch (error) {
      console.error('Error cancelling booking:', error);
      throw error;
    }
  };

  const handleRescheduleBooking = async (bookingId, newDate, newTimeSlot) => {
    try {
      const response = await apiService.rescheduleBooking(bookingId, newDate, newTimeSlot);
      if (response.success) {
        // Refresh bookings list
        fetchBookings();
        // Update selected booking
        if (selectedBooking && selectedBooking.id === bookingId) {
          setSelectedBooking(response.booking);
        }
      }
    } catch (error) {
      console.error('Error rescheduling booking:', error);
      throw error;
    }
  };

  const handleRateBooking = async (bookingId, ratingData) => {
    try {
      const response = await apiService.rateBooking(bookingId, ratingData);
      if (response.success) {
        // Refresh bookings list
        fetchBookings();
        // Update selected booking
        if (selectedBooking && selectedBooking.id === bookingId) {
          setSelectedBooking({ ...selectedBooking, rating: ratingData.rating });
        }
      }
    } catch (error) {
      console.error('Error rating booking:', error);
      throw error;
    }
  };

  const getStatusCounts = () => {
    return {
      all: bookings.length,
      pending: bookings.filter(b => b.status === 'pending').length,
      confirmed: bookings.filter(b => b.status === 'confirmed').length,
      in_progress: bookings.filter(b => b.status === 'in_progress').length,
      completed: bookings.filter(b => b.status === 'completed').length,
      cancelled: bookings.filter(b => b.status === 'cancelled').length,
    };
  };

  const filteredBookings = filter === 'all'
    ? bookings
    : bookings.filter(booking => booking.status === filter);

  if (!isAuthenticated) {
    return (
      <div className="booking-management">
        <div className="auth-required">
          <div className="auth-icon">🔐</div>
          <h3>Login Required</h3>
          <p>Please login to view your bookings</p>
        </div>
      </div>
    );
  }

  if (showDetails && selectedBooking) {
    return (
      <BookingDetails
        booking={selectedBooking}
        onBack={() => setShowDetails(false)}
        onCancel={handleCancelBooking}
        onReschedule={handleRescheduleBooking}
        onRate={handleRateBooking}
      />
    );
  }

  const statusCounts = getStatusCounts();

  return (
    <div className="booking-management">
      <div className="booking-header">
        <div className="header-content">
          <h2>My Bookings</h2>
          <p>Manage your waste collection bookings</p>
        </div>
        <div className="booking-stats">
          <div className="stat-item">
            <span className="stat-number">{statusCounts.all}</span>
            <span className="stat-label">Total</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">{statusCounts.pending}</span>
            <span className="stat-label">Pending</span>
          </div>
          <div className="stat-item">
            <span className="stat-number">{statusCounts.completed}</span>
            <span className="stat-label">Completed</span>
          </div>
        </div>
      </div>

      <div className="booking-filters">
        {[
          { key: 'all', label: 'All Bookings', count: statusCounts.all },
          { key: 'pending', label: 'Pending', count: statusCounts.pending },
          { key: 'confirmed', label: 'Confirmed', count: statusCounts.confirmed },
          { key: 'in_progress', label: 'In Progress', count: statusCounts.in_progress },
          { key: 'completed', label: 'Completed', count: statusCounts.completed },
          { key: 'cancelled', label: 'Cancelled', count: statusCounts.cancelled },
        ].map(({ key, label, count }) => (
          <button
            key={key}
            className={`filter-btn ${filter === key ? 'active' : ''}`}
            onClick={() => setFilter(key)}
          >
            {label}
            {count > 0 && <span className="filter-count">{count}</span>}
          </button>
        ))}
      </div>

      <div className="booking-content">
        {loading ? (
          <div className="loading-state">
            <div className="loading-spinner"></div>
            <p>Loading your bookings...</p>
          </div>
        ) : error ? (
          <div className="error-state">
            <div className="error-icon">❌</div>
            <h3>Error Loading Bookings</h3>
            <p>{error}</p>
            <button className="retry-btn" onClick={fetchBookings}>
              Try Again
            </button>
          </div>
        ) : filteredBookings.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">📋</div>
            <h3>No Bookings Found</h3>
            <p>
              {filter === 'all'
                ? "You haven't made any bookings yet."
                : `No ${filter} bookings found.`}
            </p>
            <button className="cta-btn" onClick={() => window.location.hash = 'classify'}>
              Start by Classifying Waste
            </button>
          </div>
        ) : (
          <div className="bookings-grid">
            {filteredBookings.map(booking => (
              <BookingCard
                key={booking.id}
                booking={booking}
                onClick={() => handleBookingClick(booking)}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default BookingManagement;