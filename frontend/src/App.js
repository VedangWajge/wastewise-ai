import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Camera from './components/Camera';
import Classification from './components/Classification';
import Dashboard from './components/Dashboard';
import ServiceDiscovery from './components/ServiceDiscovery';
import BookingForm from './components/BookingForm';
import apiService from './services/api';
import './App.css';

function App() {
  const [currentView, setCurrentView] = useState('home');
  const [classificationResult, setClassificationResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [imagePreview, setImagePreview] = useState(null);
  const [selectedService, setSelectedService] = useState(null);
  const [currentWasteType, setCurrentWasteType] = useState(null);

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
    setCurrentView('dashboard');
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
      case 'dashboard':
        return <Dashboard />;
      default:
        return <Camera onImageCapture={handleImageCapture} />;
    }
  };

  return (
    <div className="App">
      <Navbar currentView={currentView} setCurrentView={setCurrentView} />

      <main className="app-main">
        {renderContent()}
      </main>

      <Footer />
    </div>
  );
}

export default App;
