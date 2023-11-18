
@echo off

rem Set the path to your virtual environment activate script
set VENV_PATH=D:\python\FIle prep DDIS\venv\Scripts\activate

rem Activate the virtual environment
call "%VENV_PATH%"

rem Navigate to the directory of your Python script
cd /d D:\python\FIle prep DDIS

rem Run your Python script
python main.py

rem Deactivate the virtual environment (optional)
deactivate