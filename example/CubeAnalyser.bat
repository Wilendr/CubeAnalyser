@echo off
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
    echo Python is not installed on this system.
    echo Please install Python 3.8 or later from https://www.python.org/downloads/
    pause
    exit /b
)

python program/main.py
pause
