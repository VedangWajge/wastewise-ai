# 🚀 WasteWise Multi-Platform Development Guide

## 🎯 Overview
This guide explains how to run both **Web (React)** and **Mobile (React Native)** applications simultaneously, both connected to the same Flask backend server.

---

## ⚡ Quick Start

### 🖥️ **Windows Users**
```bash
# 1. Start all services at once
start-all.bat

# 2. Connect mobile device (in separate terminal)
start-mobile.bat
```

### 🍎 **Mac/Linux Users**
```bash
# 1. Start all services at once
./start-all.sh

# 2. Connect mobile device (in separate terminal)
./start-mobile.sh
```

---

## 📋 **Step-by-Step Setup**

### **1. Network Configuration**

#### **Find Your Computer's IP Address**
```bash
# Windows
ipconfig

# Mac/Linux
ifconfig
# or
ip addr show
```

#### **Update Mobile App Configuration**
Edit `mobile-app/src/services/ApiService.js`:
```javascript
// Replace with YOUR computer's IP address
const API_BASE_URL = 'http://YOUR_IP:5000/api';
// Example: const API_BASE_URL = 'http://192.168.1.2:5000/api';
```

### **2. Backend Server Setup**

#### **Start Flask Backend**
```bash
cd backend
venv\Scripts\activate    # Windows
source venv/bin/activate # Mac/Linux
python app.py
```
✅ **Server will run on:** `http://0.0.0.0:5000` (accessible from mobile devices)

### **3. Frontend Web Setup**

#### **Start React Web App**
```bash
cd frontend
npm start
```
✅ **Web app opens at:** `http://localhost:3000`

### **4. Mobile App Setup**

#### **Start Metro Bundler**
```bash
cd mobile-app
npm start
```

#### **Connect Physical Device**
```bash
# Android
npx react-native run-android

# iOS (macOS only)
npx react-native run-ios
```

#### **Use Emulator/Simulator**
```bash
# Android Emulator
npx react-native run-android

# iOS Simulator (macOS only)
npx react-native run-ios
```

---

## 🔗 **API Endpoints**

| Platform | Backend URL | Purpose |
|----------|-------------|---------|
| **Web** | `http://localhost:5000/api` | Local development |
| **Mobile** | `http://YOUR_IP:5000/api` | Network access |
| **Android Emulator** | `http://10.0.2.2:5000/api` | Emulator bridge |
| **iOS Simulator** | `http://127.0.0.1:5000/api` | Localhost |

---

## 🧪 **Testing Connectivity**

### **1. Web Browser Test**
Open: `http://localhost:5000/api/health`

### **2. Mobile Browser Test**
Open on phone: `http://YOUR_IP:5000/api/health`

### **3. Network Test Endpoints**
- `/api/health` - Basic server status
- `/api/network-test` - Mobile connectivity test
- `/api/cors-test` - CORS configuration test

### **4. Mobile App Test**
Use the built-in connectivity test in your mobile app:
```javascript
import ApiService from './services/ApiService';

// Run full connectivity test
const results = await ApiService.fullConnectivityTest();
console.log(results);
```

---

## 🔧 **Development Workflow**

### **Terminal Layout**
```
Terminal 1: Backend Server
├── cd backend && python app.py
└── 🟢 Running on http://0.0.0.0:5000

Terminal 2: Web Frontend
├── cd frontend && npm start
└── 🟢 Available at http://localhost:3000

Terminal 3: Mobile Metro
├── cd mobile-app && npm start
└── 🟢 Metro Bundler running

Terminal 4: Mobile Device
├── npx react-native run-android
└── 🟢 App installed on device
```

### **Shared Development Benefits**
- ✅ **Single Backend:** Both apps use same API endpoints
- ✅ **Shared Sessions:** User actions sync across platforms
- ✅ **Real-time Updates:** Backend changes affect both apps instantly
- ✅ **Consistent Data:** Same AI models and service providers
- ✅ **Cross-platform Testing:** Validate features on both platforms

### **Development Features**
- 📱 **Mobile:** Camera, GPS, push notifications, native UI
- 🌐 **Web:** Responsive design, PWA features, desktop-optimized
- 🤖 **AI Backend:** Waste classification, service discovery, analytics
- 📊 **Shared Data:** Statistics, bookings, user preferences

---

## 🚨 **Troubleshooting**

### **Connection Issues**

#### **Mobile can't connect to backend:**
```bash
# 1. Check IP address
ipconfig  # Windows
ifconfig  # Mac/Linux

# 2. Test from phone browser
http://YOUR_IP:5000/api/health

# 3. Check Windows Firewall
# Allow Python.exe through firewall

# 4. Verify same WiFi network
# Both devices must be on same network
```

#### **CORS Errors:**
Flask CORS is pre-configured, but if issues persist:
```python
# In backend/app.py
from flask_cors import CORS
app = Flask(__name__)
CORS(app, origins=['*'])  # Allow all origins for development
```

#### **Metro Bundler Issues:**
```bash
# Clear cache
npx react-native start --reset-cache

# Reinstall dependencies
rm -rf node_modules && npm install
```

#### **Device Not Found:**
```bash
# Check Android devices
adb devices

# Check iOS simulators (macOS)
xcrun simctl list devices
```

### **Build Issues**

#### **Android Build Errors:**
```bash
cd mobile-app/android
./gradlew clean    # Windows: gradlew.bat clean
cd ..
npx react-native run-android
```

#### **iOS Build Errors (macOS):**
```bash
cd mobile-app/ios
pod install
cd ..
npx react-native run-ios
```

---

## 📱 **Device-Specific Configuration**

### **Android Physical Device**
1. Enable **Developer Options**
2. Enable **USB Debugging**
3. Enable **Install via USB**
4. Connect via USB cable
5. Allow USB debugging prompt

### **Android Emulator**
1. Start Android Studio → AVD Manager
2. Create/Start virtual device
3. API Config: `http://10.0.2.2:5000/api`

### **iOS Physical Device (macOS)**
1. Connect via USB/WiFi
2. Trust computer when prompted
3. Ensure same Apple ID in Xcode

### **iOS Simulator (macOS)**
1. Install Xcode
2. API Config: `http://127.0.0.1:5000/api` or `http://localhost:5000/api`

---

## 🎯 **Production Deployment**

### **Environment Variables**
```javascript
// mobile-app/src/config/environment.js
const config = {
  development: {
    API_BASE_URL: 'http://192.168.1.2:5000/api'
  },
  production: {
    API_BASE_URL: 'https://your-production-api.com/api'
  }
};
```

### **Build for Production**
```bash
# Web Build
cd frontend && npm run build

# Android APK
cd mobile-app/android && ./gradlew assembleRelease

# iOS Archive (macOS)
cd mobile-app && npx react-native run-ios --configuration Release
```

---

## 📊 **Development Metrics**

### **Expected Performance**
- **Backend Response Time:** < 200ms (local network)
- **Image Classification:** 2-5 seconds
- **App Launch Time:** 2-3 seconds
- **Network Requests:** < 1 second (same WiFi)

### **Resource Usage**
- **Backend RAM:** ~100-200MB
- **Web Frontend:** ~50-100MB
- **Mobile App:** ~150-300MB
- **Development Setup:** ~4 terminal windows

---

## 🎉 **Demo Preparation**

### **Pre-Demo Checklist**
- [ ] All services running (`start-all.bat/sh`)
- [ ] Mobile device connected and tested
- [ ] Sample waste images ready
- [ ] Network connectivity verified
- [ ] Both web and mobile apps tested
- [ ] AI classification working
- [ ] Service discovery functional

### **Demo Flow**
1. **Web App:** Show AI classification on computer
2. **Mobile App:** Demonstrate same feature on phone
3. **Cross-Platform:** Show data syncing between both
4. **Features:** Camera, GPS, services, bookings
5. **Backend:** Explain shared API and AI models

---

## ✨ **Advanced Features**

### **Real-time Sync**
Both apps share the same backend sessions, so:
- Classifications appear in both apps
- Bookings sync across platforms
- Statistics update in real-time
- User preferences persist

### **Platform-Specific Features**
- **Mobile:** Camera, GPS, push notifications
- **Web:** File upload, desktop optimizations, keyboard shortcuts
- **Shared:** AI classification, service discovery, analytics

---

**🎯 Your WasteWise project now supports full cross-platform development with shared backend intelligence!**