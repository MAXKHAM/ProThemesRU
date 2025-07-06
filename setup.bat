@echo off
echo ========================================
echo ProThemesRU - Setup and Run Script
echo ========================================
echo.

echo [1/4] Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install Python dependencies
    pause
    exit /b 1
)

echo.
echo [2/4] Installing React dependencies...
cd react-canvas-editor
npm install
if %errorlevel% neq 0 (
    echo Error: Failed to install React dependencies
    pause
    exit /b 1
)
cd ..

echo.
echo [3/4] Starting Flask backend...
start "Flask Backend" cmd /k "python run.py"

echo.
echo [4/4] Starting React frontend...
cd react-canvas-editor
start "React Frontend" cmd /k "npm start"
cd ..

echo.
echo ========================================
echo Setup complete!
echo ========================================
echo.
echo Flask Backend: http://127.0.0.1:5000
echo React Frontend: http://localhost:3000
echo.
echo Both applications are now running in separate windows.
echo Close the windows to stop the applications.
echo.
pause 