@echo off
title ULPF - Universal Log Pre-processing Framework
echo =========================================================
echo   ULPF - Universal Log Pre-processing Framework
echo   Opening at http://localhost:8000
echo =========================================================
set PYTHONPATH=src
if exist .venv\Scripts\python.exe (
    .venv\Scripts\python.exe -m main api
) else (
    python -m main api
)
if errorlevel 1 (
    echo.
    echo Server stopped with error.
    pause
)
