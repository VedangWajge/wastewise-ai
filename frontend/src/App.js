import React, { useState } from 'react';
import Camera from './components/Camera';
import Classification from './components/Classification';
import Dashboard from './components/Dashboard';
import apiService from './services/api';
import './App.css';

function App() {
  const [currentView, setCurrentView] = useState('home');
  const [classificationResult, setClassificationResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [imagePreview, setImagePreview] = useState(null);

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
    setCurrentView('home');
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
      <header className="app-header">
        <div className="header-content">
          <h1 className="app-title">
            🌱 WasteWise
          </h1>
          <p className="app-subtitle">AI-Powered Smart Waste Segregation</p>
        </div>
        <nav className="app-nav">
          <button
            className={`nav-btn ${currentView === 'home' ? 'active' : ''}`}
            onClick={() => setCurrentView('home')}
          >
            📸 Classify
          </button>
          <button
            className={`nav-btn ${currentView === 'dashboard' ? 'active' : ''}`}
            onClick={() => setCurrentView('dashboard')}
          >
            📊 Dashboard
          </button>
        </nav>
      </header>

      <main className="app-main">
        {renderContent()}
      </main>

      <footer className="app-footer">
        <p>© 2024 WasteWise - Making waste management smarter with AI</p>
      </footer>
    </div>
  );
}

export default App;
