@echo off
echo 🛡️  RYVEN Fraud Detection System
echo =================================
echo.

cd backend

echo 📦 Installing dependencies...
pip install -r requirements.txt

echo.
echo 🚀 Starting backend server...
echo    API: http://localhost:8000
echo    Docs: http://localhost:8000/docs
echo.
echo 👉 Open frontend/index.html in your browser
echo.

uvicorn main:app --reload --host 0.0.0.0 --port 8000
pause
