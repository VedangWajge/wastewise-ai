import React, { useState, useEffect } from 'react';
import { AuthProvider } from './contexts/AuthContext';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Camera from './components/Camera';
import Classification from './components/Classification';
import Dashboard from './components/Dashboard';
import ServiceDiscovery from './components/ServiceDiscovery';
import BookingForm from './components/BookingForm';
import Login from './components/Auth/Login';
import Register from './components/Auth/Register';
import BookingManagement from './components/Bookings/BookingManagement';
import RewardsCenter from './components/Rewards/RewardsCenter';
import PaymentPortal from './components/Payment/PaymentPortal';
import AnalyticsDashboard from './components/Analytics/AnalyticsDashboard';
import apiService from './services/api';
import './App.css';

function App() {
  const [currentView, setCurrentView] = useState('home');
  const [classificationResult, setClassificationResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [imagePreview, setImagePreview] = useState(null);
  const [selectedService, setSelectedService] = useState(null);
  const [currentWasteType, setCurrentWasteType] = useState(null);
  const [authMode, setAuthMode] = useState('login'); // 'login' or 'register'
  const [paymentBooking, setPaymentBooking] = useState(null);

  // Handle URL hash navigation
  useEffect(() => {
    const handleHashChange = () => {
      const hash = window.location.hash.slice(1);
      if (hash) {
        setCurrentView(hash);
      }
    };

    window.addEventListener('hashchange', handleHashChange);
    handleHashChange(); // Check initial hash

    return () => {
      window.removeEventListener('hashchange', handleHashChange);
    };
  }, []);

  const handleImageCapture = async (imageFile) => {
    try {
      setIsLoading(true);
      setCurrentView('classification');

      // Create image preview
      const imageUrl = URL.createObjectURL(imageFile);
      setImagePreview(imageUrl);

      // Send for classification
      const result = await apiService.classifyWaste(imageFile);
      setClassificationResult(result);
    } catch (error) {
      console.error('Error classifying image:', error);
      alert('Failed to classify image. Please try again.');
      setCurrentView('home');
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewClassification = () => {
    setClassificationResult(null);
    setImagePreview(null);
    setSelectedService(null);
    setCurrentWasteType(null);
    setCurrentView('home');
  };

  const handleFindServices = (wasteType) => {
    setCurrentWasteType(wasteType);
    setCurrentView('services');
  };

  const handleServiceSelect = (service) => {
    setSelectedService(service);
    setCurrentView('booking');
  };

  const handleBookingComplete = (booking) => {
    alert(`Booking created successfully! Booking ID: ${booking.id}`);
    setCurrentView('bookings');
  };

  const handleLoginSuccess = () => {
    setCurrentView('dashboard');
  };

  const handleRegisterSuccess = (response) => {
    alert('Registration successful! Please check your email for verification.');
    setCurrentView('login');
  };

  const handlePaymentRequest = (bookingId, amount) => {
    setPaymentBooking({ bookingId, amount });
    setCurrentView('payment');
  };

  const handlePaymentSuccess = (payment) => {
    alert('Payment successful!');
    setPaymentBooking(null);
    setCurrentView('bookings');
  };

  const handlePaymentCancel = () => {
    setPaymentBooking(null);
    setCurrentView('bookings');
  };

  const handleBackToClassification = () => {
    setCurrentView('classification');
    setSelectedService(null);
  };

  const handleBackToServices = () => {
    setCurrentView('services');
    setSelectedService(null);
  };

  const renderContent = () => {
    switch (currentView) {
      case 'classification':
      case 'classify':
        return (
          <Classification
            result={classificationResult}
            isLoading={isLoading}
            imagePreview={imagePreview}
            onNewClassification={handleNewClassification}
            onFindServices={handleFindServices}
          />
        );
      case 'services':
        return (
          <ServiceDiscovery
            wasteType={currentWasteType}
            onServiceSelect={handleServiceSelect}
            onBack={handleBackToClassification}
          />
        );
      case 'booking':
        return (
          <BookingForm
            service={selectedService}
            wasteType={currentWasteType}
            onBookingComplete={handleBookingComplete}
            onBack={handleBackToServices}
          />
        );
      case 'bookings':
        return <BookingManagement onPaymentRequest={handlePaymentRequest} />;
      case 'rewards':
        return <RewardsCenter />;
      case 'payment':
        return paymentBooking ? (
          <PaymentPortal
            bookingId={paymentBooking.bookingId}
            amount={paymentBooking.amount}
            onPaymentSuccess={handlePaymentSuccess}
            onCancel={handlePaymentCancel}
          />
        ) : (
          <PaymentPortal />
        );
      case 'analytics':
        return <AnalyticsDashboard />;
      case 'login':
        return (
          <Login
            onSwitchToRegister={() => setCurrentView('register')}
            onLoginSuccess={handleLoginSuccess}
          />
        );
      case 'register':
        return (
          <Register
            onSwitchToLogin={() => setCurrentView('login')}
            onRegisterSuccess={handleRegisterSuccess}
          />
        );
      case 'dashboard':
        return <Dashboard />;
      default:
        return <Camera onImageCapture={handleImageCapture} />;
    }
  };

  return (
    <AuthProvider>
      <div className="App">
        <Navbar currentView={currentView} setCurrentView={setCurrentView} />

        <main className="app-main">
          {renderContent()}
        </main>

        <Footer />
      </div>
    </AuthProvider>
  );
}

export default App;
