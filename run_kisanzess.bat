@echo off
setlocal
chcp 65001 >nul
title KisanZess - Dual-Brain Agricultural Intelligence Agent

echo ===============================================================================
echo   🌾 KISANZESS: DUAL-BRAIN VERNACULAR AGRICULTURAL CO-PILOT
echo   Google Cloud | Code for Communities 2.0 (Track 4: Agriculture)
echo ===============================================================================
echo.
echo   [1] Run 7-Query Dual-Brain Pipeline Demo (Terminal)
echo   [2] Launch KisanZess Web Command Matrix Dashboard
echo   [3] Train Crop & Fertilizer Scikit-Learn ML Models
echo   [4] Open Hackathon Presentation Pitch Deck (.pptx)
echo   [5] Run Full Automated Test Suite (17 Tests)
echo   [6] Exit
echo.
set /p choice="Select an option [1-6]: "

if "%choice%"=="1" (
    echo.
    echo Running KisanZess Pipeline...
    python -X utf8 examples\04_kisanzess_agent.py
    pause
    goto :eof
)

if "%choice%"=="2" (
    echo.
    echo Freeing port 8000 if occupied...
    for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do taskkill /f /pid %%a >nul 2>&1
    echo Launching KisanZess Web Matrix on http://localhost:8000 ...
    start http://localhost:8000
    python -m reflex_agent.cli.main ui --port 8000
    goto :eof
)

if "%choice%"=="3" (
    echo.
    echo Training Crop & Fertilizer ML Models...
    python -m reflex_agent.ml.crop_recommendation_trainer
    python -m reflex_agent.ml.fertilizer_prediction_trainer
    echo Training complete!
    pause
    goto :eof
)

if "%choice%"=="4" (
    echo.
    echo Opening Comprehensive Viva & Pitch Deck...
    if exist "C:\Users\ROSHNI\OneDrive\Documents\GitHub\l-data-seT---ML\Comprehensive_Viva_Crop_Fertilizer_ML.pptx" (
        start "" "C:\Users\ROSHNI\OneDrive\Documents\GitHub\l-data-seT---ML\Comprehensive_Viva_Crop_Fertilizer_ML.pptx"
    ) else (
        echo Presentation deck not found.
    )
    goto :eof
)

if "%choice%"=="5" (
    echo.
    echo Running Pytest Suite...
    python -m pytest tests\ -p no:cacheprovider
    pause
    goto :eof
)

echo Exiting...

