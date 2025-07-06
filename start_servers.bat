@echo off
echo ========================================
echo Starting ProThemesRU AI Editor Servers
echo ========================================

echo.
echo Starting Flask backend server...
start "Flask Backend" cmd /k "cd .. && python app.py"

echo.
echo Waiting 3 seconds for Flask to start...
timeout /t 3 /nobreak > nul

echo.
echo Starting React frontend server...
start "React Frontend" cmd /k "npm start"

echo.
echo ========================================
echo Servers are starting...
echo ========================================
echo.
echo Flask backend: http://127.0.0.1:5000
echo React frontend: http://localhost:3000
echo.
echo Press any key to close this window...
pause > nul 