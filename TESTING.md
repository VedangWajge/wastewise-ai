# 🧪 WasteWise Testing Documentation

## Overview
This document provides comprehensive testing instructions for the WasteWise AI-Powered Smart Waste Segregation System. All testing scenarios are designed for demonstration and evaluation purposes.

---

## 🗂️ **Table of Contents**
1. [Pre-Testing Setup](#pre-testing-setup)
2. [Backend API Testing](#backend-api-testing)
3. [Frontend Web Application Testing](#frontend-web-application-testing)
4. [Mobile Application Testing](#mobile-application-testing)
5. [Integration Testing](#integration-testing)
6. [Performance Testing](#performance-testing)
7. [User Experience Testing](#user-experience-testing)
8. [Demo Scenarios](#demo-scenarios)

---

## 📋 **Pre-Testing Setup**

### **Environment Requirements**
- Node.js v14+ installed
- Python 3.8+ installed
- Modern web browser (Chrome, Firefox, Safari)
- Mobile device or emulator for mobile testing

### **Project Setup**
```bash
# 1. Clone/Navigate to project
cd wastewise

# 2. Backend Setup
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt

# 3. Frontend Setup
cd ../frontend
npm install

# 4. Start Services
# Terminal 1: Backend
cd backend && python app.py

# Terminal 2: Frontend
cd frontend && npm start
```

### **Verification Checklist**
- [ ] Backend running on `http://localhost:5000`
- [ ] Frontend running on `http://localhost:3000`
- [ ] No console errors on startup
- [ ] Health check endpoint responds: `http://localhost:5000/api/health`

---

## 🔧 **Backend API Testing**

### **1. Health Check**
```bash
# Test API availability
curl http://localhost:5000/api/health

# Expected Response:
{
  "status": "healthy",
  "message": "Wastewise API is running",
  "timestamp": "2024-XX-XXTXX:XX:XX"
}
```

### **2. Image Classification**
```bash
# Test with sample image (using curl or Postman)
curl -X POST http://localhost:5000/api/classify \
  -F "image=@sample-waste-image.jpg"

# Expected Response:
{
  "success": true,
  "filename": "uuid_filename.jpg",
  "classification": {
    "waste_type": "plastic",
    "confidence": 0.85,
    "recommendations": [...],
    "environmental_impact": "...",
    "all_predictions": {...}
  }
}
```

### **3. Service Provider APIs**
```bash
# Get nearby services
curl "http://localhost:5000/api/services/nearby?waste_type=plastic"

# Get all service providers
curl "http://localhost:5000/api/services/all"

# Get services by type
curl "http://localhost:5000/api/services/all?type=NGO"
```

### **4. Booking System**
```bash
# Create booking
curl -X POST http://localhost:5000/api/booking/create \
  -H "Content-Type: application/json" \
  -d '{
    "service_provider_id": "sp_001",
    "waste_type": "plastic",
    "quantity": "10 kg",
    "pickup_address": "Test Address",
    "scheduled_date": "2024-12-01T10:00:00Z"
  }'

# Track booking
curl http://localhost:5000/api/booking/track/book_001
```

### **5. Community APIs**
```bash
# Get all communities
curl http://localhost:5000/api/communities/all

# Get community dashboard
curl http://localhost:5000/api/community/comm_001/dashboard

# Join community
curl -X POST http://localhost:5000/api/community/join \
  -H "Content-Type: application/json" \
  -d '{"community_id": "comm_001", "unit_number": "A-101"}'
```

### **6. Analytics APIs**
```bash
# Environmental impact
curl "http://localhost:5000/api/analytics/impact?period=month"

# Waste trends
curl http://localhost:5000/api/analytics/trends

# Notifications
curl http://localhost:5000/api/notifications
```

---

## 🌐 **Frontend Web Application Testing**

### **1. Navigation Testing**
- [ ] **Home Page**: Loads without errors
- [ ] **Camera Tab**: Accessible via navigation
- [ ] **Dashboard Tab**: Displays statistics
- [ ] **Responsive**: Works on desktop, tablet, mobile viewports

### **2. Image Classification Flow**
1. **Image Upload Test**:
   - [ ] Click "📁 Upload Image" button
   - [ ] Select test image file
   - [ ] Verify loading spinner appears
   - [ ] Check classification results display
   - [ ] Validate confidence percentage and recommendations

2. **Camera Capture Test** (requires HTTPS/localhost):
   - [ ] Click "📸 Start Camera" button
   - [ ] Grant camera permissions
   - [ ] Verify video stream appears
   - [ ] Click "📷 Capture" button
   - [ ] Confirm image processing starts

### **3. Service Discovery Testing**
1. **After Classification**:
   - [ ] Click "🔍 Find Services Near You" button
   - [ ] Verify service list loads
   - [ ] Check service provider information accuracy
   - [ ] Test service filtering by waste type

2. **Service Selection**:
   - [ ] Click on different service providers
   - [ ] Verify service details display correctly
   - [ ] Check rating, distance, and contact information
   - [ ] Test "📞 Call" and "📅 Book Service" buttons

### **4. Booking System Testing**
1. **Booking Form**:
   - [ ] Fill all required fields
   - [ ] Test form validation (empty fields)
   - [ ] Verify date/time restrictions
   - [ ] Check cost calculation updates
   - [ ] Test recommended time slots

2. **Booking Submission**:
   - [ ] Submit valid booking form
   - [ ] Verify success message appears
   - [ ] Check booking ID generation
   - [ ] Confirm redirection to dashboard

### **5. Dashboard Testing**
1. **Statistics Display**:
   - [ ] Verify waste breakdown charts
   - [ ] Check environmental impact metrics
   - [ ] Test data refresh functionality
   - [ ] Validate responsive layout

2. **Interactive Elements**:
   - [ ] Test period selection (week/month/year)
   - [ ] Verify trend charts functionality
   - [ ] Check leaderboard display

---

## 📱 **Mobile Application Testing**

### **1. Setup and Installation**
```bash
cd mobile-app

# Install dependencies
npm install

# For Android (requires Android Studio)
npx react-native run-android

# For iOS (requires Xcode on macOS)
npx react-native run-ios
```

### **2. Navigation Testing**
- [ ] **Bottom Tab Navigation**: All tabs accessible
- [ ] **Stack Navigation**: Proper screen transitions
- [ ] **Back Button**: Correct navigation history

### **3. Camera Integration**
- [ ] **Permissions**: Camera permission request
- [ ] **Image Capture**: Photo taking functionality
- [ ] **Image Upload**: Gallery selection
- [ ] **Image Processing**: API integration

### **4. Location Services**
- [ ] **GPS Permission**: Location access request
- [ ] **Current Location**: Accurate location detection
- [ ] **Service Discovery**: Location-based filtering

### **5. Mobile-Specific Features**
- [ ] **Touch Gestures**: Tap, swipe, pinch interactions
- [ ] **Offline Indicators**: Network status display
- [ ] **Push Notifications**: Notification setup (demo)

---

## 🔄 **Integration Testing**

### **1. End-to-End User Journey**
```
User Flow: Image → Classification → Service → Booking → Tracking

1. Upload/Capture Image
2. Get AI Classification
3. Find Nearby Services
4. Select Service Provider
5. Fill Booking Form
6. Submit Booking
7. Track Booking Status
8. View Environmental Impact
```

### **2. Cross-Platform Consistency**
- [ ] **Web vs Mobile**: Feature parity
- [ ] **API Responses**: Consistent data format
- [ ] **UI/UX**: Similar user experience

### **3. Data Flow Validation**
- [ ] **Session Management**: User tracking across requests
- [ ] **Database Updates**: Data persistence
- [ ] **Real-time Updates**: Live data synchronization

---

## ⚡ **Performance Testing**

### **1. Load Testing**
```bash
# Install Apache Bench (ab) for basic load testing
# Test API endpoints
ab -n 100 -c 10 http://localhost:5000/api/health
ab -n 50 -c 5 http://localhost:5000/api/statistics
```

### **2. Response Time Testing**
- [ ] **API Response**: < 2 seconds for most endpoints
- [ ] **Image Classification**: < 10 seconds processing time
- [ ] **Page Load**: < 3 seconds initial load
- [ ] **Navigation**: < 500ms between screens

### **3. Resource Usage**
- [ ] **Memory**: Monitor browser/app memory usage
- [ ] **CPU**: Check processing efficiency
- [ ] **Network**: Optimize API calls and image sizes

---

## 🎭 **User Experience Testing**

### **1. Usability Testing**
- [ ] **Intuitive Navigation**: Easy to find features
- [ ] **Clear Instructions**: Helpful guidance text
- [ ] **Error Handling**: Friendly error messages
- [ ] **Accessibility**: Screen reader compatibility

### **2. Visual Testing**
- [ ] **Responsive Design**: All screen sizes
- [ ] **Color Contrast**: Readable text
- [ ] **Loading States**: Proper feedback
- [ ] **Empty States**: Graceful handling

### **3. Error Scenarios**
- [ ] **Network Offline**: Appropriate error handling
- [ ] **Invalid Images**: Proper validation
- [ ] **Server Errors**: User-friendly messages
- [ ] **Permission Denied**: Clear instructions

---

## 🎬 **Demo Scenarios**

### **Scenario 1: Complete User Journey (5 minutes)**
```
1. Open WasteWise web application
2. Upload sample plastic bottle image
3. Show AI classification results (plastic, 85% confidence)
4. Click "Find Services Near You"
5. Display 5 service providers with details
6. Select "RecyclePlus Industries"
7. Fill booking form with sample data
8. Submit booking and show success
9. Navigate to dashboard
10. Display environmental impact metrics
```

### **Scenario 2: Service Provider Discovery (3 minutes)**
```
1. Start from classification results
2. Show different waste types get different services
3. Demonstrate distance and rating filtering
4. Show service provider details and specialties
5. Explain booking process and tracking
```

### **Scenario 3: Community Features (3 minutes)**
```
1. Navigate to community management
2. Show society dashboard with aggregated data
3. Display community leaderboards
4. Demonstrate bulk booking features
5. Show environmental impact at community level
```

### **Scenario 4: Mobile App Experience (4 minutes)**
```
1. Open mobile app
2. Show camera integration
3. Demonstrate GPS-based service discovery
4. Show mobile-optimized booking flow
5. Display push notification setup
```

---

## 🐛 **Common Issues & Solutions**

### **Backend Issues**
| Issue | Solution |
|-------|----------|
| Port 5000 in use | Kill process: `taskkill /F /PID <pid>` (Windows) |
| Module not found | Activate venv: `venv\Scripts\activate` |
| Database errors | Delete `wastewise.db` and restart |

### **Frontend Issues**
| Issue | Solution |
|-------|----------|
| CORS errors | Ensure Flask-CORS is installed |
| npm install fails | Clear cache: `npm cache clean --force` |
| Camera not working | Use HTTPS or localhost |

### **Mobile Issues**
| Issue | Solution |
|-------|----------|
| Metro bundler issues | Reset cache: `npx react-native start --reset-cache` |
| Build failures | Clean project: `cd android && ./gradlew clean` |
| Permissions not working | Check platform-specific permission setup |

---

## ✅ **Testing Checklist Summary**

### **Critical Path Testing**
- [ ] Health check endpoint responds
- [ ] Image classification works with sample images
- [ ] Service discovery returns realistic data
- [ ] Booking form validates and submits
- [ ] Dashboard displays statistics
- [ ] Mobile app installs and runs

### **Feature Completeness**
- [ ] All 15+ API endpoints functional
- [ ] Web application fully navigable
- [ ] Mobile app prototype operational
- [ ] Demo data realistic and comprehensive
- [ ] Error handling graceful throughout

### **Presentation Readiness**
- [ ] Demo scenarios practiced
- [ ] Sample images prepared
- [ ] Test data populated
- [ ] Screenshots/videos captured
- [ ] Backup plans for technical issues

---

## 📊 **Success Metrics**

### **Technical Metrics**
- ✅ **API Coverage**: 15+ endpoints implemented
- ✅ **Response Time**: < 3 seconds average
- ✅ **Error Rate**: < 5% during testing
- ✅ **Cross-browser**: Chrome, Firefox, Safari compatible

### **Feature Metrics**
- ✅ **Classification Accuracy**: Realistic demo responses
- ✅ **Service Discovery**: 5+ service providers
- ✅ **Booking Success**: 100% form submission rate
- ✅ **Mobile Compatibility**: iOS and Android ready

### **User Experience Metrics**
- ✅ **Navigation Flow**: Intuitive user journey
- ✅ **Visual Design**: Professional appearance
- ✅ **Responsiveness**: All device sizes supported
- ✅ **Accessibility**: Screen reader compatible

---

**📝 Testing completed successfully means your WasteWise prototype is ready for college project demonstration and evaluation!**