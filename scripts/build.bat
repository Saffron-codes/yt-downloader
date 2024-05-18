@echo off
pip show pyinstaller >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    pip install pyinstaller
)

pyinstaller --onefile src\main.py

IF %ERRORLEVEL% EQU 0 (
    echo PyInstaller finished successfully.
) ELSE (
    echo PyInstaller encountered an error.
)

pause
