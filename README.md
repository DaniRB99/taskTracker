# TaskTracker


<div align="center">
    <img alt="GitHub Repo Name" src="https://img.shields.io/badge/Task_Tracker-yellow">
    <img alt="GitHub Author" src="https://img.shields.io/badge/Author-Daniel_Rocamora_Bru-b3bd1d?style=flat&color=b3bd1d">
    <img alt="GitHub commit-activity" src="https://img.shields.io/github/commit-activity/t/DaniRB99/taskTracker?color=red">
    <img alt="GitHub Created At" src="https://img.shields.io/github/created-at/DaniRB99/taskTracker?color=569414">
    <!--<img alt="GitHub Last Commit" src="https://img.shields.io/github/last-commit/yashksaini-coder/Task-Tracker">
    <img alt="GitHub Repo Size" src="https://img.shields.io/github/repo-size/yashksaini-coder/Task-Tracker">
    <img alt="GitHub License" src="https://img.shields.io/github/license/yashksaini-coder/Task-Tracker">
    <img alt="GitHub Open Issues" src="https://img.shields.io/github/issues/yashksaini-coder/Task-Tracker">
    <img alt="GitHub Closed Issues" src="https://img.shields.io/github/issues-closed/yashksaini-coder/Task-Tracker">
    <img alt="GitHub Open PR" src="https://img.shields.io/github/issues-pr/yashksaini-coder/Task-Tracker">
    <img alt="GitHub Closed PR" src="https://img.shields.io/github/issues-pr-closed/yashksaini-coder/Task-Tracker">
    <img alt="GitHub Forks" src="https://img.shields.io/github/forks/yashksaini-coder/Task-Tracker">
    <img alt="GitHub Stars" src="https://img.shields.io/github/stars/yashksaini-coder/Task-Tracker">
    <img alt="GitHub Watchers" src="https://img.shields.io/github/watchers/yashksaini-coder/Task-Tracker">
    <img alt="GitHub language count" src="https://img.shields.io/github/languages/count/yashksaini-coder/Task-Tracker">-->
</div>
<br>

<div align='center' style=" display: grid;">

  [![Gmail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:dani.rocamora.99@gmail.com)
  [![Github](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/DaniRB99)
  [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/drocamorabru/)
<!--[![Instagram](https://img.shields.io/badge/Instagram-%23FF006E.svg?style=for-the-badge&logo=Instagram&logoColor=white)](https://www.instagram.com/yashksaini.codes/)-->
  <!--[![X](https://img.shields.io/badge/X-%23000000.svg?style=for-the-badge&logo=X&logoColor=white)](https://twitter.com/EasycodesDev) -->
</div>

Herramienta para planificar tareas y registrar su progreso. El progreso de las diferentes tareas se puede guardar como planificado, en progreso o finalizado. El programa permite generar, actualizar y borrar las tareas creadas, además de ir cambiando el estado según se avance con la tarea.

<div align="center">
    <img src="images/tasktrack_img.png" alt="Task Tracker CLI" width="300"/>
</div>

Esta aplicación es CLI, por lo que está pensado para su uso a través de terminal. Se pueden seguir los pasos de instalación y configuración.

El proyecto tiene como finalidad el estudio de Python y alguna librería como, Argparse, que se utiliza para gestionar los argumentos pasados al programa. Lo funcionalidad más interesante que aporta es permitir configurar los argumentos requeridos según la funcionalidad a la que se llame, al estilo de la gestión de argumentos de Git.  Además, proporciona seguridad sobre los argumentos que se recibe en el script y evitar inyecciones maliciosas.

## USO
Con cada llamada que realizado al programa con la acción requerida esta se efectua y se guardan los cambios en el JSON que tiene adjunto (data.json). En este fichero se guardará todos los datos de las tareas.

Para conocer los argumentos que se pueden utilizar el comando *--help*. Esto indicará las posibles acciones, y usando *--help* con la acción se indicará que argumentos opcionales y obligatorios existen.

### Ejemplos de uso

> Añadiendo una nueva tarea 

`task_tracker add "Organizar carpetas" -d "Organizar las carpetas del proyecto para que sea visualmente más bonito"`

    New task added! (Id: 9)

---
> Cambiar el estado de la tarea

`task_tracker mark_in_progress 9`
    
    Task 9 marked as in_progress!

---
> Listar las tareas guardadas

`task_tracker list`

    (id) task_name - |status|

    (9) Organizar carpetas - |IN_PROGRESS|

## Pasos de instalación

> Clonar repositorio en local
------
> Abrir una terminal dentro de la carpeta del proyecto
------
> Ejecutar script constructor del paquete

``.\make_package.bat``

> Ejecutar script de instalación

``.\install_package.bat``

---
> Probar funcionamiento

``task_tracker --help``

---

> Ya está listo para su uso.
> Se puede ejecutar desde cualquier terminal con el nombre *task_tracker*

### Project based on [roadmap.sh](https://roadmap.sh/projects/task-tracker)

### License [MIT](https://mit-license.org/)