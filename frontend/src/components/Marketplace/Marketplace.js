import React, { useState, useEffect } from 'react';
import './Marketplace.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const Marketplace = () => {
  const [view, setView] = useState('browse'); // browse, myListings, myBookings, create
  const [listings, setListings] = useState([]);
  const [filters, setFilters] = useState({
    waste_type: '',
    city: '',
    max_price: '',
    condition: ''
  });
  const [loading, setLoading] = useState(false);
  const [selectedListing, setSelectedListing] = useState(null);
  const [pagination, setPagination] = useState({
    page: 1,
    per_page: 12,
    total: 0,
    pages: 0
  });

  const wasteTypes = ['plastic', 'paper', 'metal', 'glass', 'e-waste', 'organic'];
  const conditions = ['excellent', 'good', 'fair'];

  useEffect(() => {
    if (view === 'browse') {
      fetchListings();
    } else if (view === 'myListings') {
      fetchMyListings();
    } else if (view === 'myBookings') {
      fetchMyBookings();
    }
  }, [view, filters, pagination.page]);

  const fetchListings = async () => {
    setLoading(true);
    try {
      const queryParams = new URLSearchParams({
        page: pagination.page,
        per_page: pagination.per_page,
        ...filters
      });

      const response = await fetch(`${API_URL}/api/marketplace/listings/search?${queryParams}`);
      const data = await response.json();

      if (response.ok) {
        setListings(data.listings);
        setPagination(prev => ({ ...prev, ...data.pagination }));
      }
    } catch (error) {
      console.error('Error fetching listings:', error);
    }
    setLoading(false);
  };

  const fetchMyListings = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`${API_URL}/api/marketplace/my-listings?page=${pagination.page}&per_page=${pagination.per_page}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      const data = await response.json();
      if (response.ok) {
        setListings(data.listings);
        setPagination(prev => ({ ...prev, ...data.pagination }));
      }
    } catch (error) {
      console.error('Error fetching my listings:', error);
    }
    setLoading(false);
  };

  const fetchMyBookings = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`${API_URL}/api/marketplace/my-bookings?page=${pagination.page}&per_page=${pagination.per_page}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      const data = await response.json();
      if (response.ok) {
        setListings(data.bookings);
        setPagination(prev => ({ ...prev, ...data.pagination }));
      }
    } catch (error) {
      console.error('Error fetching my bookings:', error);
    }
    setLoading(false);
  };

  const handleFilterChange = (e) => {
    setFilters({
      ...filters,
      [e.target.name]: e.target.value
    });
    setPagination(prev => ({ ...prev, page: 1 }));
  };

  const clearFilters = () => {
    setFilters({
      waste_type: '',
      city: '',
      max_price: '',
      condition: ''
    });
    setPagination(prev => ({ ...prev, page: 1 }));
  };

  const viewListingDetails = async (listingId) => {
    try {
      const response = await fetch(`${API_URL}/api/marketplace/listings/${listingId}`);
      const data = await response.json();

      if (response.ok) {
        setSelectedListing(data);
      }
    } catch (error) {
      console.error('Error fetching listing details:', error);
    }
  };

  const getWasteTypeIcon = (type) => {
    const icons = {
      'plastic': '♻️',
      'organic': '🌱',
      'paper': '📄',
      'glass': '🗞️',
      'metal': '🔧',
      'e-waste': '📱'
    };
    return icons[type] || '📦';
  };

  const getConditionBadge = (condition) => {
    const colors = {
      'excellent': '#4caf50',
      'good': '#2196f3',
      'fair': '#ff9800'
    };
    return colors[condition] || '#9e9e9e';
  };

  return (
    <div className="marketplace-container">
      <div className="marketplace-header">
        <h1>Waste Marketplace</h1>
        <p>Buy and sell recyclable waste materials</p>
      </div>

      <div className="marketplace-nav">
        <button
          className={view === 'browse' ? 'nav-btn active' : 'nav-btn'}
          onClick={() => setView('browse')}
        >
          Browse Listings
        </button>
        <button
          className={view === 'myListings' ? 'nav-btn active' : 'nav-btn'}
          onClick={() => setView('myListings')}
        >
          My Listings
        </button>
        <button
          className={view === 'myBookings' ? 'nav-btn active' : 'nav-btn'}
          onClick={() => setView('myBookings')}
        >
          My Bookings
        </button>
        <button
          className={view === 'create' ? 'nav-btn active create-btn' : 'nav-btn create-btn'}
          onClick={() => setView('create')}
        >
          + Create Listing
        </button>
      </div>

      {view === 'browse' && (
        <div className="filters-section">
          <div className="filters-container">
            <select
              name="waste_type"
              value={filters.waste_type}
              onChange={handleFilterChange}
              className="filter-input"
            >
              <option value="">All Waste Types</option>
              {wasteTypes.map(type => (
                <option key={type} value={type}>
                  {getWasteTypeIcon(type)} {type.charAt(0).toUpperCase() + type.slice(1)}
                </option>
              ))}
            </select>

            <input
              type="text"
              name="city"
              value={filters.city}
              onChange={handleFilterChange}
              placeholder="City"
              className="filter-input"
            />

            <input
              type="number"
              name="max_price"
              value={filters.max_price}
              onChange={handleFilterChange}
              placeholder="Max Price (₹)"
              className="filter-input"
            />

            <select
              name="condition"
              value={filters.condition}
              onChange={handleFilterChange}
              className="filter-input"
            >
              <option value="">All Conditions</option>
              {conditions.map(cond => (
                <option key={cond} value={cond}>
                  {cond.charAt(0).toUpperCase() + cond.slice(1)}
                </option>
              ))}
            </select>

            <button onClick={clearFilters} className="clear-filters-btn">
              Clear Filters
            </button>
          </div>
        </div>
      )}

      {view === 'create' ? (
        <CreateListing onSuccess={() => setView('myListings')} />
      ) : view === 'myBookings' ? (
        <BookingsList bookings={listings} loading={loading} />
      ) : (
        <div className="listings-section">
          {loading ? (
            <div className="loading-spinner">Loading...</div>
          ) : listings.length === 0 ? (
            <div className="no-listings">
              <p>No listings found</p>
              {view === 'myListings' && (
                <button onClick={() => setView('create')} className="create-first-btn">
                  Create Your First Listing
                </button>
              )}
            </div>
          ) : (
            <>
              <div className="listings-grid">
                {listings.map(listing => (
                  <ListingCard
                    key={listing.id}
                    listing={listing}
                    onViewDetails={viewListingDetails}
                    isOwner={view === 'myListings'}
                  />
                ))}
              </div>

              {pagination.pages > 1 && (
                <div className="pagination">
                  <button
                    onClick={() => setPagination(prev => ({ ...prev, page: prev.page - 1 }))}
                    disabled={pagination.page === 1}
                    className="page-btn"
                  >
                    Previous
                  </button>
                  <span className="page-info">
                    Page {pagination.page} of {pagination.pages}
                  </span>
                  <button
                    onClick={() => setPagination(prev => ({ ...prev, page: prev.page + 1 }))}
                    disabled={pagination.page === pagination.pages}
                    className="page-btn"
                  >
                    Next
                  </button>
                </div>
              )}
            </>
          )}
        </div>
      )}

      {selectedListing && (
        <ListingDetailsModal
          listing={selectedListing}
          onClose={() => setSelectedListing(null)}
        />
      )}
    </div>
  );
};

const ListingCard = ({ listing, onViewDetails, isOwner }) => {
  const getWasteTypeIcon = (type) => {
    const icons = {
      'plastic': '♻️',
      'organic': '🌱',
      'paper': '📄',
      'glass': '🗞️',
      'metal': '🔧',
      'e-waste': '📱'
    };
    return icons[type] || '📦';
  };

  return (
    <div className="listing-card" onClick={() => onViewDetails(listing.id)}>
      <div className="listing-header">
        <span className="waste-type-badge">
          {getWasteTypeIcon(listing.waste_type)} {listing.waste_type}
        </span>
        <span className={`status-badge status-${listing.status}`}>
          {listing.status}
        </span>
      </div>

      <h3 className="listing-title">{listing.title}</h3>

      <div className="listing-details">
        <div className="detail-row">
          <span className="detail-label">Quantity:</span>
          <span className="detail-value">{listing.quantity_kg} kg</span>
        </div>

        <div className="detail-row">
          <span className="detail-label">Price:</span>
          <span className="detail-value price">₹{listing.asking_price}</span>
        </div>

        <div className="detail-row">
          <span className="detail-label">Location:</span>
          <span className="detail-value">{listing.city || listing.location}</span>
        </div>

        {listing.condition && (
          <div className="detail-row">
            <span className="detail-label">Condition:</span>
            <span className="detail-value">{listing.condition}</span>
          </div>
        )}
      </div>

      {isOwner && listing.booking_count !== undefined && (
        <div className="listing-stats">
          <span>👁️ {listing.views_count || 0} views</span>
          <span>📋 {listing.booking_count || 0} bookings</span>
        </div>
      )}

      <div className="listing-footer">
        <span className="listing-date">
          Listed {new Date(listing.created_at).toLocaleDateString()}
        </span>
      </div>
    </div>
  );
};

const CreateListing = ({ onSuccess }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    waste_type: 'plastic',
    waste_subtype: 'mixed',
    quantity_kg: '',
    asking_price: '',
    location: '',
    city: '',
    state: '',
    pincode: '',
    condition: 'good',
    pickup_available: true,
    delivery_available: false
  });

  const [estimatedValue, setEstimatedValue] = useState(null);
  const [subtypes, setSubtypes] = useState([]);
  const [loading, setLoading] = useState(false);

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

  useEffect(() => {
    if (formData.waste_type && formData.quantity_kg) {
      calculatePrice();
    }
  }, [formData.waste_type, formData.quantity_kg, formData.waste_subtype]);

  const calculatePrice = async () => {
    try {
      const response = await fetch(`${API_URL}/api/marketplace/calculate-price`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          waste_type: formData.waste_type,
          quantity_kg: parseFloat(formData.quantity_kg),
          waste_subtype: formData.waste_subtype
        })
      });

      const data = await response.json();
      if (response.ok) {
        setEstimatedValue(data.pricing);
        setSubtypes(data.available_subtypes);

        // Auto-fill asking price if not set
        if (!formData.asking_price) {
          setFormData(prev => ({
            ...prev,
            asking_price: data.pricing.total_value
          }));
        }
      }
    } catch (error) {
      console.error('Error calculating price:', error);
    }
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`${API_URL}/api/marketplace/listings/create`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(formData)
      });

      const data = await response.json();

      if (response.ok) {
        alert('Listing created successfully!');
        onSuccess();
      } else {
        alert(data.error || 'Failed to create listing');
      }
    } catch (error) {
      console.error('Error creating listing:', error);
      alert('An error occurred while creating the listing');
    }

    setLoading(false);
  };

  return (
    <div className="create-listing-container">
      <h2>Create New Listing</h2>

      <form onSubmit={handleSubmit} className="listing-form">
        <div className="form-group">
          <label>Title *</label>
          <input
            type="text"
            name="title"
            value={formData.title}
            onChange={handleChange}
            required
            placeholder="e.g., Clean PET Bottles - 50kg"
          />
        </div>

        <div className="form-group">
          <label>Description</label>
          <textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
            rows="4"
            placeholder="Describe the waste material, its condition, and any other relevant details"
          />
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Waste Type *</label>
            <select
              name="waste_type"
              value={formData.waste_type}
              onChange={handleChange}
              required
            >
              <option value="plastic">Plastic</option>
              <option value="paper">Paper</option>
              <option value="metal">Metal</option>
              <option value="glass">Glass</option>
              <option value="e-waste">E-Waste</option>
              <option value="organic">Organic</option>
            </select>
          </div>

          <div className="form-group">
            <label>Subtype</label>
            <select
              name="waste_subtype"
              value={formData.waste_subtype}
              onChange={handleChange}
            >
              {subtypes.length > 0 ? (
                subtypes.map(st => (
                  <option key={st.subtype} value={st.subtype}>
                    {st.subtype} (₹{st.rate_per_kg}/kg)
                  </option>
                ))
              ) : (
                <option value="mixed">Mixed</option>
              )}
            </select>
          </div>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>Quantity (kg) *</label>
            <input
              type="number"
              name="quantity_kg"
              value={formData.quantity_kg}
              onChange={handleChange}
              required
              min="0.1"
              step="0.1"
            />
          </div>

          <div className="form-group">
            <label>Condition *</label>
            <select
              name="condition"
              value={formData.condition}
              onChange={handleChange}
              required
            >
              <option value="excellent">Excellent</option>
              <option value="good">Good</option>
              <option value="fair">Fair</option>
            </select>
          </div>
        </div>

        {estimatedValue && (
          <div className="price-estimate">
            <h4>Estimated Value</h4>
            <div className="estimate-details">
              <p>Rate: ₹{estimatedValue.rate_per_kg}/kg</p>
              <p className="total-value">Total: ₹{estimatedValue.total_value}</p>
            </div>
          </div>
        )}

        <div className="form-group">
          <label>Asking Price (₹) *</label>
          <input
            type="number"
            name="asking_price"
            value={formData.asking_price}
            onChange={handleChange}
            required
            min="0"
            step="0.01"
          />
        </div>

        <div className="form-group">
          <label>Location *</label>
          <input
            type="text"
            name="location"
            value={formData.location}
            onChange={handleChange}
            required
            placeholder="Full address"
          />
        </div>

        <div className="form-row">
          <div className="form-group">
            <label>City *</label>
            <input
              type="text"
              name="city"
              value={formData.city}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label>State</label>
            <input
              type="text"
              name="state"
              value={formData.state}
              onChange={handleChange}
            />
          </div>

          <div className="form-group">
            <label>Pincode</label>
            <input
              type="text"
              name="pincode"
              value={formData.pincode}
              onChange={handleChange}
            />
          </div>
        </div>

        <div className="form-group checkbox-group">
          <label>
            <input
              type="checkbox"
              name="pickup_available"
              checked={formData.pickup_available}
              onChange={handleChange}
            />
            Pickup Available
          </label>

          <label>
            <input
              type="checkbox"
              name="delivery_available"
              checked={formData.delivery_available}
              onChange={handleChange}
            />
            Delivery Available
          </label>
        </div>

        <button type="submit" className="submit-btn" disabled={loading}>
          {loading ? 'Creating...' : 'Create Listing'}
        </button>
      </form>
    </div>
  );
};

const ListingDetailsModal = ({ listing, onClose }) => {
  const [bookingForm, setBookingForm] = useState({
    pickup_date: '',
    pickup_time_slot: '',
    contact_person: '',
    contact_phone: '',
    special_instructions: ''
  });
  const [showBookingForm, setShowBookingForm] = useState(false);
  const [loading, setLoading] = useState(false);

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

  const handleBooking = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const token = localStorage.getItem('access_token');
      const response = await fetch(`${API_URL}/api/marketplace/listings/${listing.id}/book`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(bookingForm)
      });

      const data = await response.json();

      if (response.ok) {
        alert('Booking created successfully! Please complete the payment.');
        onClose();
      } else {
        alert(data.error || 'Failed to create booking');
      }
    } catch (error) {
      console.error('Error creating booking:', error);
      alert('An error occurred while creating the booking');
    }

    setLoading(false);
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="close-btn" onClick={onClose}>×</button>

        <div className="listing-details-full">
          <h2>{listing.title}</h2>

          <div className="listing-meta">
            <span className="waste-type-badge">{listing.waste_type}</span>
            <span className="status-badge">{listing.status}</span>
          </div>

          <div className="details-grid">
            <div className="detail-item">
              <strong>Quantity:</strong> {listing.quantity_kg} kg
            </div>
            <div className="detail-item">
              <strong>Price:</strong> ₹{listing.asking_price}
            </div>
            <div className="detail-item">
              <strong>Condition:</strong> {listing.condition}
            </div>
            <div className="detail-item">
              <strong>Subtype:</strong> {listing.waste_subtype}
            </div>
          </div>

          <div className="description-section">
            <h3>Description</h3>
            <p>{listing.description || 'No description provided'}</p>
          </div>

          <div className="location-section">
            <h3>Location</h3>
            <p>{listing.location}</p>
            {listing.city && <p>{listing.city}, {listing.state} - {listing.pincode}</p>}
          </div>

          <div className="availability-section">
            <h3>Availability</h3>
            <p>
              {listing.pickup_available && '✓ Pickup Available'}
              {listing.delivery_available && ' | ✓ Delivery Available'}
            </p>
          </div>

          <div className="seller-section">
            <h3>Seller Information</h3>
            <p><strong>Name:</strong> {listing.seller_name}</p>
            <p><strong>Phone:</strong> {listing.seller_phone}</p>
            {listing.seller_stats && (
              <div className="seller-stats">
                <p>Average Rating: {listing.seller_stats.average_rating?.toFixed(1) || 'N/A'} ⭐</p>
                <p>Total Reviews: {listing.seller_stats.total_reviews || 0}</p>
              </div>
            )}
          </div>

          {!showBookingForm ? (
            <button
              className="book-btn"
              onClick={() => setShowBookingForm(true)}
              disabled={listing.status !== 'active'}
            >
              Book This Listing
            </button>
          ) : (
            <form onSubmit={handleBooking} className="booking-form-modal">
              <h3>Book This Listing</h3>

              <div className="form-group">
                <label>Pickup Date *</label>
                <input
                  type="date"
                  value={bookingForm.pickup_date}
                  onChange={(e) => setBookingForm({...bookingForm, pickup_date: e.target.value})}
                  required
                  min={new Date().toISOString().split('T')[0]}
                />
              </div>

              <div className="form-group">
                <label>Time Slot *</label>
                <select
                  value={bookingForm.pickup_time_slot}
                  onChange={(e) => setBookingForm({...bookingForm, pickup_time_slot: e.target.value})}
                  required
                >
                  <option value="">Select time slot</option>
                  <option value="09:00-12:00">09:00 AM - 12:00 PM</option>
                  <option value="12:00-15:00">12:00 PM - 03:00 PM</option>
                  <option value="15:00-18:00">03:00 PM - 06:00 PM</option>
                </select>
              </div>

              <div className="form-group">
                <label>Contact Person *</label>
                <input
                  type="text"
                  value={bookingForm.contact_person}
                  onChange={(e) => setBookingForm({...bookingForm, contact_person: e.target.value})}
                  required
                />
              </div>

              <div className="form-group">
                <label>Contact Phone *</label>
                <input
                  type="tel"
                  value={bookingForm.contact_phone}
                  onChange={(e) => setBookingForm({...bookingForm, contact_phone: e.target.value})}
                  required
                />
              </div>

              <div className="form-group">
                <label>Special Instructions</label>
                <textarea
                  value={bookingForm.special_instructions}
                  onChange={(e) => setBookingForm({...bookingForm, special_instructions: e.target.value})}
                  rows="3"
                />
              </div>

              <button type="submit" className="submit-btn" disabled={loading}>
                {loading ? 'Booking...' : 'Confirm Booking'}
              </button>
            </form>
          )}
        </div>
      </div>
    </div>
  );
};

const BookingsList = ({ bookings, loading }) => {
  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

  const handlePayment = async (booking) => {
    try {
      const token = localStorage.getItem('access_token');

      // Initiate payment for this booking
      const response = await fetch(`${API_URL}/api/marketplace/bookings/${booking.id}/payment`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          payment_method: 'razorpay'
        })
      });

      const data = await response.json();

      if (response.ok) {
        // Open Razorpay checkout
        const options = {
          key: data.razorpay_key_id,
          amount: data.amount * 100, // Convert to paise
          currency: 'INR',
          name: 'WasteWise Marketplace',
          description: `Payment for ${booking.listing_title}`,
          order_id: data.razorpay_order_id,
          handler: async function (response) {
            // Verify payment
            try {
              const verifyResponse = await fetch(`${API_URL}/api/payments/verify`, {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                  'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                  payment_id: data.payment_id,
                  razorpay_order_id: response.razorpay_order_id,
                  razorpay_payment_id: response.razorpay_payment_id,
                  razorpay_signature: response.razorpay_signature
                })
              });

              if (verifyResponse.ok) {
                alert('Payment successful! Your booking is confirmed.');
                window.location.reload();
              } else {
                alert('Payment verification failed');
              }
            } catch (err) {
              alert('Error verifying payment');
            }
          },
          prefill: {
            name: booking.contact_person,
            contact: booking.contact_phone
          },
          theme: {
            color: '#4caf50'
          }
        };

        const razorpay = new window.Razorpay(options);
        razorpay.open();
      } else {
        alert(data.error || 'Failed to initiate payment');
      }
    } catch (error) {
      console.error('Payment error:', error);
      alert('An error occurred while processing payment');
    }
  };

  if (loading) {
    return <div className="loading-spinner">Loading...</div>;
  }

  if (bookings.length === 0) {
    return <div className="no-listings"><p>No bookings found</p></div>;
  }

  return (
    <div className="bookings-list">
      {bookings.map(booking => (
        <div key={booking.id} className="booking-card">
          <div className="booking-header">
            <h3>{booking.listing_title}</h3>
            <span className={`status-badge status-${booking.status}`}>
              {booking.status}
            </span>
          </div>

          <div className="booking-details">
            <p><strong>Waste Type:</strong> {booking.waste_type} ({booking.waste_subtype})</p>
            <p><strong>Quantity:</strong> {booking.quantity_kg} kg</p>
            <p><strong>Price:</strong> ₹{booking.agreed_price}</p>
            <p><strong>Seller:</strong> {booking.seller_name}</p>
            <p><strong>Pickup Date:</strong> {booking.pickup_date} ({booking.pickup_time_slot})</p>
            <p><strong>Payment Status:</strong>
              <span className={`payment-status payment-${booking.payment_status}`}>
                {booking.payment_status}
              </span>
            </p>
          </div>

          {booking.payment_status === 'pending' && (
            <div className="booking-actions">
              <button
                className="btn btn-primary pay-now-btn"
                onClick={() => handlePayment(booking)}
              >
                💳 Pay Now - ₹{booking.agreed_price}
              </button>
            </div>
          )}

          <div className="booking-footer">
            <span className="booking-date">
              Booked on {new Date(booking.created_at).toLocaleDateString()}
            </span>
          </div>
        </div>
      ))}
    </div>
  );
};

export default Marketplace;
