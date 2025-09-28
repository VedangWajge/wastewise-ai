import React, { useState } from 'react';
import './PaymentForm.css';

const PaymentForm = ({ amount, paymentMethods, onSubmit, loading, disabled }) => {
  const [formData, setFormData] = useState({
    method: 'card',
    cardNumber: '',
    expiryMonth: '',
    expiryYear: '',
    cvv: '',
    cardName: '',
    upiId: '',
    bankAccount: '',
    saveCard: false,
  });
  const [errors, setErrors] = useState({});

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    let formattedValue = value;

    // Format card number with spaces
    if (name === 'cardNumber') {
      formattedValue = value.replace(/\s/g, '').replace(/(.{4})/g, '$1 ').trim();
      if (formattedValue.length > 19) return; // Max 16 digits + 3 spaces
    }

    // Limit CVV to 3-4 digits
    if (name === 'cvv' && value.length > 4) return;

    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : formattedValue
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

    if (formData.method === 'card') {
      if (!formData.cardNumber) {
        newErrors.cardNumber = 'Card number is required';
      } else if (formData.cardNumber.replace(/\s/g, '').length < 16) {
        newErrors.cardNumber = 'Card number must be 16 digits';
      }

      if (!formData.expiryMonth) {
        newErrors.expiryMonth = 'Expiry month is required';
      }

      if (!formData.expiryYear) {
        newErrors.expiryYear = 'Expiry year is required';
      }

      if (!formData.cvv) {
        newErrors.cvv = 'CVV is required';
      } else if (formData.cvv.length < 3) {
        newErrors.cvv = 'CVV must be 3-4 digits';
      }

      if (!formData.cardName.trim()) {
        newErrors.cardName = 'Cardholder name is required';
      }

      // Check if card is expired
      if (formData.expiryMonth && formData.expiryYear) {
        const currentDate = new Date();
        const cardExpiry = new Date(parseInt(formData.expiryYear), parseInt(formData.expiryMonth) - 1);
        if (cardExpiry < currentDate) {
          newErrors.expiryMonth = 'Card is expired';
        }
      }
    }

    if (formData.method === 'upi') {
      if (!formData.upiId) {
        newErrors.upiId = 'UPI ID is required';
      } else if (!formData.upiId.includes('@')) {
        newErrors.upiId = 'Invalid UPI ID format';
      }
    }

    if (formData.method === 'netbanking') {
      if (!formData.bankAccount) {
        newErrors.bankAccount = 'Please select a bank';
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    onSubmit(formData);
  };

  const getCardIcon = (cardNumber) => {
    const number = cardNumber.replace(/\s/g, '');
    if (number.startsWith('4')) return '💳'; // Visa
    if (number.startsWith('5') || number.startsWith('2')) return '💳'; // Mastercard
    if (number.startsWith('3')) return '💳'; // Amex
    return '💳';
  };

  const months = Array.from({ length: 12 }, (_, i) => {
    const month = i + 1;
    return { value: month.toString().padStart(2, '0'), label: month.toString().padStart(2, '0') };
  });

  const currentYear = new Date().getFullYear();
  const years = Array.from({ length: 10 }, (_, i) => currentYear + i);

  const banks = [
    { value: 'sbi', label: 'State Bank of India' },
    { value: 'hdfc', label: 'HDFC Bank' },
    { value: 'icici', label: 'ICICI Bank' },
    { value: 'axis', label: 'Axis Bank' },
    { value: 'kotak', label: 'Kotak Mahindra Bank' },
    { value: 'pnb', label: 'Punjab National Bank' },
  ];

  return (
    <div className="payment-form">
      <form onSubmit={handleSubmit}>
        <div className="amount-display">
          <div className="amount-label">Amount to Pay</div>
          <div className="amount-value">₹{amount}</div>
        </div>

        <div className="payment-methods">
          <h3>Select Payment Method</h3>
          <div className="method-options">
            {paymentMethods.map(method => (
              <label key={method.id} className="method-option">
                <input
                  type="radio"
                  name="method"
                  value={method.id}
                  checked={formData.method === method.id}
                  onChange={handleInputChange}
                  disabled={disabled}
                />
                <div className="method-content">
                  <span className="method-icon">{method.icon}</span>
                  <span className="method-name">{method.name}</span>
                  {method.popular && <span className="popular-badge">Popular</span>}
                </div>
              </label>
            ))}
          </div>
        </div>

        {formData.method === 'card' && (
          <div className="payment-details card-details">
            <h3>Card Details</h3>

            <div className="form-group">
              <label htmlFor="cardNumber">
                Card Number <span className="required">*</span>
              </label>
              <div className="card-input-wrapper">
                <input
                  type="text"
                  id="cardNumber"
                  name="cardNumber"
                  value={formData.cardNumber}
                  onChange={handleInputChange}
                  placeholder="1234 5678 9012 3456"
                  className={errors.cardNumber ? 'error' : ''}
                  disabled={disabled}
                />
                <span className="card-icon">{getCardIcon(formData.cardNumber)}</span>
              </div>
              {errors.cardNumber && <span className="field-error">{errors.cardNumber}</span>}
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="expiryMonth">
                  Expiry Month <span className="required">*</span>
                </label>
                <select
                  id="expiryMonth"
                  name="expiryMonth"
                  value={formData.expiryMonth}
                  onChange={handleInputChange}
                  className={errors.expiryMonth ? 'error' : ''}
                  disabled={disabled}
                >
                  <option value="">MM</option>
                  {months.map(month => (
                    <option key={month.value} value={month.value}>
                      {month.label}
                    </option>
                  ))}
                </select>
                {errors.expiryMonth && <span className="field-error">{errors.expiryMonth}</span>}
              </div>

              <div className="form-group">
                <label htmlFor="expiryYear">
                  Expiry Year <span className="required">*</span>
                </label>
                <select
                  id="expiryYear"
                  name="expiryYear"
                  value={formData.expiryYear}
                  onChange={handleInputChange}
                  className={errors.expiryYear ? 'error' : ''}
                  disabled={disabled}
                >
                  <option value="">YYYY</option>
                  {years.map(year => (
                    <option key={year} value={year}>
                      {year}
                    </option>
                  ))}
                </select>
                {errors.expiryYear && <span className="field-error">{errors.expiryYear}</span>}
              </div>

              <div className="form-group">
                <label htmlFor="cvv">
                  CVV <span className="required">*</span>
                </label>
                <input
                  type="password"
                  id="cvv"
                  name="cvv"
                  value={formData.cvv}
                  onChange={handleInputChange}
                  placeholder="123"
                  maxLength="4"
                  className={errors.cvv ? 'error' : ''}
                  disabled={disabled}
                />
                {errors.cvv && <span className="field-error">{errors.cvv}</span>}
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="cardName">
                Cardholder Name <span className="required">*</span>
              </label>
              <input
                type="text"
                id="cardName"
                name="cardName"
                value={formData.cardName}
                onChange={handleInputChange}
                placeholder="Name as on card"
                className={errors.cardName ? 'error' : ''}
                disabled={disabled}
              />
              {errors.cardName && <span className="field-error">{errors.cardName}</span>}
            </div>

            <div className="form-group checkbox-group">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  name="saveCard"
                  checked={formData.saveCard}
                  onChange={handleInputChange}
                  disabled={disabled}
                />
                <span className="checkmark"></span>
                Save this card for future payments
              </label>
            </div>
          </div>
        )}

        {formData.method === 'upi' && (
          <div className="payment-details upi-details">
            <h3>UPI Details</h3>
            <div className="form-group">
              <label htmlFor="upiId">
                UPI ID <span className="required">*</span>
              </label>
              <input
                type="text"
                id="upiId"
                name="upiId"
                value={formData.upiId}
                onChange={handleInputChange}
                placeholder="yourname@paytm"
                className={errors.upiId ? 'error' : ''}
                disabled={disabled}
              />
              {errors.upiId && <span className="field-error">{errors.upiId}</span>}
            </div>
          </div>
        )}

        {formData.method === 'netbanking' && (
          <div className="payment-details netbanking-details">
            <h3>Net Banking</h3>
            <div className="form-group">
              <label htmlFor="bankAccount">
                Select Bank <span className="required">*</span>
              </label>
              <select
                id="bankAccount"
                name="bankAccount"
                value={formData.bankAccount}
                onChange={handleInputChange}
                className={errors.bankAccount ? 'error' : ''}
                disabled={disabled}
              >
                <option value="">Choose your bank</option>
                {banks.map(bank => (
                  <option key={bank.value} value={bank.value}>
                    {bank.label}
                  </option>
                ))}
              </select>
              {errors.bankAccount && <span className="field-error">{errors.bankAccount}</span>}
            </div>
          </div>
        )}

        <button
          type="submit"
          className="payment-btn"
          disabled={disabled || loading}
        >
          {loading ? (
            <>
              <div className="btn-spinner"></div>
              Processing Payment...
            </>
          ) : (
            <>
              <span className="btn-icon">💳</span>
              Pay ₹{amount}
            </>
          )}
        </button>
      </form>
    </div>
  );
};

export default PaymentForm;