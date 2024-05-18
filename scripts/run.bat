@echo off
python -m venv venv
call venv\Scripts\pip install -r requirements.txt
call venv\Scripts\activate
python src\main.py
deactivate
