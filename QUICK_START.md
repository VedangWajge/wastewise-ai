# 🚀 WasteWise - Quick Start Reference

## ⚡ One-Command Setup
```bash
# Windows (from project root)
start-all.bat

# This automatically starts:
# ✅ Backend server (http://localhost:5000)
# ✅ Frontend web app (http://localhost:3000)
# ✅ Mobile Metro bundler (if needed)
```

## 🛠 Manual Setup (if needed)

### First Time Setup
```bash
# 1. Backend setup
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env

# 2. Frontend setup
cd frontend
npm install

# 3. Start servers
cd backend && venv\Scripts\activate && python app.py
cd frontend && npm start
```

## 📂 Key Directories for Team

### **Frontend Developer** 👨‍💻
```bash
frontend/src/
├── components/     # React components (your main work area)
├── services/api.js # API calls to backend
├── App.js         # Main app logic
└── *.css          # Styling files
```

### **Backend Developer** ⚙️
```bash
backend/
├── app.py              # Main Flask app
├── routes/             # API endpoints
├── models/database.py  # Database operations
├── models/user_manager.py # User auth
└── utils/              # Helper functions
```

### **Mobile Developer** 📱
```bash
mobile-app/
├── App.js          # Main mobile app
├── components/     # Mobile components
└── services/       # API integration
```

## 🔄 Daily Workflow

### 1. Start Development
```bash
git pull origin main        # Get latest changes
start-all.bat              # Start all servers
```

### 2. Create New Feature
```bash
git checkout -b feature/your-feature-name
# Make your changes
git add .
git commit -m "feat: description"
git push origin feature/your-feature-name
```

### 3. Common Commands
```bash
# Check if servers are running
netstat -ano | findstr :3000    # Frontend
netstat -ano | findstr :5000    # Backend

# Restart if needed
Ctrl+C in server terminals
start-all.bat

# Install new packages
cd frontend && npm install package-name
cd backend && pip install package-name
```

## 🐛 Quick Fixes

### Server Not Starting?
```bash
# Check ports
netstat -ano | findstr :3000
netstat -ano | findstr :5000

# Kill if occupied
taskkill /PID <process_id> /F

# Restart
start-all.bat
```

### Database Issues?
```bash
# Delete and recreate database
cd backend
del wastewise.db
python app.py    # Will recreate database
```

### Package Issues?
```bash
# Frontend
cd frontend
del package-lock.json
rmdir /s node_modules
npm install

# Backend
cd backend
pip install --upgrade pip
pip install -r requirements.txt
```

## 📋 URLs & Ports

- **Frontend Web App**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **API Documentation**: http://localhost:5000/api/docs
- **Database**: backend/wastewise.db (SQLite file)

## 💡 Development Tips

1. **Keep servers running** - Use `start-all.bat` for convenience
2. **Check browser console** - Look for JavaScript errors
3. **Check backend terminal** - Look for Python errors
4. **Use browser dev tools** - Network tab for API calls
5. **Test API endpoints** - Use Postman or browser

## 🚨 Emergency Contacts

- **Git Issues**: [Team Lead Name]
- **Backend Issues**: [Backend Developer]
- **Frontend Issues**: [Frontend Developer]
- **Mobile Issues**: [Mobile Developer]

---

**Quick Help**: Run `start-all.bat` and visit http://localhost:3000 🚀