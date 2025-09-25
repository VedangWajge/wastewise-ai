# 🌱 WasteWise: AI-Powered Smart Waste Segregation System

WasteWise is an intelligent waste management application that uses AI-powered image recognition to classify waste types and provide disposal recommendations. Built with React frontend and Flask backend, it helps users make environmentally conscious decisions about waste disposal.

## ✨ Features

- **📸 Smart Image Classification**: Upload or capture images of waste items for instant AI-powered classification
- **🎯 Accurate Detection**: Identifies 5 waste categories: Plastic, Organic, Paper, Glass, and Metal
- **📊 Real-time Dashboard**: Track your environmental impact with comprehensive statistics
- **♻️ Disposal Recommendations**: Get specific instructions for proper waste disposal
- **🌍 Environmental Impact**: Monitor CO₂, water, and energy savings from your recycling efforts
- **📱 Mobile-Friendly**: Responsive design works perfectly on all devices
- **🔄 Real-time Processing**: Instant classification results with confidence scoring

## 🏗️ System Architecture

```
WasteWise/
├── frontend/                 # React Application
│   ├── src/
│   │   ├── components/       # React Components
│   │   │   ├── Camera.js     # Image capture/upload
│   │   │   ├── Classification.js  # Results display
│   │   │   └── Dashboard.js  # Statistics dashboard
│   │   ├── services/
│   │   │   └── api.js        # API communication
│   │   ├── App.js           # Main application
│   │   └── App.css          # Global styles
│   └── public/              # Static assets
├── backend/                 # Flask API Server
│   ├── app.py              # Main Flask application
│   ├── models/
│   │   ├── waste_classifier.py  # AI classification logic
│   │   └── database.py     # Database operations
│   ├── utils/
│   │   └── image_processing.py  # Image preprocessing
│   └── uploads/            # Uploaded images storage
├── database/
│   └── init.sql            # Database schema
└── README.md               # Project documentation
```

## 🚀 Quick Start

### Prerequisites

- **Node.js** (v14 or higher)
- **Python** (v3.8 or higher)
- **npm** or **yarn**
- **pip** (Python package installer)

### Installation Steps

#### 1. Clone the Repository
```bash
git clone <repository-url>
cd wastewise
```

#### 2. Set Up Backend (Flask)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\\Scripts\\activate
# macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Start Flask server
python app.py
```

The Flask server will start at `http://localhost:5000`

#### 3. Set Up Frontend (React)

```bash
# Open new terminal and navigate to frontend
cd frontend

# Install Node.js dependencies
npm install

# Start React development server
npm start
```

The React app will open at `http://localhost:3000`

## 📋 API Endpoints

### Health Check
- **GET** `/api/health` - Check API server status

### Waste Classification
- **POST** `/api/classify` - Classify waste from uploaded image
  - Body: `multipart/form-data` with `image` file
  - Response: Classification result with confidence and recommendations

### Statistics
- **GET** `/api/statistics` - Get waste classification statistics
- **GET** `/api/recent?limit=10` - Get recent classifications

## 🤖 AI Model Integration

The system uses a modular AI architecture:

### Current Implementation
- **Mock Classification**: Returns realistic predictions for development/testing
- **Image Preprocessing**: OpenCV-based image enhancement and resizing
- **Feature Extraction**: Basic color and texture analysis

### Production Deployment
Replace the mock classifier with a trained model:

```python
# In models/waste_classifier.py
def load_model(self, model_path):
    import tensorflow as tf
    self.model = tf.keras.models.load_model(model_path)

def classify(self, image_path):
    processed_image = self.preprocess_image(image_path)
    predictions = self.model.predict(processed_image)
    # Process predictions and return results
```

## 🗄️ Database Schema

### SQLite Tables
- **classifications**: Store all waste classification results
- **waste_categories**: Reference data for waste types
- **user_sessions**: Track user activity and statistics

### Key Features
- Automatic timestamp tracking
- Session-based user analytics
- Comprehensive waste statistics
- Data cleanup utilities

## 🎨 UI Components

### Camera Component
- Camera access and image capture
- File upload functionality
- Cross-platform compatibility
- Error handling and permissions

### Classification Component
- Real-time result display
- Confidence visualization
- Disposal recommendations
- Environmental impact information

### Dashboard Component
- Interactive statistics
- Waste breakdown charts
- Environmental impact metrics
- Historical data visualization

## 📱 Mobile Support

- **Responsive Design**: Adapts to all screen sizes
- **Touch-Friendly**: Optimized for mobile interactions
- **Camera Access**: Direct camera integration on mobile devices
- **Offline Capability**: Basic functionality without internet (future feature)

## 🔒 Security Features

- **File Validation**: Secure file upload with type checking
- **CORS Protection**: Configured cross-origin resource sharing
- **Input Sanitization**: Secure filename handling
- **Session Management**: Secure session tracking
- **Rate Limiting**: API abuse protection (recommended for production)

## 🌍 Environmental Impact

WasteWise calculates environmental benefits:

- **CO₂ Savings**: Based on recycling vs. landfill disposal
- **Water Conservation**: Manufacturing savings from recycled materials
- **Energy Efficiency**: Reduced energy consumption from recycling
- **Resource Conservation**: Raw material savings

## 📊 Analytics & Monitoring

### Built-in Analytics
- Classification accuracy tracking
- User engagement metrics
- Waste type distribution
- Environmental impact calculations

### Future Enhancements
- Advanced analytics dashboard
- Machine learning model performance monitoring
- User behavior analysis
- A/B testing framework

## 🚀 Deployment

### Development
- Frontend: `npm start` (React Dev Server)
- Backend: `python app.py` (Flask Dev Server)

### Production
- Frontend: `npm run build` → Deploy to CDN/Static hosting
- Backend: Use production WSGI server (Gunicorn, uWSGI)
- Database: PostgreSQL/MySQL for production workloads
- Images: Cloud storage (AWS S3, Cloudinary)

### Docker Deployment (Recommended)

```dockerfile
# Dockerfile example for backend
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

## 🔧 Configuration

### Environment Variables
```bash
# Backend Configuration
FLASK_ENV=development
DATABASE_URL=sqlite:///wastewise.db
SECRET_KEY=your-secret-key-here
MAX_CONTENT_LENGTH=16777216  # 16MB

# AI Model Configuration
MODEL_PATH=models/waste_classifier.h5
CONFIDENCE_THRESHOLD=0.6
```

### Frontend Configuration
```javascript
// src/config.js
export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';
export const MAX_FILE_SIZE = 16 * 1024 * 1024; // 16MB
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
python -m pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check this README and inline code comments
- **Issues**: Open an issue on GitHub for bugs or feature requests
- **Community**: Join our community discussions

## 🎯 Roadmap

### Version 1.0 (Current)
- ✅ Basic waste classification
- ✅ Web-based interface
- ✅ SQLite database
- ✅ Statistics dashboard

### Version 2.0 (Planned)
- 🔄 Advanced AI models (YOLOv8, ResNet)
- 🔄 Real-time video processing
- 🔄 Multi-language support
- 🔄 Progressive Web App (PWA)

### Version 3.0 (Future)
- 🔄 IoT integration
- 🔄 Community features
- 🔄 Gamification
- 🔄 Enterprise features

---

**Made with ❤️ for a sustainable future**

*WasteWise - Making waste management smarter with AI*