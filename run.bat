@echo off
title PROJECT DURGAM — Sovereign Cyber Defense Platform
color 0A
cls

echo.
echo  ████████████████████████████████████████████████████████████████████████
echo  █                                                                      █
echo  █   PROJECT DURGAM — National Cybercrime Real-Time Interception Grid  █
echo  █   I4C / MHA / SIH-2026 — Sub-89ms Fraud Intercept Architecture     █
echo  █                                                                      █
echo  ████████████████████████████████████████████████████████████████████████
echo.

:: ── 1. Check Python ─────────────────────────────────────────────────────────
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo [ERROR] Python 3.10+ is required but not found in PATH.
    echo         Install from: https://python.org/downloads
    pause
    exit /b 1
)
for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do set PY_VER=%%v
echo [OK] Python %PY_VER% detected.

:: ── 2. Install / verify dependencies ────────────────────────────────────────
echo.
echo [*] Verifying Python dependencies...
python -c "import fastapi, uvicorn, pydantic, aiofiles" >nul 2>&1
if %errorlevel% neq 0 (
    echo [*] Installing required packages - first-time setup...
    pip install -q -r requirements.txt
    if %errorlevel% neq 0 (
        color 0C
        echo [ERROR] Failed to install dependencies. Check requirements.txt and pip.
        pause
        exit /b 1
    )
    echo [OK] Dependencies installed.
) else (
    echo [OK] All dependencies present.
)

:: ── 3. Synchronize frontend assets to static directory ─────────────────────
echo.
echo [*] Synchronizing frontend assets to backend/app/static/...
python sync_static.py
if %errorlevel% neq 0 (
    echo [WARN] Static sync encountered issues — some pages may not load.
)

:: ── 4. Initialize and seed the database ─────────────────────────────────────
echo.
echo [*] Seeding persistent sovereign case records...
python seed_user_complaints.py
if %errorlevel% neq 0 (
    echo [WARN] Seed script encountered issues — using pre-seeded DB if available.
)

:: ── 5. Open browser to the login portal once server is ready ───────────────
echo.
echo [*] Launching DURGAM Sovereign Portal browser watcher...
start "" /b python scripts\open_browser.py

:: ── 6. Print portal directory ────────────────────────────────────────────────
echo.
echo  ╔══════════════════════════════════════════════════════════════════════╗
echo  ║  DURGAM PORTAL DIRECTORY                                            ║
echo  ╠══════════════════════════════════════════════════════════════════════╣
echo  ║  Home / Login    http://127.0.0.1:8000/login.html                  ║
echo  ║  Citizen Desk    http://127.0.0.1:8000/citizen.html                ║
echo  ║  Police Radar    http://127.0.0.1:8000/police.html                 ║
echo  ║  Bank Console    http://127.0.0.1:8000/bank.html                   ║
echo  ║  Command Center  http://127.0.0.1:8000/command.html                ║
echo  ║  Judiciary Court http://127.0.0.1:8000/judiciary.html              ║
echo  ║  BSA Verify Vault http://127.0.0.1:8000/verify.html                ║
echo  ║  API Docs        http://127.0.0.1:8000/api/docs                    ║
echo  ║  Health Check    http://127.0.0.1:8000/health                      ║
echo  ╚══════════════════════════════════════════════════════════════════════╝
echo.
echo  [*] Starting FastAPI Uvicorn server on http://127.0.0.1:8000
echo  [!] Press CTRL+C to stop the server.
echo.

:: ── 7. Launch production-grade Uvicorn server ────────────────────────────────
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload --log-level info

pause
