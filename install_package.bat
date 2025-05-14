@echo off
echo ====== Instalando el paquete task-tracker ======

REM Activar entorno virtual si existe
IF EXIST venv (
    call venv\Scripts\activate
) ELSE (
    echo !!! No se encontró el entorno virtual 'venv'.
    echo Puedes crear uno con: python -m venv venv
    pause
    exit /b
)

REM Buscar el archivo .whl en dist\
for /f %%i in ('dir /b /s dist\task_tracker-*.whl') do (
    set "WHEEL=%%i"
    goto :found
)

:found
if not defined WHEEL (
    echo !!! No se encontró un archivo .whl en la carpeta dist\
    pause
    exit /b
)

REM Instalar el paquete
pip install "%WHEEL%" --force-reinstall

echo.
echo == task_tracker instalado correctamente.
echo Ejecuta "task_tracker" desde cualquier terminal.
pause
