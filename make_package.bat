@echo off
echo ====== Construyendo el paquete task-tracker ======
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
python -m build
echo.
echo => Paquete generado en la carpeta 'dist\'
pause
