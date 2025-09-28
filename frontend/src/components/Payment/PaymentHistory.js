import React, { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import apiService from '../../services/api';

const PaymentHistory = () => {
  const { isAuthenticated } = useAuth();
  const [payments, setPayments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    if (isAuthenticated) {
      fetchPaymentHistory();
    }
  }, [isAuthenticated]);

  const fetchPaymentHistory = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await apiService.getPaymentHistory();
      if (response.success) {
        setPayments(response.payments || []);
      }
    } catch (error) {
      console.error('Error fetching payment history:', error);
      setError('Failed to load payment history');
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed':
        return '#4CAF50';
      case 'pending':
        return '#FF9800';
      case 'failed':
        return '#f44336';
      case 'refunded':
        return '#2196F3';
      default:
        return '#757575';
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const filteredPayments = payments.filter(payment => {
    if (filter === 'all') return true;
    return payment.status === filter;
  });

  if (!isAuthenticated) {
    return (
      <div className="payment-history">
        <div className="auth-required">
          <div className="auth-icon">💳</div>
          <h3>Login Required</h3>
          <p>Please login to view your payment history</p>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="payment-history">
        <div className="loading-state">
          <div className="loading-spinner"></div>
          <p>Loading payment history...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="payment-history">
        <div className="error-state">
          <div className="error-icon">❌</div>
          <h3>Error Loading Payments</h3>
          <p>{error}</p>
          <button className="retry-btn" onClick={fetchPaymentHistory}>
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="payment-history">
      <div className="history-header">
        <h2>💳 Payment History</h2>
        <div className="filter-controls">
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="status-filter"
          >
            <option value="all">All Payments</option>
            <option value="completed">Completed</option>
            <option value="pending">Pending</option>
            <option value="failed">Failed</option>
            <option value="refunded">Refunded</option>
          </select>
        </div>
      </div>

      {filteredPayments.length === 0 ? (
        <div className="no-payments">
          <div className="no-payments-icon">💸</div>
          <h3>No Payment History</h3>
          <p>You haven't made any payments yet</p>
        </div>
      ) : (
        <div className="payments-list">
          {filteredPayments.map(payment => (
            <div key={payment.id} className="payment-item">
              <div className="payment-info">
                <div className="payment-header">
                  <div className="payment-id">
                    <strong>Payment #{payment.id}</strong>
                  </div>
                  <div
                    className="payment-status"
                    style={{ backgroundColor: getStatusColor(payment.status) }}
                  >
                    {payment.status?.toUpperCase()}
                  </div>
                </div>

                <div className="payment-details">
                  <div className="detail-row">
                    <span className="detail-label">Service:</span>
                    <span className="detail-value">{payment.service_description || 'Waste Collection Service'}</span>
                  </div>

                  <div className="detail-row">
                    <span className="detail-label">Amount:</span>
                    <span className="detail-value amount">₹{payment.amount || 0}</span>
                  </div>

                  <div className="detail-row">
                    <span className="detail-label">Date:</span>
                    <span className="detail-value">
                      {payment.created_at ? formatDate(payment.created_at) : 'N/A'}
                    </span>
                  </div>

                  <div className="detail-row">
                    <span className="detail-label">Method:</span>
                    <span className="detail-value">{payment.payment_method || 'N/A'}</span>
                  </div>

                  {payment.transaction_id && (
                    <div className="detail-row">
                      <span className="detail-label">Transaction ID:</span>
                      <span className="detail-value transaction-id">{payment.transaction_id}</span>
                    </div>
                  )}

                  {payment.booking_id && (
                    <div className="detail-row">
                      <span className="detail-label">Booking ID:</span>
                      <span className="detail-value">#{payment.booking_id}</span>
                    </div>
                  )}
                </div>

                {payment.notes && (
                  <div className="payment-notes">
                    <span className="notes-label">Notes:</span>
                    <span className="notes-text">{payment.notes}</span>
                  </div>
                )}
              </div>

              <div className="payment-actions">
                {payment.status === 'completed' && (
                  <button className="btn-download">
                    📄 Download Receipt
                  </button>
                )}
                {payment.status === 'failed' && (
                  <button className="btn-retry">
                    🔄 Retry Payment
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="payment-summary">
        <div className="summary-item">
          <span className="summary-label">Total Payments:</span>
          <span className="summary-value">{filteredPayments.length}</span>
        </div>
        <div className="summary-item">
          <span className="summary-label">Total Amount:</span>
          <span className="summary-value">
            ₹{filteredPayments.reduce((sum, payment) => sum + (payment.amount || 0), 0)}
          </span>
        </div>
      </div>
    </div>
  );
};

export default PaymentHistory;