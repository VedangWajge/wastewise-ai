import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import apiService from '../../services/api';
import PaymentForm from './PaymentForm';
import PaymentHistory from './PaymentHistory';
import './PaymentPortal.css';

const PaymentPortal = ({ bookingId, amount, onPaymentSuccess, onCancel }) => {
  const { user, isAuthenticated } = useAuth();
  const [activeTab, setActiveTab] = useState('payment');
  const [paymentMethods, setPaymentMethods] = useState([]);
  const [paymentHistory, setPaymentHistory] = useState([]);
  const [pendingBookings, setPendingBookings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [processing, setProcessing] = useState(false);
  const [selectedBooking, setSelectedBooking] = useState(null);

  useEffect(() => {
    if (isAuthenticated) {
      fetchPaymentData();
    }
  }, [isAuthenticated]);

  const fetchPaymentData = async () => {
    try {
      setLoading(true);
      setError(null);

      const [methodsResponse, historyResponse, bookingsResponse] = await Promise.all([
        apiService.getPaymentMethods(),
        apiService.getPaymentHistory(),
        apiService.getBookings() // Fetch user's bookings
      ]);

      if (methodsResponse.success) {
        setPaymentMethods(methodsResponse.payment_methods);
      }

      if (historyResponse.success) {
        setPaymentHistory(historyResponse.payments);
      }

      if (bookingsResponse.success) {
        // Filter bookings with pending payment status
        const pending = bookingsResponse.bookings.filter(
          booking => booking.payment_status === 'pending' && booking.status !== 'cancelled'
        );
        setPendingBookings(pending);
      }
    } catch (error) {
      console.error('Error fetching payment data:', error);
      setError(error.message || 'Failed to load payment data');
    } finally {
      setLoading(false);
    }
  };

  const handlePaymentSubmit = async (paymentData) => {
    try {
      setProcessing(true);
      setError(null);

      // Use either the provided bookingId or the selected booking
      const targetBookingId = bookingId || selectedBooking?.id;
      const targetAmount = amount || selectedBooking?.estimated_cost || selectedBooking?.total_amount;

      if (!targetBookingId || !targetAmount) {
        throw new Error('Invalid booking or amount');
      }

      // Step 1: Initiate payment
      const initiateResponse = await apiService.initiatePayment({
        booking_id: targetBookingId,
        amount: targetAmount,
        payment_method: paymentData.method,
        currency: 'INR'
      });

      if (!initiateResponse.success) {
        throw new Error(initiateResponse.message || 'Payment initiation failed');
      }

      console.log('Payment initiated:', initiateResponse);

      // Step 2: Open Razorpay checkout for real payment
      // Check if we should use Razorpay checkout (for card/UPI)
      if (initiateResponse.gateway_key && initiateResponse.options) {
        // Real Razorpay integration
        await openRazorpayCheckout(initiateResponse, targetBookingId);
      } else {
        // Fallback: Simulate payment gateway processing (for testing)
        await simulatePaymentGateway(initiateResponse, paymentData);

        // Step 3: Verify payment
        const verifyResponse = await apiService.verifyPayment({
          payment_id: initiateResponse.payment_id,
          razorpay_order_id: initiateResponse.order_id,
          razorpay_payment_id: `pay_${Date.now()}`,
          razorpay_signature: `sig_${Date.now()}`
        });

        if (verifyResponse.success) {
          // Refresh data after successful payment
          await fetchPaymentData();
          setSelectedBooking(null);

          if (onPaymentSuccess) {
            onPaymentSuccess(verifyResponse.payment);
          } else {
            // If no callback, switch to history tab
            setActiveTab('history');
            alert('Payment successful!');
          }
        } else {
          throw new Error(verifyResponse.message || 'Payment verification failed');
        }
      }
    } catch (error) {
      console.error('Payment error:', error);
      setError(error.message || 'Payment failed. Please try again.');
    } finally {
      setProcessing(false);
    }
  };

  const openRazorpayCheckout = (paymentData, bookingId) => {
    return new Promise((resolve, reject) => {
      // Load Razorpay script if not already loaded
      if (!window.Razorpay) {
        const script = document.createElement('script');
        script.src = 'https://checkout.razorpay.com/v1/checkout.js';
        script.onerror = () => reject(new Error('Failed to load Razorpay SDK'));
        script.onload = () => initializeRazorpay();
        document.body.appendChild(script);
      } else {
        initializeRazorpay();
      }

      function initializeRazorpay() {
        const options = {
          key: paymentData.gateway_key,
          amount: paymentData.options.amount,
          currency: paymentData.options.currency,
          name: paymentData.options.name,
          description: paymentData.options.description,
          order_id: paymentData.options.order_id,
          prefill: paymentData.options.prefill,
          theme: paymentData.options.theme,
          handler: async function (response) {
            try {
              // Payment successful - verify on backend
              const verifyResponse = await apiService.verifyPayment({
                payment_id: paymentData.payment_id,
                razorpay_order_id: response.razorpay_order_id,
                razorpay_payment_id: response.razorpay_payment_id,
                razorpay_signature: response.razorpay_signature
              });

              if (verifyResponse.success) {
                await fetchPaymentData();
                setSelectedBooking(null);
                setProcessing(false);

                if (onPaymentSuccess) {
                  onPaymentSuccess(verifyResponse.payment);
                } else {
                  setActiveTab('history');
                  alert('Payment successful!');
                }
                resolve(verifyResponse);
              } else {
                throw new Error(verifyResponse.message || 'Payment verification failed');
              }
            } catch (error) {
              setProcessing(false);
              setError(error.message);
              reject(error);
            }
          },
          modal: {
            ondismiss: function () {
              setProcessing(false);
              setError('Payment cancelled');
              reject(new Error('Payment cancelled by user'));
            }
          }
        };

        const rzp = new window.Razorpay(options);
        rzp.on('payment.failed', function (response) {
          setProcessing(false);
          setError(`Payment failed: ${response.error.description}`);
          reject(new Error(response.error.description));
        });

        rzp.open();
      }
    });
  };

  const handleBookingSelect = (booking) => {
    setSelectedBooking(booking);
    setError(null);
  };

  const handleCancelBookingPayment = () => {
    setSelectedBooking(null);
    setError(null);
  };

  const simulatePaymentGateway = async (paymentDetails, paymentData) => {
    // Simulate payment processing delay
    await new Promise(resolve => setTimeout(resolve, 2000));

    // Simulate random payment failure (5% chance)
    if (Math.random() < 0.05) {
      throw new Error('Payment declined by gateway');
    }

    return {
      status: 'success',
      transaction_id: `txn_${Date.now()}`,
      gateway_response: 'Payment successful'
    };
  };

  if (!isAuthenticated) {
    return (
      <div className="payment-portal">
        <div className="auth-required">
          <div className="auth-icon">💳</div>
          <h3>Login Required</h3>
          <p>Please login to access payment features</p>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="payment-portal">
        <div className="loading-state">
          <div className="loading-spinner"></div>
          <p>Loading payment information...</p>
        </div>
      </div>
    );
  }

  if (error && !bookingId) {
    return (
      <div className="payment-portal">
        <div className="error-state">
          <div className="error-icon">❌</div>
          <h3>Error Loading Payment Data</h3>
          <p>{error}</p>
          <button className="retry-btn" onClick={fetchPaymentData}>
            Try Again
          </button>
        </div>
      </div>
    );
  }

  // If we have a specific booking to pay for
  if (bookingId && amount) {
    return (
      <div className="payment-portal booking-payment">
        <div className="payment-header">
          <h2>💳 Complete Payment</h2>
          <p>Secure payment for your waste collection booking</p>
          {onCancel && (
            <button className="close-btn" onClick={onCancel}>✕</button>
          )}
        </div>

        <div className="payment-summary">
          <div className="summary-card">
            <h3>Payment Summary</h3>
            <div className="summary-details">
              <div className="detail-row">
                <span>Booking ID:</span>
                <span>#{bookingId.slice(-8)}</span>
              </div>
              <div className="detail-row">
                <span>Service Amount:</span>
                <span>₹{amount}</span>
              </div>
              <div className="detail-row">
                <span>Processing Fee:</span>
                <span>₹{Math.round(amount * 0.02)}</span>
              </div>
              <div className="detail-row total">
                <span>Total Amount:</span>
                <span>₹{amount + Math.round(amount * 0.02)}</span>
              </div>
            </div>
          </div>
        </div>

        {error && (
          <div className="error-alert">
            <span className="error-icon">⚠️</span>
            {error}
          </div>
        )}

        <PaymentForm
          amount={amount + Math.round(amount * 0.02)}
          paymentMethods={paymentMethods}
          onSubmit={handlePaymentSubmit}
          loading={processing}
          disabled={processing}
        />

        <div className="security-notice">
          <div className="security-icon">🔒</div>
          <div className="security-text">
            <h4>Secure Payment</h4>
            <p>Your payment information is encrypted and secure. We never store your card details.</p>
          </div>
        </div>
      </div>
    );
  }

  // General payment portal view
  const tabs = [
    { id: 'payment', label: 'Make Payment', icon: '💳' },
    { id: 'history', label: 'Payment History', icon: '📋' },
  ];

  return (
    <div className="payment-portal">
      <div className="payment-header">
        <h2>💳 Payment Center</h2>
        <p>Manage your payments and view transaction history</p>
      </div>

      <div className="payment-navigation">
        {tabs.map(tab => (
          <button
            key={tab.id}
            className={`nav-tab ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
          >
            <span className="tab-icon">{tab.icon}</span>
            <span className="tab-label">{tab.label}</span>
          </button>
        ))}
      </div>

      <div className="payment-content">
        {activeTab === 'payment' ? (
          <div className="payment-tab">
            {selectedBooking ? (
              // Show payment form for selected booking
              <div className="selected-booking-payment">
                <div className="payment-header">
                  <h3>💳 Complete Payment</h3>
                  <button className="back-btn" onClick={handleCancelBookingPayment}>
                    ← Back to Bookings
                  </button>
                </div>

                <div className="payment-summary">
                  <div className="summary-card">
                    <h4>Payment Summary</h4>
                    <div className="summary-details">
                      <div className="detail-row">
                        <span>Booking ID:</span>
                        <span>#{selectedBooking.id.slice(-8)}</span>
                      </div>
                      <div className="detail-row">
                        <span>Waste Type:</span>
                        <span>{selectedBooking.waste_type}</span>
                      </div>
                      <div className="detail-row">
                        <span>Quantity:</span>
                        <span>{selectedBooking.quantity}</span>
                      </div>
                      <div className="detail-row">
                        <span>Service Amount:</span>
                        <span>₹{selectedBooking.estimated_cost || selectedBooking.total_amount}</span>
                      </div>
                      <div className="detail-row">
                        <span>Processing Fee:</span>
                        <span>₹{Math.round((selectedBooking.estimated_cost || selectedBooking.total_amount) * 0.02)}</span>
                      </div>
                      <div className="detail-row total">
                        <span>Total Amount:</span>
                        <span>₹{(selectedBooking.estimated_cost || selectedBooking.total_amount) + Math.round((selectedBooking.estimated_cost || selectedBooking.total_amount) * 0.02)}</span>
                      </div>
                    </div>
                  </div>
                </div>

                {error && (
                  <div className="error-alert">
                    <span className="error-icon">⚠️</span>
                    {error}
                  </div>
                )}

                <PaymentForm
                  amount={(selectedBooking.estimated_cost || selectedBooking.total_amount) + Math.round((selectedBooking.estimated_cost || selectedBooking.total_amount) * 0.02)}
                  paymentMethods={paymentMethods}
                  onSubmit={handlePaymentSubmit}
                  loading={processing}
                  disabled={processing}
                />

                <div className="security-notice">
                  <div className="security-icon">🔒</div>
                  <div className="security-text">
                    <h4>Secure Payment</h4>
                    <p>Your payment information is encrypted and secure. We never store your card details.</p>
                  </div>
                </div>
              </div>
            ) : pendingBookings.length > 0 ? (
              // Show list of pending bookings
              <div className="pending-bookings-list">
                <h3>💰 Pending Payments ({pendingBookings.length})</h3>
                <p className="subtitle">Select a booking to complete payment</p>

                <div className="bookings-grid">
                  {pendingBookings.map(booking => (
                    <div key={booking.id} className="booking-payment-card">
                      <div className="booking-header">
                        <div className="booking-id">
                          <span className="label">Booking ID:</span>
                          <span className="value">#{booking.id.slice(-8)}</span>
                        </div>
                        <span className="payment-badge pending">Pending</span>
                      </div>

                      <div className="booking-details">
                        <div className="detail-item">
                          <span className="icon">🗑️</span>
                          <div>
                            <div className="detail-label">Waste Type</div>
                            <div className="detail-value">{booking.waste_type}</div>
                          </div>
                        </div>

                        <div className="detail-item">
                          <span className="icon">⚖️</span>
                          <div>
                            <div className="detail-label">Quantity</div>
                            <div className="detail-value">{booking.quantity}</div>
                          </div>
                        </div>

                        <div className="detail-item">
                          <span className="icon">📍</span>
                          <div>
                            <div className="detail-label">Location</div>
                            <div className="detail-value">{booking.pickup_address?.substring(0, 40)}...</div>
                          </div>
                        </div>

                        <div className="detail-item">
                          <span className="icon">📅</span>
                          <div>
                            <div className="detail-label">Scheduled</div>
                            <div className="detail-value">
                              {new Date(booking.scheduled_date).toLocaleDateString()}
                            </div>
                          </div>
                        </div>
                      </div>

                      <div className="booking-footer">
                        <div className="amount">
                          <span className="amount-label">Amount Due:</span>
                          <span className="amount-value">₹{booking.estimated_cost || booking.total_amount}</span>
                        </div>
                        <button
                          className="pay-btn"
                          onClick={() => handleBookingSelect(booking)}
                        >
                          💳 Pay Now
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              // No pending payments
              <div className="no-pending-payments">
                <div className="empty-icon">💰</div>
                <h3>No Pending Payments</h3>
                <p>You don't have any pending payments at the moment.</p>
                <button
                  className="cta-btn"
                  onClick={() => window.location.hash = 'classify'}
                >
                  Book a Service
                </button>
              </div>
            )}
          </div>
        ) : (
          <PaymentHistory payments={paymentHistory} />
        )}
      </div>
    </div>
  );
};

export default PaymentPortal;