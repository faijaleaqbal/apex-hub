@echo off
cd /d "%~dp0"
title Apex Hub - Gaming Peripheral Control Suite

if exist "%LOCALAPPDATA%\Programs\ApexHub\ApexHub.exe" (
    start "" "%LOCALAPPDATA%\Programs\ApexHub\ApexHub.exe"
) else (
    start "" python run_app.py
)
exit
