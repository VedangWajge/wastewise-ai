@echo off
title WasteWise - Mobile Device Connection
echo ===== WasteWise Mobile Device Connection =====
echo.

if not exist "mobile-app\package.json" (
    echo Error: Please run this script from the wastewise root directory
    pause
    exit /b 1
)

echo Choose your mobile development option:
echo.
echo 1. Traditional React Native (requires Android Studio)
echo 2. Expo (easiest - scan QR code with Expo Go app)
echo 3. Check project setup status
echo 4. Fix React Native project
echo 5. Exit
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    echo.
    if exist "mobile-app\android" (
        echo Starting traditional React Native...
        echo Make sure:
        echo - Android Studio is installed
        echo - USB debugging is enabled
        echo - Device is connected via USB OR emulator is running
        echo.
        cd mobile-app
        start "Metro Bundler" cmd /k "npx react-native start"
        timeout /t 3 /nobreak >nul
        echo.
        echo Choose platform:
        echo A. Android
        echo I. iOS (macOS only)
        echo.
        set /p platform="Enter A or I: "
        if /i "%platform%"=="A" (
            npx react-native run-android
        ) else if /i "%platform%"=="I" (
            npx react-native run-ios
        )
    ) else (
        echo ❌ Android project not found!
        echo.
        echo Your React Native project is missing the native Android/iOS folders.
        echo This is required to run on physical devices.
        echo.
        echo Solutions:
        echo 1. Use option 4 to fix the React Native project
        echo 2. Use option 2 for Expo (no Android Studio needed)
        echo.
        pause
    )
) else if "%choice%"=="2" (
    echo.
    echo Starting Expo development...
    if exist "mobile-app-expo" (
        cd mobile-app-expo
        echo.
        echo 📱 Instructions:
        echo 1. Install "Expo Go" app on your phone
        echo 2. Scan the QR code that appears
        echo 3. Your app will load automatically!
        echo.
        npx expo start
    ) else (
        echo ❌ Expo project not found!
        echo.
        echo Creating Expo project for easy mobile development...
        npx create-expo-app mobile-app-expo --template blank
        echo.
        echo ✅ Expo project created! Run this option again to start.
        pause
    )
) else if "%choice%"=="3" (
    echo.
    echo Checking project setup status...
    echo.
    if exist "mobile-app\android" (
        echo ✅ React Native Android project found
    ) else (
        echo ❌ React Native Android project missing
    )
    if exist "mobile-app\ios" (
        echo ✅ React Native iOS project found
    ) else (
        echo ❌ React Native iOS project missing
    )
    if exist "mobile-app-expo" (
        echo ✅ Expo project found
    ) else (
        echo ❌ Expo project not found
    )
    echo.
    if exist "mobile-app\node_modules" (
        echo ✅ Node modules installed
    ) else (
        echo ❌ Node modules missing - run 'npm install'
    )
    echo.
    pause
    goto :start
) else if "%choice%"=="4" (
    echo.
    echo 🔧 React Native Project Fix
    echo.
    echo This will help you set up a proper React Native project.
    echo Please see REACT_NATIVE_FIX.md for detailed instructions.
    echo.
    echo Quick options:
    echo A. Open React Native fix guide
    echo B. Go back to main menu
    echo.
    set /p fix="Enter A or B: "
    if /i "%fix%"=="A" (
        notepad REACT_NATIVE_FIX.md
    )
    goto :start
) else if "%choice%"=="5" (
    exit /b 0
) else (
    echo Invalid choice. Please try again.
    echo.
    goto :start
)

:start
pause