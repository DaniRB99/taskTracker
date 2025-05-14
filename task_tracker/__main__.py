#!/python3
import logging.config
import logging
import yaml # type: ignore
import os
import argparse

from task_tracker.TaskRepository import TaskRepository, Status


#FIXME: FORMA INCORRECTA DE CARGAR FICHEROS EXTERNOS
# import importlib.resources

# with importlib.resources.files("task_tracker.data").joinpath("tareas.json").open("r", encoding="utf-8") as f:
#     contenido = f.read()

# try:
#     import importlib.resources as pkg_resources  # Python 3.9+
# except ImportError:
#     import importlib_resources as pkg_resources  # pip install importlib_resources

# from task_tracker import data

# with pkg_resources.open_text(data, "tareas.json") as f:
#     contenido = f.read()

def arguments():
    parser = argparse.ArgumentParser(prog="Task Tracker Manager", 
                            description="Task to track the state of the tasks easily with commands via CLI", 
                            epilog="Contact with the email 'dani.rocamora.99@gmail.com' to report any trouble detected")
    subparser = parser.add_subparsers(title="Functionalities", dest="action", required=True )
    
    add_par = subparser.add_parser("add", help="Add new task")
    add_par.add_argument("taskName")
    add_par.add_argument("-d", "--description")
    
    updt_par = subparser.add_parser("update", help="Update an existent task")
    updt_par.add_argument("taskId", type=int)
    updt_par.add_argument("-n", "--name", type=str)
    updt_par.add_argument("-d", "--description", type=str)
    updt_par.add_argument("-s", "--status", choices=[Status.to_list()])
    
    del_par = subparser.add_parser("delete", help="Delete a task")
    del_par.add_argument("taskId", type=int)
    
    list_par = subparser.add_parser("list", help="List created tasks")
    list_par.add_argument("--id",type=int)
    list_par.add_argument("-d","--detailled", action="store_true")
    list_par.add_argument("status",nargs='?',  choices=[Status.to_list()])
    
    newStatusParser = []
    for status in Status.to_list_mark():
        newStatusParser.append(subparser.add_parser(status, help="Change task status to " + Status.remove_mark(status)))
        newStatusParser[-1].add_argument("taskId", type=int)
    return parser.parse_args()

#Change the directory path to be able to read the config files
#Because task-tracker can be executed from anywhere
def changePathExec():
    chDirOutput = f"Executing script from {os.getcwd()}"
    dirScript = os.path.dirname(os.path.abspath(__file__))
    if os.getcwd() != dirScript:
        os.chdir(dirScript)
        chDirOutput = chDirOutput + f" -- Changed path to {os.getcwd()}"
    else:
        chDirOutput = "Path OK"
    return chDirOutput
 
def initLogger(configPath:str, logsPath:str):
    chPath = changePathExec()
    if not os.path.exists(logsPath):
        os.mkdir(logsPath)
    
    with open(configPath, "rt") as f:
        config=yaml.safe_load(f.read())
        logging.config.dictConfig(config) 
        
    logger = logging.getLogger(__name__)
    logger.debug("-"*30)
    logger.debug("Inicio")
    logger.debug(chPath)
    return logger

JSON_PATH:str = "data\\data.json"
CONFIG_PATH:str = "config\\config.yaml"
LOGS_PATH:str = "logs\\"

#options add, update, delete, list
#TODO: evolución del proyecto: conectar con un mongo ?¿
def main():
    logger = initLogger(CONFIG_PATH, LOGS_PATH)
    
    args = arguments()
    logger.debug(f"Arguments: {args}")
    manager = TaskRepository.loadTasks(JSON_PATH)
    
    match args.action:
        case "add":  
            manager.add(args.taskName, args.description)
        case "list":
            manager.list(args.id, args.detailled,args.status)
        case "update":
            manager.update(args.taskId, args.name,  args.description, args.status)
        case "delete":
            manager.delete(args.taskId)
        case _:
            if Status.remove_mark(args.action):
                manager.change_status(args.taskId, Status.remove_mark(args.action))

    logger.debug("Fin")
    logger.debug("     ")
    
if __name__ == "__main__":
    main()