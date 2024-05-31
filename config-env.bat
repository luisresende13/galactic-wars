@echo off
REM Install Python Virtual Environment (venv)
python -m venv venv

REM Activate the Virtual Environment
venv\Scripts\activate

REM Install Required Dependencies from requirements.txt
pip install -r requirements.txt

REM Optional: Display a message
echo Environment setup completed!
