# 🚀 WasteWise - Complete Team Setup Guide

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Prerequisites](#prerequisites)
3. [Initial Setup](#initial-setup)
4. [Project Structure](#project-structure)
5. [Environment Configuration](#environment-configuration)
6. [Running the Application](#running-the-application)
7. [Development Workflow](#development-workflow)
8. [Architecture & Data Flow](#architecture--data-flow)
9. [Static vs Dynamic Components](#static-vs-dynamic-components)
10. [Team Collaboration](#team-collaboration)
11. [Troubleshooting](#troubleshooting)
12. [Deployment](#deployment)

---

## 🎯 Project Overview

**WasteWise** is a full-stack waste classification and management system with:
- **Frontend**: React.js web application (Port 3000)
- **Backend**: Flask Python API server (Port 5000)
- **Database**: SQLite for development
- **Mobile**: React Native app
- **AI/ML**: TensorFlow waste classification model

### Key Features
- Image-based waste classification using AI
- User authentication and management
- Booking system for waste collection services
- Rewards and analytics system
- Payment processing integration

---

## ✅ Prerequisites

### Required Software
```bash
# Essential Tools
- Node.js (v16 or higher)
- Python (3.8 or higher)
- Git
- VS Code or preferred IDE

# For Mobile Development (Optional)
- Android Studio (for Android)
- Xcode (for iOS - Mac only)
```

### System Requirements
- **Windows**: Windows 10/11
- **RAM**: Minimum 8GB (16GB recommended)
- **Storage**: 5GB free space
- **Internet**: Required for package installation

---

## 🛠 Initial Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd wastewise
```

### 2. Backend Setup (Python/Flask)
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
copy .env.example .env
# Edit .env with your configurations
```

### 3. Frontend Setup (React)
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Verify installation
npm start
```

### 4. Database Setup
```bash
# The SQLite database will be automatically created when you first run the backend
# Location: backend/wastewise.db
```

---

## 📁 Project Structure

```
wastewise/
├── 📂 backend/                 # Python Flask API
│   ├── 📂 config/             # Configuration files
│   ├── 📂 models/             # Database models
│   │   ├── database.py        # Classification data manager
│   │   └── user_manager.py    # User authentication manager
│   ├── 📂 routes/             # API endpoints
│   ├── 📂 utils/              # Utility functions
│   ├── 📂 uploads/            # User uploaded images
│   ├── 📂 venv/               # Python virtual environment
│   ├── app.py                 # Main Flask application
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Environment variables
│
├── 📂 frontend/               # React web application
│   ├── 📂 public/             # Static assets
│   ├── 📂 src/
│   │   ├── 📂 components/     # React components
│   │   │   ├── 📂 Auth/       # Login/Register components
│   │   │   ├── 📂 Bookings/   # Booking management
│   │   │   ├── 📂 Payment/    # Payment processing
│   │   │   ├── 📂 Rewards/    # Rewards system
│   │   │   └── 📂 Analytics/  # Analytics dashboard
│   │   ├── 📂 contexts/       # React context providers
│   │   ├── 📂 services/       # API service calls
│   │   └── App.js             # Main React component
│   ├── package.json           # Node.js dependencies
│   └── package-lock.json      # Dependency lock file
│
├── 📂 mobile-app/             # React Native mobile app
├── 📂 models/                 # AI/ML model files
├── 📂 database/               # Database schema files
├── start-all.bat             # Quick start script (Windows)
└── README.md                 # Project documentation
```

---

## ⚙️ Environment Configuration

### Backend Environment (.env)
```bash
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-super-secret-key-here
DEBUG=True

# Database Configuration
DATABASE_URL=sqlite:///wastewise.db
DATABASE_PATH=wastewise.db

# File Upload Configuration
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216  # 16MB
ALLOWED_EXTENSIONS=png,jpg,jpeg,gif

# AI Model Configuration
MODEL_PATH=models/waste_classifier.h5
CONFIDENCE_THRESHOLD=0.6
USE_MOCK_CLASSIFIER=True  # Set to False when real model is ready

# CORS Configuration
CORS_ORIGINS=http://localhost:3000

# Server Configuration
HOST=localhost
PORT=5000
```

### Frontend Configuration
```javascript
// API endpoints are configured in src/services/api.js
const API_BASE_URL = 'http://localhost:5000/api';
```

---

## 🚀 Running the Application

### Option 1: Quick Start (Windows)
```bash
# From project root directory
start-all.bat
```
This will automatically start:
- Backend server on http://localhost:5000
- Frontend server on http://localhost:3000
- Mobile Metro bundler (if mobile-app exists)

### Option 2: Manual Start

#### Start Backend
```bash
cd backend
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
python app.py
```

#### Start Frontend
```bash
cd frontend
npm start
```

### Option 3: Development Mode
```bash
# Terminal 1: Backend with auto-reload
cd backend
venv\Scripts\activate
flask run --debug

# Terminal 2: Frontend with hot-reload
cd frontend
npm start
```

---

## 🔄 Development Workflow

### Daily Development Process
1. **Pull latest changes**
   ```bash
   git pull origin main
   ```

2. **Create feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Start development servers**
   ```bash
   # Use start-all.bat or manual start
   ```

4. **Make your changes**
   - Frontend: Edit files in `frontend/src/`
   - Backend: Edit files in `backend/`

5. **Test your changes**
   ```bash
   # Test frontend
   cd frontend && npm test

   # Test backend
   cd backend && python -m pytest
   ```

6. **Commit and push**
   ```bash
   git add .
   git commit -m "feat: your feature description"
   git push origin feature/your-feature-name
   ```

---

## 🏗 Architecture & Data Flow

### System Architecture
```
[Frontend React App] ←→ [Flask API Server] ←→ [SQLite Database]
      ↓                        ↓                      ↓
  - User Interface        - Business Logic        - Data Storage
  - State Management      - Authentication        - Classifications
  - API Calls            - File Processing       - User Data
  - Routing              - AI Integration        - Session Data
```

### Data Flow
1. **Image Upload Flow**
   ```
   User uploads image → Frontend sends to API → Backend processes with AI →
   Classification result stored in DB → Response sent to Frontend →
   User sees classification result
   ```

2. **Authentication Flow**
   ```
   User login → Frontend sends credentials → Backend validates →
   JWT token generated → Token stored in Frontend →
   Protected routes accessible
   ```

3. **Booking Flow**
   ```
   User selects service → Booking form filled → Backend creates booking →
   Database stores booking → Email notification sent →
   Booking confirmation displayed
   ```

### API Endpoints Structure
```
/api/
├── /auth/                     # Authentication
│   ├── POST /login
│   ├── POST /register
│   └── POST /logout
├── /classify/                 # Waste Classification
│   └── POST /upload
├── /services/                 # Service Discovery
│   └── GET /nearby
├── /bookings/                # Booking Management
│   ├── GET /
│   ├── POST /create
│   └── PUT /:id
├── /users/                   # User Management
│   ├── GET /profile
│   └── PUT /profile
└── /admin/                   # Admin Functions
    ├── GET /stats
    └── GET /users
```

---

## 📊 Static vs Dynamic Components

### Static Components (Pre-built, rarely change)
```javascript
// Frontend Static Components
├── Navbar.js                 # Navigation bar
├── Footer.js                 # Footer component
├── Camera.js                 # Image capture interface
├── Dashboard.js              # Main dashboard layout
└── Auth/
    ├── Login.js              # Login form
    └── Register.js           # Registration form

// Backend Static Components
├── config/settings.py        # Configuration settings
├── utils/validators.py       # Input validation functions
└── routes/admin.py          # Admin endpoints (mostly static)
```

### Dynamic Components (Frequently updated/modified)
```javascript
// Frontend Dynamic Components
├── Classification.js         # Shows AI classification results
├── ServiceDiscovery.js      # Service listing (varies by location)
├── BookingForm.js           # Booking creation (varies by service)
├── BookingManagement.js     # User bookings (varies by user)
├── Rewards/                 # User rewards and points
├── Payment/                 # Payment processing
└── Analytics/               # Statistics and charts

// Backend Dynamic Components
├── models/database.py       # Database operations
├── models/user_manager.py   # User data management
├── routes/bookings.py       # Booking logic
├── routes/payments.py       # Payment processing
└── app.py                   # Main application logic
```

### Database Tables (Dynamic Data)
```sql
-- Dynamic Tables (content changes frequently)
├── classifications          # AI classification results
├── users                   # User account data
├── bookings               # Waste collection bookings
├── user_sessions          # Active user sessions
├── payments               # Payment transactions
└── rewards                # User rewards and points

-- Static/Reference Tables (rarely change)
├── waste_categories       # Waste type definitions
├── services              # Available services
└── service_providers     # Company information
```

---

## 👥 Team Collaboration

### Role-Based Development Areas

#### **Frontend Developer**
**Focus Areas:**
- `frontend/src/components/` - React components
- `frontend/src/services/api.js` - API integration
- `frontend/src/App.js` - Main application logic
- CSS styling and responsive design

**Key Files to Work On:**
- User interface components
- State management
- API service calls
- Responsive design implementation

#### **Backend Developer**
**Focus Areas:**
- `backend/app.py` - Main Flask application
- `backend/routes/` - API endpoints
- `backend/models/` - Database operations
- Authentication and security

**Key Files to Work On:**
- API endpoint development
- Database schema and operations
- Authentication logic
- File upload and processing

#### **Mobile Developer**
**Focus Areas:**
- `mobile-app/` - React Native application
- Mobile-specific UI components
- Device camera integration
- Push notifications

**Key Files to Work On:**
- Mobile app components
- Navigation structure
- Camera functionality
- Mobile-specific API calls

### Git Workflow for Teams
```bash
# Branch naming convention
feature/feature-name         # New features
bugfix/bug-description      # Bug fixes
hotfix/critical-fix         # Critical fixes
improvement/enhancement     # Improvements

# Example workflow
git checkout main
git pull origin main
git checkout -b feature/user-profile
# Make changes
git add .
git commit -m "feat: add user profile editing"
git push origin feature/user-profile
# Create pull request
```

### Code Review Guidelines
1. **All changes require code review**
2. **Test your changes before pushing**
3. **Follow existing code style**
4. **Update documentation for new features**
5. **Use meaningful commit messages**

---

## 🔧 Troubleshooting

### Common Setup Issues

#### Backend Issues
```bash
# Virtual environment activation fails
Problem: 'venv\Scripts\activate' is not recognized
Solution:
cd backend
python -m venv venv
venv\Scripts\activate.bat

# Package installation fails
Problem: pip install fails
Solution:
python -m pip install --upgrade pip
pip install -r requirements.txt

# Database connection issues
Problem: SQLite database errors
Solution:
Delete existing wastewise.db file
Restart backend server to recreate database
```

#### Frontend Issues
```bash
# Node modules installation fails
Problem: npm install fails
Solution:
Delete node_modules folder
Delete package-lock.json
npm cache clean --force
npm install

# Port already in use
Problem: Port 3000 already in use
Solution:
netstat -ano | findstr :3000
taskkill /PID <process_id> /F
npm start

# API connection issues
Problem: Cannot connect to backend
Solution:
Check backend is running on port 5000
Verify CORS settings in backend
Check API_BASE_URL in frontend
```

#### Database Issues
```bash
# Database file permissions
Problem: SQLite permission denied
Solution:
Check file permissions on wastewise.db
Run command prompt as administrator
Ensure backend folder is writable

# Database schema outdated
Problem: Database table errors
Solution:
Backup existing database
Delete wastewise.db
Restart backend to recreate with latest schema
```

### Performance Issues
```bash
# Slow development server
Solution:
Close unnecessary browser tabs
Restart development servers
Check system memory usage
Clear browser cache

# Large bundle size
Solution:
Run npm run build to check production size
Use React DevTools to identify large components
Optimize images and assets
```

---

## 🚀 Deployment

### Development Deployment
```bash
# Local development
npm start (frontend)
python app.py (backend)

# Local production testing
npm run build (frontend)
serve -s build (serve frontend)
gunicorn app:app (backend)
```

### Production Deployment Options

#### Option 1: Traditional Server
```bash
# Frontend (Build for production)
cd frontend
npm run build
# Deploy build folder to web server

# Backend (Use production WSGI server)
cd backend
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

#### Option 2: Docker Deployment
```dockerfile
# Create Dockerfile for backend
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

# Create Dockerfile for frontend
FROM node:16
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
CMD ["npm", "start"]
```

### Environment Variables for Production
```bash
# Production .env
FLASK_ENV=production
DEBUG=False
DATABASE_URL=postgresql://user:pass@localhost/wastewise_prod
SECRET_KEY=very-secure-production-key
CORS_ORIGINS=https://yourdomain.com
```

---

## 📚 Additional Resources

### Documentation Links
- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://reactjs.org/docs/)
- [SQLite Documentation](https://sqlite.org/docs.html)
- [TensorFlow Documentation](https://tensorflow.org/guide)

### Development Tools
- **API Testing**: Postman or Thunder Client
- **Database Viewer**: DB Browser for SQLite
- **Git Client**: GitHub Desktop or command line
- **Code Editor**: VS Code with Python and JavaScript extensions

### Team Communication
- **Daily Standups**: Discuss progress and blockers
- **Code Reviews**: Use GitHub pull requests
- **Documentation**: Keep this guide updated
- **Issue Tracking**: Use GitHub Issues

---

## 🎯 Quick Reference Commands

```bash
# Start development environment
start-all.bat                 # Windows quick start

# Manual startup
cd backend && venv\Scripts\activate && python app.py
cd frontend && npm start

# Git workflow
git checkout -b feature/name   # Create new branch
git add . && git commit -m ""  # Commit changes
git push origin feature/name   # Push to remote

# Package management
pip install package-name       # Backend dependencies
npm install package-name       # Frontend dependencies

# Database operations
python -c "from models.database import DatabaseManager; DatabaseManager()"

# Testing
npm test                       # Frontend tests
python -m pytest             # Backend tests
```

---

**Happy Coding! 🚀**

*Last Updated: [Date]*
*Version: 1.0*