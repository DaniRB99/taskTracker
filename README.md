# TaskTracker
Herramienta para planificar tareas y registrar su progreso. El progreso de las diferentes tareas se puede guardar como planificado, en progreso o finalizado. El programa permite generar, actualizar y borrar las tareas creadas, además de ir cambiando el estado según se avance con la tarea.

Esta aplicación es CLI por lo que está pensado para su uso a través de terminal. Se pueden seguir los pasos de instalación y configuración para su uso.

El proyecto tiene como finalidad el estudio de Python y alguna librería como, Argparse, que se utiliza para gestionar los argumentos pasados al programa. Lo más interesante es permitir configurar los argumentos requeridos según a la funcionalidad que se necesite utilizar, al estilo del funcionamiento de argumentos de Git.

## USO
Con cada llamada que realizado al programa con la acción requerida esta se efectua y se guardan los cambios en el JSON que tiene adjunto (data.json). En este fichero se guardará todos los datos de las tareas.

Para conocer los argumentos que se pueden utilizar el comando *--help*. Esto indicará las posibles acciones, y usando *--help* con la acción se indicará que argumentos opcionales y obligatorios existen.


## INSTALLATION STEPS

Clone the repository on local

Move to the folder of the project and open a terminal

Create virtual enviroment
> python -m venv ./venv

Install requirements
> pip -m install requirements.txt

Execute
> python main.py --help