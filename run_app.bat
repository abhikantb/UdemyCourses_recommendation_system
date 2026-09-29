@echo off
TITLE Launching Course Recommendation Engine
echo ===================================================
echo   Starting LLM Course Recommendation Engine...
echo ===================================================
echo.

REM 1. Navigate to current project directory
cd /d "%~dp0"

REM 2. Activate virtual environment
call .venv\Scripts\activate.bat

REM 3. Launch Gradio App
echo Environment activated. Launching app in browser...
python app.py

pause