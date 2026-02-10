import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import apiService from '../services/api';
import './BookingForm.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const BookingForm = ({ service, wasteType, onBookingComplete, onBack }) => {
  const { user, isAuthenticated } = useAuth();
  const [formData, setFormData] = useState({
    quantity: '',
    pickup_address: user?.address || '',
    scheduled_date: '',
    scheduled_time_slot: '',
    special_instructions: '',
    contact_phone: user?.phone || '',
    contact_person: user?.full_name || '',
    waste_subtype: 'mixed'
  });
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});
  const [authWarning, setAuthWarning] = useState(!isAuthenticated);
  const [priceEstimate, setPriceEstimate] = useState(null);
  const [subtypes, setSubtypes] = useState([]);

  // Calculate price when quantity or subtype changes
  useEffect(() => {
    if (formData.quantity && parseFloat(formData.quantity) > 0) {
      calculatePriceEstimate();
    } else {
      setPriceEstimate(null);
    }
  }, [formData.quantity, formData.waste_subtype, wasteType]);

  const calculatePriceEstimate = async () => {
    try {
      const response = await fetch(`${API_URL}/api/marketplace/calculate-price`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          waste_type: wasteType,
          quantity_kg: parseFloat(formData.quantity),
          waste_subtype: formData.waste_subtype
        })
      });

      const data = await response.json();
      if (response.ok) {
        setPriceEstimate(data.pricing);
        if (data.available_subtypes && data.available_subtypes.length > 0) {
          setSubtypes(data.available_subtypes);
        }
      }
    } catch (error) {
      console.error('Error calculating price:', error);
    }
  };

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

          <div className="form-row">
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
                min="0.1"
                step="0.1"
                max="1000"
                className={errors.quantity ? 'error' : ''}
              />
              {errors.quantity && <span className="error-text">{errors.quantity}</span>}
            </div>

            {subtypes.length > 0 && (
              <div className="form-group">
                <label htmlFor="waste_subtype">
                  Waste Subtype
                </label>
                <select
                  id="waste_subtype"
                  name="waste_subtype"
                  value={formData.waste_subtype}
                  onChange={handleInputChange}
                >
                  {subtypes.map(st => (
                    <option key={st.subtype} value={st.subtype}>
                      {st.subtype} (₹{st.rate_per_kg}/kg)
                    </option>
                  ))}
                </select>
              </div>
            )}
          </div>

          {priceEstimate && (
            <div className="waste-value-info">
              <div className="value-badge">
                💰 Waste Value: ₹{priceEstimate.total_value}
              </div>
              <p className="value-note">
                This is the estimated market value of your waste (₹{priceEstimate.rate_per_kg}/kg)
              </p>
            </div>
          )}

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

        {priceEstimate && (
          <div className="cost-estimate">
            <div className="cost-info">
              <h4>💰 Cost & Value Breakdown</h4>
              <div className="cost-breakdown">
                <div className="cost-section">
                  <h5>Your Waste Value</h5>
                  <div className="cost-item positive">
                    <span>Market Value ({priceEstimate.rate_per_kg} × {priceEstimate.quantity_kg} kg):</span>
                    <span>+ ₹{priceEstimate.total_value}</span>
                  </div>
                </div>

                <div className="cost-section">
                  <h5>Collection Charges</h5>
                  <div className="cost-item">
                    <span>Base Pickup Charge:</span>
                    <span>₹30</span>
                  </div>
                  <div className="cost-item">
                    <span>Collection Fee ({formData.quantity} kg):</span>
                    <span>₹{(parseFloat(formData.quantity || 0) * 5).toFixed(2)}</span>
                  </div>
                  <div className="cost-item">
                    <span>GST (18%):</span>
                    <span>₹{((30 + parseFloat(formData.quantity || 0) * 5) * 0.18).toFixed(2)}</span>
                  </div>
                  <div className="cost-item subtotal">
                    <span>Total Collection Cost:</span>
                    <span>₹{((30 + parseFloat(formData.quantity || 0) * 5) * 1.18).toFixed(2)}</span>
                  </div>
                </div>

                <div className="cost-item total">
                  <span><strong>Net Amount:</strong></span>
                  <span className={priceEstimate.total_value - ((30 + parseFloat(formData.quantity || 0) * 5) * 1.18) >= 0 ? 'positive' : 'negative'}>
                    <strong>
                      {priceEstimate.total_value - ((30 + parseFloat(formData.quantity || 0) * 5) * 1.18) >= 0 ? '+ ' : '- '}
                      ₹{Math.abs(priceEstimate.total_value - ((30 + parseFloat(formData.quantity || 0) * 5) * 1.18)).toFixed(2)}
                    </strong>
                  </span>
                </div>
              </div>
              <p className="cost-note">
                {priceEstimate.total_value - ((30 + parseFloat(formData.quantity || 0) * 5) * 1.18) >= 0 ? (
                  <span className="positive">
                    ✓ You will earn money from this waste! Amount will be credited after collection.
                  </span>
                ) : (
                  <span>
                    💡 You will pay for the collection service. Final cost may vary based on actual quantity.
                  </span>
                )}
              </p>
            </div>
          </div>
        )}

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