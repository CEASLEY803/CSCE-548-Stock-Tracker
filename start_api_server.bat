@echo off
REM Stock Portfolio Tracker - Start REST API Server
REM This script starts the FastAPI service layer

echo ============================================
echo Stock Portfolio Tracker - API Server
echo ============================================
echo.

echo Installing/Updating dependencies...
py -m pip install -r requirements.txt --quiet

echo.
echo Starting REST API server...
echo.
echo API Documentation will be available at:
echo   http://localhost:8000/docs
echo.
echo Press CTRL+C to stop the server
echo ============================================
echo.

py -m uvicorn service_layer:app --reload --host 0.0.0.0 --port 8000
