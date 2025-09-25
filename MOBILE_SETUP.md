# 📱 WasteWise Mobile App Setup & Testing Guide

## 🎯 **Overview**
This guide will help you set up, test, and install the WasteWise mobile app on your phone, and connect it to the backend server.

---

## 🛠️ **Prerequisites**

### **For Development:**
- Node.js (v14 or higher)
- React Native CLI
- Android Studio (for Android) or Xcode (for iOS on macOS)
- Your computer and phone on the same WiFi network

### **For Your Phone:**
- Android 6.0+ or iOS 10+
- Developer options enabled (Android)
- USB cable for initial setup

---

## 🔧 **Step 1: Backend Setup for Mobile**

### **1.1 Update Backend for Mobile Access**

First, let's modify the Flask app to accept connections from your phone:

```bash
# Navigate to backend
cd wastewise/backend

# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
```

**Edit `backend/app.py`** - Change the last line:

```python
# OLD:
if __name__ == '__main__':
    app.run(debug=True, port=5000)

# NEW:
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

### **1.2 Find Your Computer's IP Address**

**Windows:**
```cmd
ipconfig
# Look for "IPv4 Address" under your WiFi adapter
# Example: 192.168.1.105
```

**macOS/Linux:**
```bash
ifconfig | grep inet
# Look for your local IP (usually 192.168.x.x or 10.0.x.x)
```

**Alternative Method:**
- Open Command Prompt/Terminal
- Run: `ping $(hostname)` and note the IP address

### **1.3 Update Mobile App API Configuration**

**Edit `mobile-app/src/services/ApiService.js`** - Line 6:

```javascript
// OLD:
const API_BASE_URL = 'http://192.168.1.100:5000/api';

// NEW (replace with YOUR computer's IP):
const API_BASE_URL = 'http://YOUR_COMPUTER_IP:5000/api';
// Example: const API_BASE_URL = 'http://192.168.1.105:5000/api';
```

---

## 📱 **Step 2: Mobile App Development Setup**

### **2.1 Install React Native CLI**
```bash
npm install -g react-native-cli
# OR
npm install -g @react-native-community/cli
```

### **2.2 Setup for Android**

#### **Install Android Studio:**
1. Download from https://developer.android.com/studio
2. Install with default settings
3. Open Android Studio → SDK Manager
4. Install Android SDK (API level 29 or higher)

#### **Setup Environment Variables:**
**Windows:**
```cmd
# Add to System Environment Variables:
ANDROID_HOME = C:\Users\YourUsername\AppData\Local\Android\Sdk
# Add to PATH:
C:\Users\YourUsername\AppData\Local\Android\Sdk\platform-tools
```

**macOS/Linux:**
```bash
# Add to ~/.bashrc or ~/.zshrc:
export ANDROID_HOME=$HOME/Library/Android/sdk
export PATH=$PATH:$ANDROID_HOME/emulator
export PATH=$PATH:$ANDROID_HOME/platform-tools
```

#### **Enable Developer Options on Phone:**
1. Go to **Settings** → **About Phone**
2. Tap **Build Number** 7 times
3. Go back to **Settings** → **Developer Options**
4. Enable **USB Debugging**
5. Enable **Install via USB**

### **2.3 Setup for iOS (macOS only)**

#### **Install Xcode:**
1. Download from Mac App Store
2. Install Xcode Command Line Tools:
```bash
xcode-select --install
```

#### **Install CocoaPods:**
```bash
sudo gem install cocoapods
```

---

## 🚀 **Step 3: Running the Mobile App**

### **3.1 Install Dependencies**
```bash
cd wastewise/mobile-app
npm install

# For iOS only (macOS):
cd ios && pod install && cd ..
```

### **3.2 Start Metro Bundler**
```bash
# In mobile-app directory
npm start
# OR
npx react-native start
```

### **3.3 Run on Android**

#### **Method 1: Physical Device**
```bash
# Connect phone via USB
# Ensure USB debugging is enabled
adb devices  # Should show your device

# Run the app
npx react-native run-android
```

#### **Method 2: Android Emulator**
```bash
# Start Android Studio → AVD Manager → Create Virtual Device
# Start the emulator, then:
npx react-native run-android
```

### **3.4 Run on iOS (macOS only)**
```bash
npx react-native run-ios
# OR for specific device:
npx react-native run-ios --device "Your iPhone Name"
```

---

## 📋 **Step 4: Testing the Connection**

### **4.1 Test Backend Connectivity**

**Start Backend:**
```bash
# Terminal 1: Backend
cd wastewise/backend
python app.py
# Should show: Running on http://0.0.0.0:5000
```

**Test API from Phone's Browser:**
1. Open browser on your phone
2. Navigate to: `http://YOUR_COMPUTER_IP:5000/api/health`
3. Should see: `{"status": "healthy", "message": "Wastewise API is running"}`

### **4.2 Test Mobile App Features**

**Launch Mobile App:**
1. App should start without errors
2. Check console for API connection messages

**Test Core Features:**
- [ ] **Home Screen**: Loads with statistics
- [ ] **Camera**: Takes photos successfully
- [ ] **Location**: Gets GPS coordinates
- [ ] **Service Discovery**: Loads service providers
- [ ] **API Calls**: No network errors in console

---

## 📦 **Step 5: Installing APK on Android Phone**

### **5.1 Build Release APK**
```bash
cd mobile-app/android

# Build release APK
./gradlew assembleRelease
# Windows: gradlew.bat assembleRelease

# APK will be created at:
# android/app/build/outputs/apk/release/app-release.apk
```

### **5.2 Install APK on Phone**

#### **Method 1: USB Installation**
```bash
# Copy APK to phone and install via file manager
adb install android/app/build/outputs/apk/release/app-release.apk
```

#### **Method 2: Direct Transfer**
1. Copy `app-release.apk` to phone storage
2. Open file manager on phone
3. Tap the APK file
4. Enable "Install from unknown sources" if prompted
5. Install the app

### **5.3 Configure App on Phone**

After installing, the app will try to connect to your backend. Ensure:
1. **Same WiFi**: Phone and computer on same network
2. **Firewall**: Windows Firewall allows Python app
3. **Backend Running**: Flask server is active
4. **Correct IP**: App has your computer's IP address

---

## 🔧 **Troubleshooting Common Issues**

### **Backend Connection Issues**

#### **Problem**: App can't connect to backend
**Solutions:**
1. **Check IP Address:**
   ```bash
   # Test from phone browser:
   http://YOUR_IP:5000/api/health
   ```

2. **Windows Firewall:**
   - Go to Windows Security → Firewall
   - Allow Python.exe through firewall
   - OR temporarily disable firewall for testing

3. **Router Settings:**
   - Ensure both devices on same WiFi
   - Some routers block device-to-device communication

#### **Problem**: CORS errors
**Solution:**
```python
# In backend/app.py, ensure CORS is configured:
from flask_cors import CORS
app = Flask(__name__)
CORS(app)  # This should already be there
```

### **Mobile App Build Issues**

#### **Android Build Errors:**
```bash
# Clean and rebuild
cd android
./gradlew clean
cd ..
npx react-native run-android
```

#### **Metro Bundler Issues:**
```bash
# Reset Metro cache
npx react-native start --reset-cache
```

#### **Node Modules Issues:**
```bash
# Reinstall dependencies
rm -rf node_modules
npm install
```

### **Phone-Specific Issues**

#### **Android Installation Problems:**
1. Enable "Install from unknown sources"
2. Enable "Developer options"
3. Check available storage space

#### **Permissions Issues:**
1. Grant camera permissions manually
2. Allow location access
3. Enable network permissions

---

## 🧪 **Step 6: Testing Scenarios**

### **6.1 Complete App Test Flow**

**Preparation:**
1. Start backend: `cd backend && python app.py`
2. Ensure phone and computer on same WiFi
3. Open app on phone

**Test Sequence:**
1. **Home Screen Test:**
   - [ ] App opens without crashes
   - [ ] Statistics load (may show demo data)
   - [ ] Location permission requested

2. **Camera Test:**
   - [ ] Navigate to camera screen
   - [ ] Camera permission granted
   - [ ] Can take photos
   - [ ] Photos upload to backend

3. **Classification Test:**
   - [ ] Upload image gets processed
   - [ ] Classification results display
   - [ ] Confidence and recommendations shown

4. **Service Discovery Test:**
   - [ ] Service providers load
   - [ ] Can view service details
   - [ ] Location-based filtering works

5. **API Connectivity Test:**
   - [ ] All API calls successful
   - [ ] No network errors in logs
   - [ ] Data syncs properly

### **6.2 Demo Preparation Checklist**

**Before Demo:**
- [ ] Backend running on computer
- [ ] App installed on phone
- [ ] Same WiFi network
- [ ] Sample images ready
- [ ] All permissions granted
- [ ] Test complete user flow

**During Demo:**
- [ ] Show home screen with statistics
- [ ] Demonstrate camera functionality
- [ ] Show AI classification results
- [ ] Navigate through service providers
- [ ] Display booking functionality
- [ ] Show cross-platform consistency

---

## 📊 **Expected Performance**

### **Network Requirements:**
- **WiFi Speed**: Any modern WiFi (no specific speed required)
- **Latency**: < 100ms on local network
- **Data Usage**: Minimal (mostly image uploads)

### **Phone Requirements:**
- **Android**: 6.0+ (API level 23+)
- **iOS**: 10.0+
- **RAM**: 2GB+ recommended
- **Storage**: 100MB for app installation

### **Expected Load Times:**
- **App Launch**: 2-3 seconds
- **API Calls**: < 2 seconds on local network
- **Image Classification**: 3-5 seconds
- **Service Discovery**: 1-2 seconds

---

## 🎯 **Quick Setup Summary**

### **For Quick Demo Setup:**
```bash
# 1. Get your computer's IP
ipconfig  # Windows
ifconfig  # macOS/Linux

# 2. Update mobile app config
# Edit mobile-app/src/services/ApiService.js
# Change IP to your computer's IP

# 3. Start backend
cd backend && python app.py

# 4. Install app dependencies
cd mobile-app && npm install

# 5. Run on phone
npx react-native run-android  # or run-ios
```

### **For APK Installation:**
```bash
# Build APK
cd mobile-app/android
./gradlew assembleRelease

# Install on phone
adb install app/build/outputs/apk/release/app-release.apk
```

**🎉 Your WasteWise mobile app is now ready for testing and demonstration!**

Remember: For college demo, having both web and mobile versions working shows comprehensive full-stack development skills!