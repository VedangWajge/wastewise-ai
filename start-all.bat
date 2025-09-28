@echo off
title WasteWise - Full Stack Development
echo ===== Starting WasteWise Full Stack Development Environment =====
echo.

:: Check if we're in the right directory
if not exist "backend\app.py" (
    echo Error: Please run this script from the wastewise root directory
    echo Expected structure: wastewise/backend/app.py
    pause
    exit /b 1
)

echo Starting all services...
echo.

:: Start Backend Server
echo [1/4] Starting Backend Server (Flask)...
start "WasteWise Backend" cmd /k "cd backend && venv\Scripts\activate && echo Backend Server Starting... && python app.py"

:: Wait a moment for backend to initialize
timeout /t 3 /nobreak >nul

:: Start Frontend Web Server
echo [2/4] Starting Frontend Web Server (React)...
start "WasteWise Frontend" cmd /k "cd frontend && echo Frontend Starting... && npm start"

:: Start Mobile Metro Bundler
echo [3/4] Starting Mobile Metro Bundler...
start "WasteWise Mobile Metro" cmd /k "cd mobile-app && echo Metro Bundler Starting... && npx react-native start"

:: Wait for Metro to initialize
timeout /t 5 /nobreak >nul

:: Prompt for mobile device connection
echo [4/4] Ready to connect mobile device...
echo.
echo ===== Next Steps =====
echo 1. Backend Server: Running on http://localhost:5000
echo 2. Web Frontend: Opening at http://localhost:3000
echo 3. Mobile Metro: Ready for device connection
echo.
echo To connect your mobile device:
echo   Run: npx react-native run-android (requires Android Studio)
echo   Or: npx react-native run-ios (requires Xcode)
echo.
echo 📱 Make sure you have Android Studio or Xcode set up for mobile development!
echo.
echo ===== Network Info =====
echo Your computer's IP addresses:
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4"') do (
    for /f "tokens=1" %%b in ("%%a") do (
        echo Mobile API URL: http://%%b:5000/api
    )
)
echo.
echo All services are starting in separate windows...
echo Close this window or press any key to continue.
pause >nul