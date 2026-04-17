@echo off
setlocal
set "PROJECT_ROOT=%~dp0..\..\..\.."
cd /d "%PROJECT_ROOT%"
set PYTHONIOENCODING=utf-8
set "PYTHON_EXE=%LocalAppData%\Programs\Python\Python311\python.exe"
if not exist "%PYTHON_EXE%" set "PYTHON_EXE=python"
"%PYTHON_EXE%" "Grow24_AI\marketplaces\amazon\seller_api\listing_health\top_listing_monitor_v1.1.py" --top 0
endlocal
