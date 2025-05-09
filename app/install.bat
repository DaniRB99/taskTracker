@echo off
python -m venv ./venv

pip install -r requirements.txt

doskey task-tracker=%cd%\task-tracker.bat