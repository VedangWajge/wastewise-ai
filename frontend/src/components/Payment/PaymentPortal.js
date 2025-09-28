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
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [processing, setProcessing] = useState(false);

  useEffect(() => {
    if (isAuthenticated) {
      fetchPaymentData();
    }
  }, [isAuthenticated]);

  const fetchPaymentData = async () => {
    try {
      setLoading(true);
      setError(null);

      const [methodsResponse, historyResponse] = await Promise.all([
        apiService.getPaymentMethods(),
        apiService.getPaymentHistory()
      ]);

      if (methodsResponse.success) {
        setPaymentMethods(methodsResponse.payment_methods);
      }

      if (historyResponse.success) {
        setPaymentHistory(historyResponse.payments);
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

      // Step 1: Initiate payment
      const initiateResponse = await apiService.initiatePayment({
        booking_id: bookingId,
        amount: amount,
        payment_method: paymentData.method,
        currency: 'INR'
      });

      if (!initiateResponse.success) {
        throw new Error(initiateResponse.message || 'Payment initiation failed');
      }

      // Step 2: Simulate payment gateway processing
      // In a real implementation, this would integrate with Razorpay or similar
      await simulatePaymentGateway(initiateResponse.payment_details, paymentData);

      // Step 3: Verify payment
      const verifyResponse = await apiService.verifyPayment({
        payment_id: initiateResponse.payment_details.payment_id,
        razorpay_order_id: initiateResponse.payment_details.order_id,
        razorpay_payment_id: `pay_${Date.now()}`,
        razorpay_signature: `sig_${Date.now()}`
      });

      if (verifyResponse.success) {
        onPaymentSuccess && onPaymentSuccess(verifyResponse.payment);
      } else {
        throw new Error(verifyResponse.message || 'Payment verification failed');
      }
    } catch (error) {
      console.error('Payment error:', error);
      setError(error.message || 'Payment failed. Please try again.');
    } finally {
      setProcessing(false);
    }
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
          </div>
        ) : (
          <PaymentHistory payments={paymentHistory} />
        )}
      </div>
    </div>
  );
};

export default PaymentPortal;