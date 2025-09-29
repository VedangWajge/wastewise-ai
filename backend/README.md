# WasteWise Backend Setup

## Prerequisites
- Python 3.11.0 (specified in runtime.txt)
- pip (Python package manager)

## Installation Steps

### 1. Clone the Repository
```bash
git clone https://github.com/VedangWajge/wastewise-ai.git
cd wastewise-ai/backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv
```

### 3. Activate Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Upgrade pip
```bash
pip install --upgrade pip
```

### 5. Install Dependencies
```bash
pip install -r requirements.txt
```

## Troubleshooting

### TensorFlow Installation Issues
If TensorFlow installation fails, try installing it separately first:
```bash
pip install tensorflow==2.13.0
```

### OpenCV Installation Issues
If opencv-python fails, try:
```bash
pip install opencv-python-headless==4.8.1.78
```

### Python Version Issues
- Ensure you're using Python 3.11.0 (check with `python --version`)
- TensorFlow 2.13.0 requires Python 3.8-3.11
- Python 3.12+ is not supported by this TensorFlow version

### Common Error Solutions
1. **"Microsoft Visual C++ 14.0 is required"** (Windows):
   - Install Microsoft Visual Studio Build Tools

2. **Permission errors**:
   - Use `pip install --user -r requirements.txt`

3. **Package conflicts**:
   - Delete venv folder and recreate it
   - Clear pip cache: `pip cache purge`

## Running the Backend
```bash
python app.py
```

## Environment Variables
Create a `.env` file in the backend directory with required environment variables (refer to the main project documentation).