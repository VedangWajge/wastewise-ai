#!/bin/bash

echo "===== Starting WasteWise Full Stack Development Environment ====="
echo

# Check if we're in the right directory
if [ ! -f "backend/app.py" ]; then
    echo "Error: Please run this script from the wastewise root directory"
    echo "Expected structure: wastewise/backend/app.py"
    exit 1
fi

echo "Starting all services..."
echo

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Start Backend Server
echo "[1/4] Starting Backend Server (Flask)..."
if [ -f "backend/venv/bin/activate" ]; then
    osascript -e 'tell app "Terminal" to do script "cd '$(pwd)'/backend && source venv/bin/activate && echo \"Backend Server Starting...\" && python app.py"' 2>/dev/null || \
    gnome-terminal --title="WasteWise Backend" -- bash -c "cd backend && source venv/bin/activate && echo 'Backend Server Starting...' && python app.py; exec bash" 2>/dev/null || \
    echo "Please manually run: cd backend && source venv/bin/activate && python app.py"
else
    echo "Virtual environment not found. Please run: cd backend && python -m venv venv"
fi

# Wait for backend to initialize
sleep 3

# Start Frontend Web Server
echo "[2/4] Starting Frontend Web Server (React)..."
if command_exists npm; then
    osascript -e 'tell app "Terminal" to do script "cd '$(pwd)'/frontend && echo \"Frontend Starting...\" && npm start"' 2>/dev/null || \
    gnome-terminal --title="WasteWise Frontend" -- bash -c "cd frontend && echo 'Frontend Starting...' && npm start; exec bash" 2>/dev/null || \
    echo "Please manually run: cd frontend && npm start"
else
    echo "npm not found. Please install Node.js"
fi

# Start Mobile Metro Bundler
echo "[3/4] Starting Mobile Metro Bundler..."
if command_exists npm; then
    osascript -e 'tell app "Terminal" to do script "cd '$(pwd)'/mobile-app && echo \"Metro Bundler Starting...\" && npm start"' 2>/dev/null || \
    gnome-terminal --title="WasteWise Mobile Metro" -- bash -c "cd mobile-app && echo 'Metro Bundler Starting...' && npm start; exec bash" 2>/dev/null || \
    echo "Please manually run: cd mobile-app && npm start"
fi

# Wait for Metro to initialize
sleep 5

echo "[4/4] Ready to connect mobile device..."
echo
echo "===== Next Steps ====="
echo "1. Backend Server: Running on http://localhost:5000"
echo "2. Web Frontend: Opening at http://localhost:3000"
echo "3. Mobile Metro: Ready for device connection"
echo
echo "To connect your mobile device:"
echo "  Android: npx react-native run-android"
echo "  iOS:     npx react-native run-ios"
echo
echo "Or run: ./start-mobile.sh (in a new terminal)"
echo
echo "===== Network Info ====="
echo "Your computer's IP addresses:"
if command_exists ifconfig; then
    ifconfig | grep -E "inet [0-9]" | grep -v "127.0.0.1" | awk '{print "Mobile API URL: http://" $2 ":5000/api"}'
elif command_exists ip; then
    ip addr show | grep -E "inet [0-9]" | grep -v "127.0.0.1" | awk '{print "Mobile API URL: http://" $2 ":5000/api"}' | cut -d'/' -f1
fi
echo
echo "All services are starting in separate terminals..."