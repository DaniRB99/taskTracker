#!/python3
import logging.config
import sys
import os
import json
import logging
import yaml # type: ignore
import argparse
from datetime import datetime


JSON_PATH:str = ".\\data.json"
MASK:str = "%d/%m/%Y %H:%M:%S"

logger:logging.Logger

#CLASE TASK
class task:
    #id sequential
    _idCounter:int = 0
    
    id:int
    name:str
    description:str
    status:str #"planned" | "ongoing" | "finished"
    createdAt:datetime
    updatedAt:datetime
    
    def __init__(self, obj:dict):
        self.id = obj["id"]
        self.name = obj["name"]
        self.description = obj["description"]
        self.status = obj["status"]
        self.createdAt = obj["createdAt"]
        self.updatedAt = obj["updatedAt"]
    
    @classmethod
    def new(cls, name:str, desc:str = ""):
        obj = {
            "id":cls.nextId(),
            "name":name,
            "description":desc,
            "status":"planned",
            "createdAt":datetime.now(),
            "updatedAt":datetime.now()
        }
        return cls(obj)

    @classmethod
    def load(cls, obj:dict):
        obj["createdAt"] = datetime.strptime(obj["createdAt"], MASK)
        obj["updatedAt"] = datetime.strptime(obj["updatedAt"], MASK)
        return cls(obj)
    
    @classmethod
    def nextId(cls) -> int:
        cls._idCounter+=1
        return cls._idCounter
    
    @classmethod
    def updateSequ(cls, lastId:int):
        cls._idCounter = lastId
    
    def toDict(self, detailledOutput:bool) -> dict:
        taskDict:dict
        if detailledOutput:
            taskDict = {
                "id":self.id,
                "name":self.name,
                "description":self.description,
                "status":self.status,
                "createdAt":self.createdAt.strftime(MASK),
                "updatedAt":self.updatedAt.strftime(MASK)
            }
        else:
            taskDict = {
                "(id) name":f"({self.id}) {self.name}"
            }
        return taskDict

#TASK_MANAGER
class taskManager:
    tasks:list[task]
    logger:logging
    
    def __init__(self, tasks:list = []):
        self.tasks = tasks
        self.iniSequential()
        self.logger = logging.getLogger("taskManager")
    
    def add(self, task_name:str, task_descrition:str = ""):
        newTask = task.new(task_name, task_descrition)
        self.tasks.append(newTask)
        self.updateJson()
        self.logger.debug(f"ADD (Id: {newTask.id})")
        print(f"New task added! (Id: {newTask.id})")
    
    def update(self, task_id:int, task_name:str = "", task_desc:str = "", newStatus:str="") -> str:
        changed:str = "ok"
        uptTask = self.findTask(task_id)
        if uptTask:
            uptTask.name = task_name if task_name != "" else uptTask.name
            uptTask.description = task_desc if task_desc != "" else uptTask.description
            statusOutput = self.change_status(task_id, newStatus)
            uptTask.updatedAt = datetime.now()
            self.updateJson()
            print(f"Task {task_id} updated! {statusOutput}")
        else:
            changed = "not found"
            print(f"!!! Task not found!")
        return changed
    
    def change_status(self, taskId:int, newStatus:str =""):
        if newStatus == "":
            return ""
        
        changed:str = "ok"
        myTask:task = self.findTask(taskId)
        if myTask:
            myTask.status = newStatus
            myTask.updatedAt = datetime.now()
            changed = f"New status: {newStatus}"
        else:
            changed = "not found"
        
        return changed
        
    def delete(self, taskId:int):
        popped:str = "Task no encontrada"
        for i, task in enumerate(self.tasks):
            if task.id == taskId:
                tasks.pop(i)
                self.updateJson()
                popped = f"Task con id: {task.id} ha sido eliminada"
                break
        return popped
        
    #FIXME: mejora de output -> salida de tarea con mejor formato
    def list(self, taskId:int=None, detailled:bool = False, indent:bool = True)-> dict:
        indentOutput:int = 4 if indent else None
        task = self.findTask(taskId)
        tasksList = [task] if task else self.tasks
        
        output:dict={}
        for onetask in tasksList:
            output[onetask.name] = onetask.toDict(detailled)
        print(json.dumps(output, indent=indentOutput))
    
    def findTask(self, taskId:int)->task | None:
        for i, onetask in enumerate(self.tasks):
            if onetask.id == taskId:
                return onetask
        return None
    
    def iniSequential(self):
        maxId:int = 0
        for taskSaved in self.tasks:
            if taskSaved.id > maxId:
                maxId = taskSaved.id
        task.updateSequ(maxId)
    
    def updateJson(self):
        newData = {}
        for task in self.tasks:
            newData[task.id] = task.toDict()
            
        with open(JSON_PATH, "w") as jsonIO:
            jsonIO.write(json.dumps(newData, indent=4))
    
#FILE_HANDLER
def loadJson()->dict:
    if not os.path.exists(JSON_PATH) or not os.path.isfile(JSON_PATH):
         with open(JSON_PATH, "w") as jsonIO:
             jsonIO.write(json.dumps({}, indent=4))
             return {}
         
    with open(JSON_PATH, "r") as jsonIO:
        return dict(json.loads(jsonIO.read()))

def loadTasks() -> list:
    taskDict = loadJson()
    tasks:list = []
    for key in taskDict.keys():
        tasks.append(task.load(taskDict[key]))
    
    return tasks
    

def arguments():
    parser = argparse.ArgumentParser(prog="Task Tracker Manager", 
                            description="Task to track the state of the tasks easily with commands via CLI", 
                            epilog="Contact with the email 'dani.rocamora.99@gmail.com' to solve any trouble detected")
    subparser = parser.add_subparsers(title="Functionalities", dest="action")
    
    add_par = subparser.add_parser("add", help="Add new task")
    add_par.add_argument("taskName")
    add_par.add_argument("-d", "--description")
    
    updt_par = subparser.add_parser("update", help="Update an existent task")
    updt_par.add_argument("taskId", type=int)
    updt_par.add_argument("-n", "--name", type=str)
    updt_par.add_argument("-d", "--description", type=str)
    updt_par.add_argument("-s", "--status", choices=["planned", "ongoing", "stuck", "finished"], type=int)
    
    del_par = subparser.add_parser("delete", help="Delete a task")
    del_par.add_argument("taskId", type=int)
    
    list_par = subparser.add_parser("list", help="List created tasks")
    list_par.add_argument("taskId",type=int, nargs="?")
    list_par.add_argument("-d","--detailled", action="store_true")
    return parser.parse_args()
    
#options add, update, delete, list
#TODO: USAR logging
#TODO: pasar por parámetro nombre con espacios, ej: "mi tarea"
#TODO: evolución del proyecto: conectar con un mongo ?¿
if __name__ == "__main__":
    with open("config.yaml", "rt") as f:
        config=yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    logger = logging.getLogger("development")
    
    logger.debug("Inicio")
    args = arguments()
    logger.debug(f"Arguments: {args}")

    tasks:list = loadTasks()
    manager = taskManager(tasks)
    
    match args.action:
        case "add":  
            manager.add(args.taskName, args.description)
        case "list":
            manager.list(args.taskId, args.detailled)
        case "update":
            manager.update(args.taskId, args.taskName,  args.description, args.status)
        case "delete":
            manager.delete(args.taskId)
    
    logger.debug("Fin")
    logger.debug("     ")