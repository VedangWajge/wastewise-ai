# How to Start WasteWise Application

## The Problem
You're seeing these errors:
```
Failed to load resource: net::ERR_CONNECTION_REFUSED
localhost:5000/api/auth/profile
localhost:5000/api/auth/logout
```

**This means the backend server is NOT running!**

## Solution - Start Both Servers

### Step 1: Start Backend Server (Required!)

Open a **new terminal** and run:

```bash
cd backend
python app.py
```

**Expected Output:**
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
Database initialized successfully
```

**Important:** Keep this terminal open! Don't close it.

### Step 2: Start Frontend Server (if not running)

Open **another terminal** and run:

```bash
cd frontend
npm start
```

**Expected Output:**
```
Compiled successfully!
You can now view wastewise in the browser.

Local:            http://localhost:3000
```

## Full Startup Process

### Option A: Using Two Terminals (Recommended)

**Terminal 1 - Backend:**
```bash
# Navigate to backend folder
cd E:\Vedang\STUDY\Programming\com.vedang.play\V2WEngg\MajorProjsem7and8\wastewise\backend

# Start Flask server
python app.py
```

**Terminal 2 - Frontend:**
```bash
# Navigate to frontend folder
cd E:\Vedang\STUDY\Programming\com.vedang.play\V2WEngg\MajorProjsem7and8\wastewise\frontend

# Start React app
npm start
```

### Option B: Using PowerShell Background Jobs

Create a file `start_all.ps1`:
```powershell
# Start backend in background
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; python app.py"

# Wait a bit for backend to start
Start-Sleep -Seconds 3

# Start frontend in background
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm start"

Write-Host "Both servers starting..."
Write-Host "Backend: http://localhost:5000"
Write-Host "Frontend: http://localhost:3000"
```

Then run: `.\start_all.ps1`

## Verification Checklist

### 1. Check Backend is Running
Open browser to: http://localhost:5000

**You should see:** Some JSON response or Flask error page (not connection refused)

### 2. Check Frontend is Running
Open browser to: http://localhost:3000

**You should see:** Your WasteWise application

### 3. Check API Connection
Open browser console (F12), you should see:
- No `ERR_CONNECTION_REFUSED` errors
- Successful API calls to `http://localhost:5000/api/*`

## Common Issues & Solutions

### Issue 1: Port 5000 Already in Use
```
OSError: [WinError 10048] Only one usage of each socket address
```

**Solution:**
```bash
# Kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F

# Or use different port
python app.py --port 5001
```

### Issue 2: Port 3000 Already in Use
```
? Something is already running on port 3000.
```

**Solution:**
- Press `Y` to run on different port (3001)
- Or kill existing process:
```bash
netstat -ano | findstr :3000
taskkill /PID <PID_NUMBER> /F
```

### Issue 3: Python Not Found
```
'python' is not recognized as an internal or external command
```

**Solution:**
```bash
# Try python3 instead
python3 app.py

# Or use py launcher
py app.py
```

### Issue 4: Module Not Found
```
ModuleNotFoundError: No module named 'flask'
```

**Solution:**
```bash
cd backend
pip install -r requirements.txt
```

## Status Indicators

### Backend Running ✅
Terminal shows:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

Browser http://localhost:5000 shows response (not connection error)

### Backend NOT Running ❌
Browser shows:
```
This site can't be reached
localhost refused to connect
ERR_CONNECTION_REFUSED
```

### Frontend Running ✅
Browser http://localhost:3000 shows your app
Terminal shows: `webpack compiled with 0 errors`

### Frontend NOT Running ❌
Browser shows:
```
This site can't be reached
localhost refused to connect
```

## Quick Test Commands

### Test Backend API
```bash
# Windows PowerShell
Invoke-WebRequest -Uri "http://localhost:5000/api/analytics/dashboard" -Method GET

# Or use browser
# Open: http://localhost:5000/api/analytics/dashboard
```

### Test Frontend
```bash
# Open browser to:
http://localhost:3000
```

## Recommended Workflow

### Development Session Start:
1. Open VS Code (or your IDE)
2. Open Terminal 1 → `cd backend` → `python app.py`
3. Open Terminal 2 → `cd frontend` → `npm start`
4. Wait for both to compile
5. Browser opens automatically to http://localhost:3000

### Development Session End:
1. Terminal 1 → Press `Ctrl+C` to stop backend
2. Terminal 2 → Press `Ctrl+C` to stop frontend
3. Close terminals

## Current Status Check

Run these commands to check what's running:

```powershell
# Check if backend is running on port 5000
netstat -ano | findstr :5000

# Check if frontend is running on port 3000
netstat -ano | findstr :3000

# If you see output, servers are running
# If no output, servers are NOT running
```

## Your Next Steps

1. **Start Backend Server** (Terminal 1):
   ```bash
   cd backend
   python app.py
   ```

2. **Keep Frontend Running** (Terminal 2 should already be running):
   ```bash
   # If not running:
   cd frontend
   npm start
   ```

3. **Refresh Browser** at http://localhost:3000

4. **Check Console** - Should see no connection errors

Once both servers are running:
- ✅ Services will load
- ✅ No connection refused errors
- ✅ Authentication will work
- ✅ All features functional

## Summary

**Your issue:** Backend server not running → Connection refused errors

**Solution:** Start backend server with `python app.py` in backend folder

**Result:** All API calls will work, services will load, no more errors!

---

**IMPORTANT:** Always run both servers during development:
- **Backend** (port 5000) - Flask API server
- **Frontend** (port 3000) - React development server
