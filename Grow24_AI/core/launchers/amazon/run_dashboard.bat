@echo off
setlocal
title Grow24 AI - Amazon Dashboard
color 0A
set "PROJECT_ROOT=%~dp0..\..\..\.."
cd /d "%PROJECT_ROOT%"

echo.
echo  ================================================
echo    Grow24 AI - Amazon Dashboard Launcher
echo  ================================================
echo.

set "PYTHON_EXE=%LocalAppData%\Programs\Python\Python311\python.exe"
if not exist "%PYTHON_EXE%" set "PYTHON_EXE=python"

echo  [1/3] Stopping old server (if any)...

:kill_loop
for /f "tokens=5" %%P in ('netstat -ano 2^>nul ^| findstr ":5000 " ^| findstr "LISTENING"') do (
    echo         Killing PID %%P
    taskkill /PID %%P /F >nul 2>&1
    goto kill_loop
)
timeout /t 2 /nobreak >nul

netstat -ano 2>nul | findstr ":5000 " | findstr "LISTENING" >nul
if %errorlevel%==0 (
    echo  [WARN] Port still busy, retrying...
    timeout /t 2 /nobreak >nul
    goto kill_loop
)
echo         Port 5000 is free.
echo.

echo  [2/3] Scheduling browser open...
start "" /min cmd /c "timeout /t 3 /nobreak >nul && start http://localhost:5000"

echo  [3/3] Starting Grow24 AI Amazon Dashboard server...
echo.
echo  ================================================
echo   Dashboard:    http://localhost:5000
echo   FBA Settings: http://localhost:5000/fba-settings
echo   Settings:     http://localhost:5000/settings
echo   Rules:        http://localhost:5000/rules
echo  ================================================
echo.

"%PYTHON_EXE%" "Grow24_AI\core\dashboard\dashboard_server_v1.1.py" --port 5000

echo.
echo  Server stopped.
pause
endlocal
