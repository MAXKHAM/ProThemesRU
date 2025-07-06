@echo off
echo ========================================
echo ProThemesRU AI Editor Setup
echo ========================================

echo.
echo Installing Flask backend dependencies...
cd ..
pip install -r requirements.txt

echo.
echo Installing React frontend dependencies...
cd react-canvas-editor
npm install

echo.
echo ========================================
echo Setup complete!
echo ========================================
echo.
echo To start the servers:
echo 1. Flask backend: python app.py (in main directory)
echo 2. React frontend: npm start (in react-canvas-editor directory)
echo.
echo Or run: start_servers.bat
echo.
pause 