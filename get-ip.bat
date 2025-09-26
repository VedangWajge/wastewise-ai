@echo off
echo ===== WasteWise Network Configuration =====
echo.
echo Finding your computer's IP address for mobile connection:
echo.

for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4"') do (
    for /f "tokens=1" %%b in ("%%a") do (
        echo Found IP: %%b
    )
)

echo.
echo ===== Instructions =====
echo 1. Use one of the IP addresses above (typically 192.168.x.x)
echo 2. Update mobile-app/src/services/ApiService.js
echo 3. Replace "192.168.1.100" with your actual IP address
echo 4. Make sure both devices are on the same WiFi network
echo.
echo Example: const API_BASE_URL = 'http://192.168.1.2:5000/api';
echo.
pause