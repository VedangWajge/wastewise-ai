import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import './Navbar.css';

const Navbar = ({ currentView, setCurrentView }) => {
  const { isAuthenticated, user, logout } = useAuth();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  const handleNavClick = (view) => {
    setCurrentView(view);
    setIsMobileMenuOpen(false);
    setShowUserMenu(false);
    window.location.hash = view;
  };

  const handleLogout = async () => {
    try {
      await logout();
      setCurrentView('home');
      setShowUserMenu(false);
      window.location.hash = '';
    } catch (error) {
      console.error('Logout error:', error);
    }
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
                className={`nav-link ${['home', 'classify'].includes(currentView) ? 'active' : ''}`}
                onClick={() => handleNavClick('home')}
              >
                <span className="nav-icon">📸</span>
                Classify
              </button>
            </li>
            {isAuthenticated && (
              <>
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
                    className={`nav-link ${currentView === 'bookings' ? 'active' : ''}`}
                    onClick={() => handleNavClick('bookings')}
                  >
                    <span className="nav-icon">📅</span>
                    Bookings
                  </button>
                </li>
                <li className="nav-item">
                  <button
                    className={`nav-link ${currentView === 'rewards' ? 'active' : ''}`}
                    onClick={() => handleNavClick('rewards')}
                  >
                    <span className="nav-icon">🎁</span>
                    Rewards
                  </button>
                </li>
                <li className="nav-item">
                  <button
                    className={`nav-link ${currentView === 'analytics' ? 'active' : ''}`}
                    onClick={() => handleNavClick('analytics')}
                  >
                    <span className="nav-icon">📈</span>
                    Analytics
                  </button>
                </li>
              </>
            )}
            <li className="nav-item">
              <button
                className={`nav-link ${currentView === 'marketplace' ? 'active' : ''}`}
                onClick={() => handleNavClick('marketplace')}
              >
                <span className="nav-icon">🛒</span>
                Marketplace
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
          </ul>

          {isAuthenticated ? (
            <div className="user-menu">
              <button
                className="user-button"
                onClick={() => setShowUserMenu(!showUserMenu)}
              >
                <span className="user-avatar">👤</span>
                <span className="user-name">{user?.full_name || 'User'}</span>
                <span className="dropdown-arrow">▼</span>
              </button>
              {showUserMenu && (
                <div className="user-dropdown">
                  <div className="user-info">
                    <span className="user-email">{user?.email}</span>
                    <span className="user-role">{user?.role}</span>
                  </div>
                  <div className="dropdown-divider"></div>
                  <button
                    className="dropdown-item"
                    onClick={() => handleNavClick('profile')}
                  >
                    <span className="item-icon">👤</span>
                    Profile
                  </button>
                  <button
                    className="dropdown-item"
                    onClick={() => handleNavClick('payment')}
                  >
                    <span className="item-icon">💳</span>
                    Payments
                  </button>
                  <div className="dropdown-divider"></div>
                  <button
                    className="dropdown-item logout"
                    onClick={handleLogout}
                  >
                    <span className="item-icon">🚪</span>
                    Logout
                  </button>
                </div>
              )}
            </div>
          ) : (
            <div className="auth-buttons">
              <button
                className="auth-btn login"
                onClick={() => handleNavClick('login')}
              >
                Login
              </button>
              <button
                className="auth-btn register"
                onClick={() => handleNavClick('register')}
              >
                Sign Up
              </button>
            </div>
          )}
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