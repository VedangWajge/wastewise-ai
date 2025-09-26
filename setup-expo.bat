@echo off
title WasteWise - Expo Setup (Easy Mobile Development)
echo ===== WasteWise Expo Setup =====
echo.
echo This will set up Expo for easy mobile development (no Android Studio required!)
echo.

if exist "mobile-app-expo" (
    echo ✅ Expo project already exists in wastewise directory!
    echo Do you want to:
    echo 1. Start existing Expo project
    echo 2. Recreate Expo project
    echo 3. Exit
    echo.
    set /p choice="Enter your choice (1-3): "

    if "%choice%"=="1" (
        goto :start_expo
    ) else if "%choice%"=="2" (
        echo Removing existing Expo project...
        rmdir /s /q mobile-app-expo
        goto :create_expo
    ) else (
        exit /b 0
    )
) else (
    goto :create_expo
)

:create_expo
echo.
echo 📱 Creating Expo project...
echo This may take a few minutes...
echo.

npx create-expo-app mobile-app-expo --template blank

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Failed to create Expo project!
    echo Please make sure you have Node.js installed and try again.
    pause
    exit /b 1
)

echo.
echo ✅ Expo project created successfully!
echo.

cd mobile-app-expo

echo Installing navigation dependencies...
npx expo install @react-navigation/native @react-navigation/stack @react-navigation/bottom-tabs
npx expo install react-native-screens react-native-safe-area-context

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ⚠️ Some packages failed to install, but the basic Expo project is ready.
)

echo.
echo 📋 Copying your WasteWise code...

:: Copy the custom App.js and source files
if exist "..\mobile-app\App.js" (
    copy "..\mobile-app\App.js" "App.js" >nul
    echo ✅ App.js copied
)

if exist "..\mobile-app\src\" (
    xcopy "..\mobile-app\src\" "src\" /E /I /Q >nul
    echo ✅ Source files copied
) else (
    echo ⚠️ Source files not found - you may need to recreate them for Expo
)

echo.
echo 🎉 Expo setup complete!
echo.

:start_expo
cd mobile-app-expo

echo ===== How to Use Expo =====
echo.
echo 1. Install "Expo Go" app on your phone from:
echo    - Android: Google Play Store
echo    - iOS: Apple App Store
echo.
echo 2. Make sure your phone and computer are on the same WiFi network
echo.
echo 3. When the QR code appears, scan it with:
echo    - Android: Expo Go app
echo    - iOS: Camera app (will open in Expo Go)
echo.
echo 4. Your WasteWise app will load on your phone instantly!
echo.
echo 📱 Starting Expo development server...
echo Press Ctrl+C to stop when you're done.
echo.

npx expo start

echo.
echo Development server stopped.
pause