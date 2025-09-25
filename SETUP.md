# 🚀 WasteWise Setup Guide

This guide will help you set up the WasteWise AI-Powered Smart Waste Segregation System on your local machine.

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Node.js** (v14 or higher) - [Download here](https://nodejs.org/)
- **Python** (v3.8 or higher) - [Download here](https://python.org/)
- **Git** - [Download here](https://git-scm.com/)
- **Code Editor** (VS Code recommended) - [Download here](https://code.visualstudio.com/)

## 🔄 Quick Setup (5 minutes)

### Step 1: Clone the Repository
```bash
git clone <your-repository-url>
cd wastewise
```

### Step 2: Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment configuration
cp .env.example .env

# Start the Flask server
python app.py
```

You should see:
```
 * Running on http://localhost:5000
 * Debug mode: on
Database initialized successfully
```

### Step 3: Frontend Setup
Open a **new terminal window**:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start React development server
npm start
```

The browser will automatically open `http://localhost:3000`

## 🎉 Test the Application

1. **Health Check**: Visit `http://localhost:5000/api/health`
2. **Upload Image**: Use the camera or upload feature to classify waste
3. **View Dashboard**: Click on "📊 Dashboard" to see statistics

## 🛠️ Detailed Setup Instructions

### Backend Configuration

#### 1. Environment Setup
```bash
cd backend

# Create virtual environment (isolates Python packages)
python -m venv venv

# Activate virtual environment
# Windows (Command Prompt)
venv\Scripts\activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# macOS/Linux
source venv/bin/activate

# Verify activation (you should see (venv) in your prompt)
which python  # Should point to venv/bin/python
```

#### 2. Install Dependencies
```bash
# Install all required packages
pip install -r requirements.txt

# If you get permission errors, try:
pip install --user -r requirements.txt

# Verify installation
pip list
```

#### 3. Database Initialization
The database will be automatically created when you first run the application. To manually initialize:

```bash
python -c "from models.database import DatabaseManager; DatabaseManager()"
```

#### 4. Test Backend
```bash
# Start Flask development server
python app.py

# In another terminal, test the API
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "message": "Wastewise API is running",
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00"
}
```

### Frontend Configuration

#### 1. Node.js Setup
```bash
cd frontend

# Install dependencies (this may take a few minutes)
npm install

# If you encounter errors, try:
npm install --legacy-peer-deps

# Verify installation
npm list --depth=0
```

#### 2. Environment Configuration
Create `.env` file in frontend directory:
```bash
# frontend/.env
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_MAX_FILE_SIZE=16777216
```

#### 3. Start Development Server
```bash
# Start React development server
npm start

# The browser should automatically open http://localhost:3000
# If not, manually navigate to the URL
```

## 🐛 Troubleshooting

### Common Issues

#### Backend Issues

**1. ModuleNotFoundError: No module named 'flask'**
```bash
# Ensure virtual environment is activated
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

**2. Port 5000 already in use**
```bash
# Kill process using port 5000
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F

# macOS/Linux
lsof -ti:5000 | xargs kill -9

# Or use different port
python -c "import app; app.app.run(port=5001)"
```

**3. Database permission errors**
```bash
# Ensure write permissions in backend directory
chmod 755 backend/
chmod 644 backend/wastewise.db  # if exists
```

**4. OpenCV installation issues**
```bash
# If opencv-python fails to install
pip install opencv-python-headless
# or
pip install --upgrade pip
pip install opencv-python
```

#### Frontend Issues

**1. npm install fails**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

**2. CORS errors**
- Ensure Flask-CORS is installed in backend
- Check that backend is running on port 5000
- Verify API_BASE_URL in frontend/src/services/api.js

**3. Camera not working**
- Use HTTPS for camera access (use browser dev tools)
- Check browser permissions for camera access
- Try the file upload option instead

### Platform-Specific Issues

#### Windows
```bash
# If Scripts\activate doesn't work, try:
venv\Scripts\activate.bat

# PowerShell execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### macOS
```bash
# If you get permission denied:
sudo chown -R $(whoami) /usr/local/lib/node_modules

# Python version issues:
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

#### Linux
```bash
# Install Python dev headers if needed
sudo apt-get update
sudo apt-get install python3-dev python3-pip

# Node.js installation
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

## 🔧 Advanced Configuration

### Production Setup

#### Environment Variables
```bash
# backend/.env
FLASK_ENV=production
DEBUG=False
SECRET_KEY=your-very-secure-secret-key
DATABASE_URL=postgresql://user:password@localhost/wastewise
```

#### Production Server (Gunicorn)
```bash
# Install gunicorn
pip install gunicorn

# Run production server
gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
```

#### Build Frontend for Production
```bash
cd frontend
npm run build

# Serve with static server
npx serve -s build -l 3000
```

### Docker Setup (Optional)

#### Backend Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

#### Docker Compose
```yaml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    volumes:
      - ./backend/uploads:/app/uploads
    environment:
      - FLASK_ENV=production

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
```

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] Backend runs without errors (`http://localhost:5000/api/health`)
- [ ] Frontend loads successfully (`http://localhost:3000`)
- [ ] Image upload works
- [ ] Classification returns results
- [ ] Dashboard displays statistics
- [ ] Database file is created (`backend/wastewise.db`)
- [ ] Upload folder exists (`backend/uploads/`)

## 📚 Next Steps

1. **Customize AI Model**: Replace mock classifier with trained model
2. **Add Features**: Implement additional waste categories
3. **Deploy**: Follow deployment guide for production setup
4. **Monitor**: Set up logging and analytics
5. **Scale**: Add Redis cache, PostgreSQL database

## 🤝 Getting Help

If you encounter issues:

1. Check this troubleshooting guide
2. Review error messages carefully
3. Check GitHub issues for similar problems
4. Open a new issue with:
   - Your operating system
   - Python and Node.js versions
   - Complete error message
   - Steps to reproduce

## 📱 Mobile Testing

To test on mobile devices:

1. Find your computer's IP address:
   ```bash
   # Windows
   ipconfig
   # macOS/Linux
   ifconfig | grep inet
   ```

2. Start servers with host binding:
   ```bash
   # Backend
   python -c "import app; app.app.run(host='0.0.0.0', port=5000)"

   # Frontend
   npm start -- --host 0.0.0.0
   ```

3. Access from mobile: `http://YOUR_IP:3000`

---

**🎉 Congratulations! Your WasteWise application is now ready to use.**

**Happy coding and building a sustainable future! 🌱**