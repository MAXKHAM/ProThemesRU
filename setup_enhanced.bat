@echo off
echo ========================================
echo ProThemesRU Enhanced Editor Setup
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
echo Installing additional dependencies for enhanced features...
npm install jszip file-saver

echo.
echo ========================================
echo Enhanced setup complete!
echo ========================================
echo.
echo New features available:
echo - History management with undo/redo
echo - Enhanced export to HTML/CSS with ZIP
echo - AI color palette generator
echo - Improved UI and interactions
echo.
echo To start the servers:
echo 1. Flask backend: python app.py (in main directory)
echo 2. React frontend: npm start (in react-canvas-editor directory)
echo.
echo Or run: start_servers.bat
echo.
pause 