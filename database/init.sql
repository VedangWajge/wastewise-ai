-- WasteWise Database Schema
-- Initialize database for waste classification tracking

CREATE DATABASE IF NOT EXISTS wastewise_db;
USE wastewise_db;

-- Classifications table to store all waste classification results
CREATE TABLE classifications (
    id INT PRIMARY KEY AUTO_INCREMENT,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255),
    waste_type VARCHAR(50) NOT NULL,
    confidence DECIMAL(4,3) NOT NULL,
    image_path VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Waste categories table for reference data
CREATE TABLE waste_categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    category_name VARCHAR(50) UNIQUE NOT NULL,
    icon VARCHAR(10),
    color_code VARCHAR(7),
    description TEXT,
    disposal_instructions TEXT,
    environmental_impact TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User sessions table for tracking usage (optional)
CREATE TABLE user_sessions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    session_id VARCHAR(100) UNIQUE NOT NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    first_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    classification_count INT DEFAULT 0
);

-- Statistics view for dashboard
CREATE VIEW waste_statistics AS
SELECT
    waste_type,
    COUNT(*) as count,
    AVG(confidence) as avg_confidence,
    MIN(created_at) as first_classification,
    MAX(created_at) as last_classification
FROM classifications
GROUP BY waste_type;

-- Insert default waste categories
INSERT INTO waste_categories (category_name, icon, color_code, description, disposal_instructions, environmental_impact) VALUES
('plastic', '♻️', '#2196f3', 'Synthetic materials that can be recycled', 'Place in recycling bin, clean before disposal, remove labels', 'High recyclability - can be processed into new products'),
('organic', '🌱', '#4caf50', 'Biodegradable waste from living organisms', 'Compost this waste, use for organic fertilizer, dispose in green bin', 'Can be composted to create nutrient-rich soil'),
('paper', '📄', '#ff9800', 'Paper-based materials and cardboard', 'Place in paper recycling, remove plastic coating, ensure clean and dry', 'Easily recyclable - saves trees and reduces landfill waste'),
('glass', '🗞️', '#00bcd4', 'Glass containers and materials', 'Place in glass recycling bin, remove caps and lids, handle with care', '100% recyclable without quality loss'),
('metal', '🔧', '#607d8b', 'Metallic materials and containers', 'Place in metal recycling, clean any food residue, infinitely recyclable', 'Infinitely recyclable - high environmental value');

-- Create indexes for better performance
CREATE INDEX idx_classifications_waste_type ON classifications(waste_type);
CREATE INDEX idx_classifications_created_at ON classifications(created_at);
CREATE INDEX idx_user_sessions_session_id ON user_sessions(session_id);
CREATE INDEX idx_user_sessions_last_activity ON user_sessions(last_activity);