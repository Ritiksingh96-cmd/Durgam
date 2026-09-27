@echo off
title PROJECT DURGAM - Sovereign AI Cybercrime Defense Platform
color 0A
cls

echo ========================================================================
echo          PROJECT DURGAM - SOVEREIGN AI CYBERCRIME DEFENSE
echo       National Real-Time Interception, CAD Dispatch ^& Restitution
echo ========================================================================
echo.

:: 1. Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo [ERROR] Python is not installed or not in system PATH!
    echo Please install Python 3.10+ from python.org and add it to PATH.
    pause
    exit /b 1
)

echo [*] Python environment detected.
echo [*] Synchronizing frontend assets and static files...
python sync_static.py

echo [*] Seeding persistent case records and empirical complaints...
python seed_user_complaints.py

echo [*] Launching DURGAM Sovereign Portal in default browser...
start "" "http://127.0.0.1:8000/login.html"

echo.
echo ========================================================================
echo  Server URL: http://127.0.0.1:8000
echo  Citizen Portal: http://127.0.0.1:8000/citizen.html
echo  Bank Portal:    http://127.0.0.1:8000/bank.html
echo  Command Center: http://127.0.0.1:8000/command.html
echo  Police Portal:  http://127.0.0.1:8000/police.html
echo  Judiciary Court:http://127.0.0.1:8000/judiciary.html
echo  BSA Vault:      http://127.0.0.1:8000/verify.html
echo ========================================================================
echo.
echo [*] Starting FastAPI Uvicorn Server on 127.0.0.1:8000...
echo [!] Press CTRL+C to stop the server.
echo.

python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload

pause
