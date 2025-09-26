#!/bin/bash
echo "===== WasteWise Network Configuration ====="
echo
echo "Finding your computer's IP address for mobile connection:"
echo

# For macOS/Linux
if command -v ifconfig &> /dev/null; then
    echo "Available IP addresses:"
    ifconfig | grep -E "inet [0-9]" | grep -v "127.0.0.1" | awk '{print "Found IP:", $2}'
    echo
elif command -v ip &> /dev/null; then
    echo "Available IP addresses:"
    ip addr show | grep -E "inet [0-9]" | grep -v "127.0.0.1" | awk '{print "Found IP:", $2}' | cut -d'/' -f1
    echo
fi

echo "===== Instructions ====="
echo "1. Use one of the IP addresses above (typically 192.168.x.x or 10.0.x.x)"
echo "2. Update mobile-app/src/services/ApiService.js"
echo "3. Replace '192.168.1.100' with your actual IP address"
echo "4. Make sure both devices are on the same WiFi network"
echo
echo "Example: const API_BASE_URL = 'http://192.168.1.2:5000/api';"
echo