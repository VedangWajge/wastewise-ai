import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import apiService from '../services/api';
import './BookingForm.css';

const BookingForm = ({ service, wasteType, onBookingComplete, onBack }) => {
  const { user, isAuthenticated } = useAuth();
  const [formData, setFormData] = useState({
    quantity: '',
    pickup_address: user?.address || '',
    scheduled_date: '',
    scheduled_time_slot: '',
    special_instructions: '',
    contact_phone: user?.phone || '',
    contact_person: user?.full_name || ''
  });
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});
  const [authWarning, setAuthWarning] = useState(!isAuthenticated);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));

    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.quantity || formData.quantity <= 0) {
      newErrors.quantity = 'Please enter a valid quantity';
    }
    if (!formData.pickup_address.trim()) {
      newErrors.pickup_address = 'Pickup address is required';
    }
    if (!formData.scheduled_date) {
      newErrors.scheduled_date = 'Please select a date';
    }
    if (!formData.scheduled_time_slot) {
      newErrors.scheduled_time_slot = 'Please select a time slot';
    }
    if (!formData.contact_person.trim()) {
      newErrors.contact_person = 'Contact name is required';
    }
    if (!formData.contact_phone.trim()) {
      newErrors.contact_phone = 'Contact phone is required';
    }

    // Check if date is in the future
    const selectedDate = new Date(formData.scheduled_date);
    const now = new Date();
    selectedDate.setHours(0, 0, 0, 0);
    now.setHours(0, 0, 0, 0);
    if (selectedDate <= now) {
      newErrors.scheduled_date = 'Please select a future date';
    }

    // Check authentication
    if (!isAuthenticated) {
      newErrors.auth = 'Please login to create a booking';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setLoading(true);

    try {
      const bookingData = {
        service_provider_id: service.id,
        waste_type: wasteType,
        quantity: `${formData.quantity} kg`,
        pickup_address: formData.pickup_address,
        scheduled_date: `${formData.scheduled_date}T10:00:00Z`,
        scheduled_time_slot: formData.scheduled_time_slot,
        special_instructions: formData.special_instructions,
        contact_person: formData.contact_person,
        contact_phone: formData.contact_phone
      };

      const result = await apiService.createBooking(bookingData);

      if (result.success) {
        onBookingComplete && onBookingComplete(result.booking);
      }
    } catch (error) {
      console.error('Booking error:', error);
      setErrors({ general: error.message || 'Failed to create booking. Please try again.' });
    } finally {
      setLoading(false);
    }
  };

  const getMinDate = () => {
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    return tomorrow.toISOString().split('T')[0];
  };

  const getMinTime = () => {
    const selectedDate = new Date(formData.scheduled_date);
    const today = new Date();

    if (selectedDate.toDateString() === today.toDateString()) {
      const now = new Date();
      now.setHours(now.getHours() + 2); // Minimum 2 hours from now
      return now.toTimeString().slice(0, 5);
    }

    return '09:00'; // Default minimum time
  };

  if (!isAuthenticated) {
    return (
      <div className="booking-form-container">
        <div className="form-header">
          <button className="back-btn" onClick={onBack}>
            ← Back to Services
          </button>
          <h2>Book Waste Collection Service</h2>
        </div>

        <div className="auth-warning">
          <div className="auth-warning-icon">🔐</div>
          <h3>Login Required</h3>
          <p>You need to login to your account to book waste collection services.</p>
          <div className="auth-warning-actions">
            <button className="btn btn-primary" onClick={() => window.location.hash = 'login'}>
              Login Now
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
    <div className="booking-form-container">
      <div className="form-header">
        <button className="back-btn" onClick={onBack}>
          ← Back to Services
        </button>
        <h2>Book Waste Collection Service</h2>
      </div>

      <div className="service-summary">
        <div className="service-info">
          <div className="service-icon">
            {service.type === 'NGO' ? '🤝' :
             service.type === 'E-Waste' ? '💻' :
             service.type === 'Composting' ? '🌱' :
             service.type === 'Recycling' ? '♻️' : '🏢'}
          </div>
          <div className="service-details">
            <h3>{service.name}</h3>
            <p>{service.type} • ⭐ {service.rating}/5</p>
            <p>📍 {service.distance} • 🕒 {service.estimated_time}</p>
          </div>
        </div>
        <div className="waste-type-badge">
          {wasteType.toUpperCase()} Waste
        </div>
      </div>

      <form onSubmit={handleSubmit} className="booking-form">
        {errors.general && (
          <div className="error-alert">
            {errors.general}
          </div>
        )}

        <div className="form-section">
          <h3>📦 Waste Details</h3>

          <div className="form-group">
            <label htmlFor="quantity">
              Quantity (kg) <span className="required">*</span>
            </label>
            <input
              type="number"
              id="quantity"
              name="quantity"
              value={formData.quantity}
              onChange={handleInputChange}
              placeholder="Enter quantity in kg"
              min="1"
              max="1000"
              className={errors.quantity ? 'error' : ''}
            />
            {errors.quantity && <span className="error-text">{errors.quantity}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="special_instructions">
              Special Instructions
            </label>
            <textarea
              id="special_instructions"
              name="special_instructions"
              value={formData.special_instructions}
              onChange={handleInputChange}
              placeholder="Any special handling requirements or notes..."
              rows="3"
            />
          </div>
        </div>

        <div className="form-section">
          <h3>📍 Pickup Details</h3>

          <div className="form-group">
            <label htmlFor="pickup_address">
              Pickup Address <span className="required">*</span>
            </label>
            <textarea
              id="pickup_address"
              name="pickup_address"
              value={formData.pickup_address}
              onChange={handleInputChange}
              placeholder="Enter complete pickup address including building/apartment details"
              rows="3"
              className={errors.pickup_address ? 'error' : ''}
            />
            {errors.pickup_address && <span className="error-text">{errors.pickup_address}</span>}
          </div>
        </div>

        <div className="form-section">
          <h3>📅 Schedule</h3>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="scheduled_date">
                Preferred Date <span className="required">*</span>
              </label>
              <input
                type="date"
                id="scheduled_date"
                name="scheduled_date"
                value={formData.scheduled_date}
                onChange={handleInputChange}
                min={getMinDate()}
                className={errors.scheduled_date ? 'error' : ''}
              />
              {errors.scheduled_date && <span className="error-text">{errors.scheduled_date}</span>}
            </div>

            <div className="form-group">
              <label htmlFor="scheduled_time_slot">
                Preferred Time Slot <span className="required">*</span>
              </label>
              <select
                id="scheduled_time_slot"
                name="scheduled_time_slot"
                value={formData.scheduled_time_slot}
                onChange={handleInputChange}
                className={errors.scheduled_time_slot ? 'error' : ''}
              >
                <option value="">Select a time slot</option>
                <option value="9:00 AM - 11:00 AM">9:00 AM - 11:00 AM</option>
                <option value="11:00 AM - 1:00 PM">11:00 AM - 1:00 PM</option>
                <option value="1:00 PM - 3:00 PM">1:00 PM - 3:00 PM</option>
                <option value="3:00 PM - 5:00 PM">3:00 PM - 5:00 PM</option>
                <option value="5:00 PM - 7:00 PM">5:00 PM - 7:00 PM</option>
              </select>
              {errors.scheduled_time_slot && <span className="error-text">{errors.scheduled_time_slot}</span>}
            </div>
          </div>

          <div className="available-slots">
            <h4>✨ Recommended Slots:</h4>
            <div className="slots-list">
              {service.available_slots?.map((slot, index) => (
                <button
                  key={index}
                  type="button"
                  className="slot-btn"
                  onClick={() => {
                    const [dateStr, timeRange] = slot.split(' ', 2);
                    const [startTime] = timeRange.split(' - ');

                    let date = '';
                    if (dateStr === 'Today') {
                      date = new Date().toISOString().split('T')[0];
                    } else if (dateStr === 'Tomorrow') {
                      const tomorrow = new Date();
                      tomorrow.setDate(tomorrow.getDate() + 1);
                      date = tomorrow.toISOString().split('T')[0];
                    }

                    if (date) {
                      setFormData(prev => ({
                        ...prev,
                        scheduled_date: date,
                        scheduled_time: startTime
                      }));
                    }
                  }}
                >
                  {slot}
                </button>
              ))}
            </div>
          </div>
        </div>

        <div className="form-section">
          <h3>📞 Contact Information</h3>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="contact_person">
                Contact Name <span className="required">*</span>
              </label>
              <input
                type="text"
                id="contact_person"
                name="contact_person"
                value={formData.contact_person}
                onChange={handleInputChange}
                placeholder="Your name"
                className={errors.contact_person ? 'error' : ''}
              />
              {errors.contact_person && <span className="error-text">{errors.contact_person}</span>}
            </div>

            <div className="form-group">
              <label htmlFor="contact_phone">
                Contact Phone <span className="required">*</span>
              </label>
              <input
                type="tel"
                id="contact_phone"
                name="contact_phone"
                value={formData.contact_phone}
                onChange={handleInputChange}
                placeholder="+91-XXXXX-XXXXX"
                className={errors.contact_phone ? 'error' : ''}
              />
              {errors.contact_phone && <span className="error-text">{errors.contact_phone}</span>}
            </div>
          </div>
        </div>

        <div className="cost-estimate">
          <div className="cost-info">
            <h4>💰 Estimated Cost</h4>
            <div className="cost-breakdown">
              <div className="cost-item">
                <span>Service Fee:</span>
                <span>₹{Math.floor(formData.quantity * 2.5) || 0}</span>
              </div>
              <div className="cost-item">
                <span>Transportation:</span>
                <span>₹50</span>
              </div>
              <div className="cost-item total">
                <span>Total:</span>
                <span>₹{(Math.floor(formData.quantity * 2.5) || 0) + 50}</span>
              </div>
            </div>
            <p className="cost-note">
              💡 Final cost may vary based on actual quantity and service type
            </p>
          </div>
        </div>

        <div className="form-actions">
          <button
            type="button"
            className="btn btn-secondary"
            onClick={onBack}
          >
            Cancel
          </button>
          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading}
          >
            {loading ? (
              <>
                <div className="btn-spinner"></div>
                Creating Booking...
              </>
            ) : (
              '📅 Book Service'
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default BookingForm;