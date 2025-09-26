import React from 'react';
import './Footer.css';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-container">
        <div className="footer-content">
          <div className="footer-section footer-brand">
            <div className="footer-logo">
              <span className="footer-icon">🌱</span>
              <h3>WasteWise</h3>
            </div>
            <p className="footer-description">
              Revolutionizing waste management with AI-powered classification
              and smart disposal solutions. Making the world cleaner, one item at a time.
            </p>
            <div className="footer-social">
              <a href="#" className="social-link" aria-label="Facebook">
                <i className="fab fa-facebook-f"></i>
              </a>
              <a href="#" className="social-link" aria-label="Twitter">
                <i className="fab fa-twitter"></i>
              </a>
              <a href="#" className="social-link" aria-label="Instagram">
                <i className="fab fa-instagram"></i>
              </a>
              <a href="#" className="social-link" aria-label="LinkedIn">
                <i className="fab fa-linkedin-in"></i>
              </a>
            </div>
          </div>

          <div className="footer-section">
            <h4 className="footer-title">Services</h4>
            <ul className="footer-links">
              <li><a href="#" className="footer-link">Waste Classification</a></li>
              <li><a href="#" className="footer-link">Smart Collection</a></li>
              <li><a href="#" className="footer-link">Recycling Services</a></li>
              <li><a href="#" className="footer-link">E-waste Disposal</a></li>
              <li><a href="#" className="footer-link">Bulk Pickup</a></li>
            </ul>
          </div>

          <div className="footer-section">
            <h4 className="footer-title">Company</h4>
            <ul className="footer-links">
              <li><a href="#" className="footer-link">About Us</a></li>
              <li><a href="#" className="footer-link">How It Works</a></li>
              <li><a href="#" className="footer-link">Sustainability</a></li>
              <li><a href="#" className="footer-link">Blog</a></li>
              <li><a href="#" className="footer-link">Careers</a></li>
            </ul>
          </div>

          <div className="footer-section">
            <h4 className="footer-title">Support</h4>
            <ul className="footer-links">
              <li><a href="#" className="footer-link">Help Center</a></li>
              <li><a href="#" className="footer-link">Contact Us</a></li>
              <li><a href="#" className="footer-link">Privacy Policy</a></li>
              <li><a href="#" className="footer-link">Terms of Service</a></li>
              <li><a href="#" className="footer-link">Report Issue</a></li>
            </ul>
          </div>

          <div className="footer-section footer-contact">
            <h4 className="footer-title">Get In Touch</h4>
            <div className="contact-info">
              <div className="contact-item">
                <span className="contact-icon">📧</span>
                <span>hello@wastewise.ai</span>
              </div>
              <div className="contact-item">
                <span className="contact-icon">📞</span>
                <span>+91 99999 99999</span>
              </div>
              <div className="contact-item">
                <span className="contact-icon">📍</span>
                <span>Mumbai, Maharashtra, India</span>
              </div>
            </div>
            <div className="footer-newsletter">
              <p>Subscribe to our newsletter</p>
              <div className="newsletter-form">
                <input
                  type="email"
                  placeholder="Enter your email"
                  className="newsletter-input"
                />
                <button className="newsletter-btn">
                  <span>Subscribe</span>
                  <i className="fas fa-arrow-right"></i>
                </button>
              </div>
            </div>
          </div>
        </div>

        <div className="footer-bottom">
          <div className="footer-bottom-content">
            <p className="copyright">
              © 2024 WasteWise. All rights reserved. | Powered by AI for a sustainable future
            </p>
            <div className="footer-badges">
              <span className="badge">🌿 Carbon Neutral</span>
              <span className="badge">♻️ Zero Waste</span>
              <span className="badge">🤖 AI Powered</span>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;