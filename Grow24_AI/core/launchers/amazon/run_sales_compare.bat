@echo off
setlocal
set "PROJECT_ROOT=%~dp0..\..\..\.."
cd /d "%PROJECT_ROOT%"
set PYTHONIOENCODING=utf-8
set "PYTHON_EXE=%LocalAppData%\Programs\Python\Python311\python.exe"
if not exist "%PYTHON_EXE%" set "PYTHON_EXE=python"
"%PYTHON_EXE%" "ClaudeCode\Python\intraday_sales_v1.0.py"
endlocal
