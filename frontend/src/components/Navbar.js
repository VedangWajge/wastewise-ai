import React, { useState } from 'react';
import './Navbar.css';

const Navbar = ({ currentView, setCurrentView }) => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  const handleNavClick = (view) => {
    setCurrentView(view);
    setIsMobileMenuOpen(false);
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-brand">
          <h1 className="brand-logo">
            <span className="brand-icon">🌱</span>
            WasteWise
          </h1>
          <p className="brand-tagline">AI-Powered Smart Waste Management</p>
        </div>

        <div className={`navbar-menu ${isMobileMenuOpen ? 'active' : ''}`}>
          <ul className="navbar-nav">
            <li className="nav-item">
              <button
                className={`nav-link ${currentView === 'home' ? 'active' : ''}`}
                onClick={() => handleNavClick('home')}
              >
                <span className="nav-icon">📸</span>
                Classify Waste
              </button>
            </li>
            <li className="nav-item">
              <button
                className={`nav-link ${currentView === 'dashboard' ? 'active' : ''}`}
                onClick={() => handleNavClick('dashboard')}
              >
                <span className="nav-icon">📊</span>
                Dashboard
              </button>
            </li>
            <li className="nav-item">
              <button
                className={`nav-link ${currentView === 'services' ? 'active' : ''}`}
                onClick={() => handleNavClick('services')}
              >
                <span className="nav-icon">🏢</span>
                Services
              </button>
            </li>
            <li className="nav-item">
              <button
                className={`nav-link ${currentView === 'about' ? 'active' : ''}`}
                onClick={() => handleNavClick('about')}
              >
                <span className="nav-icon">ℹ️</span>
                About
              </button>
            </li>
          </ul>
        </div>

        <div className="navbar-toggle" onClick={toggleMobileMenu}>
          <span className="toggle-bar"></span>
          <span className="toggle-bar"></span>
          <span className="toggle-bar"></span>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;