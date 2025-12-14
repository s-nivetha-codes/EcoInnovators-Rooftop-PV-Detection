@echo off
REM Solar Panel Verification System Launcher for Windows
REM This batch file provides easy access to the application

setlocal enabledelayedexpansion

cls
echo.
echo ================================================================
echo       SOLAR PANEL INSTALLATION VERIFICATION SYSTEM
echo               PM Surya Ghar Yojana Tool
echo ================================================================
echo.
echo Choose an option:
echo.
echo   1. Launch GUI (Tkinter) - Recommended for users
echo   2. Launch GUI (PySimpleGUI) - Modern interface
echo   3. View Quick Start Guide
echo   4. Run System Tests
echo   5. Command-Line Interface
echo   6. Exit
echo.

set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" (
    echo.
    echo Launching Tkinter GUI...
    echo.
    python gui_tkinter.py
) else if "%choice%"=="2" (
    echo.
    echo Launching PySimpleGUI...
    echo.
    python gui_app.py
) else if "%choice%"=="3" (
    echo.
    python QUICKSTART.py
    echo.
    pause
) else if "%choice%"=="4" (
    echo.
    echo Running system tests...
    echo.
    python test_system.py
    echo.
    pause
) else if "%choice%"=="5" (
    echo.
    echo Command-Line Interface
    echo.
    echo Usage: python main.py "image_path" [--satellite-image "sat_image"]
    echo.
    echo Example:
    echo   python main.py "C:\Users\amith\Downloads\home.jpg"
    echo.
    pause
) else if "%choice%"=="6" (
    echo Exiting...
    exit /b 0
) else (
    echo Invalid choice. Please try again.
    pause
    goto :start
)

echo.
echo ================================================================
echo Press any key to return to menu...
echo ================================================================
pause
cls
goto :start

:end
endlocal
