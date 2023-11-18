@echo off

rem Run PowerShell script to set environment variables from .env
powershell -Command "& {Get-Content '.env' | ForEach-Object { [System.Environment]::SetEnvironmentVariable($_.Split('=')[0], $_.Split('=')[1]) }}"

rem Navigate to the directory of your Python script
cd /d %ROOT_PATH%

rem Activate the virtual environment
call "%VENV_PATH%"

rem Run your Python script
python main.py

rem Deactivate the virtual environment (optional)
deactivate
