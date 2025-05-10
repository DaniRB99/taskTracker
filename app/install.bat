@echo off
python -m venv ./venv

pip install -r %cd%\requirements.txt

doskey task-tracker=%cd%\task-tracker.bat