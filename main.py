#!/python3
import logging.config
import sys
import os
import json
import logging
import yaml
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
    
    def toDict(self) -> dict:
        taskDict:dict = {
            "id":self.id,
            "name":self.name,
            "description":self.description,
            "status":self.status,
            "createdAt":self.createdAt.strftime(MASK),
            "updatedAt":self.updatedAt.strftime(MASK)
        }
        return taskDict

#TASK_MANAGER
class taskManager:
    tasks:list[task]
    
    def __init__(self, tasks:list = []):
        self.tasks = tasks
        self.iniSequential()
    
    def add(self, task_name:str, task_descrition:str = ""):
        newTask = task.new(task_name, task_descrition)
        self.tasks.append(newTask)
        self.updateJson()
        
        return newTask.id
    
    def update(self, task_id:int, task_name:str = "", task_desc:str = "") -> str:
        changed:str = "ok"
        uptTask = self.findTask(task_id)
        if uptTask:
            uptTask.name = task_name if task_name != "" else uptTask.name
            uptTask.description = task_desc if task_desc != "" else uptTask.description
            uptTask.updatedAt = datetime.now()
            self.updateJson()
        else:
            changed = "not found"
        return changed
    
    def change_status(self, taskId:int, newStatus:str):
        changed:str = "ok"
        myTask:task = self.findTask(taskId)
        if myTask:
            myTask.status = newStatus
            myTask.updatedAt = datetime.now()
            return changed
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
    def list(self, indent:bool = True)-> dict:
        output={}
        indentOutput:int = 4 if indent else None
        for onetask in manager.tasks:
            output[onetask.name] = onetask.toDict()
        return json.dumps(output, indent=indentOutput)
    
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
    argparse.ArgumentParser(prog="Task Tracker Manager", 
                            description="Task to track the state of the tasks easily with commands via CLI", 
                            epilog="Contact with the email 'dani.rocamora.99@gmail.com' to solve any trouble detected")
    
    
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
    
    operation:str
    argument:str
    
    #TODO: mejorar tratamiento de argumentos (USAR ARGPARSE)
    if len(sys.argv) < 3 and sys.argv[1] in ("add", "update", "delete"):
        logger.info("No operation argument indicated")
        logger.info("Use example: \n\n\t> python main.py add myNewTask\n")
        exit(code=1)
    else:
        logger.info(f"Parametros: {sys.argv}")
        operation = sys.argv[1]
        if len(sys.argv) < 3:
            argument = ""
        else:
            argument = sys.argv[2]
    
    tasks:list = loadTasks()
    manager = taskManager(tasks)
    logger.debug(f"Tasks readed: {manager.list(indent=False)}")
    
    if operation == "add":        
        taskId = manager.add(argument) #falta pasar description
        logger.debug(f"ADD (Id: {taskId})")
        print(f"New task added! (Id: {taskId})")
      
    elif operation  == "list":
        print(manager.list())
            
    #TODO: identificar el campo a actualizar
    elif operation  == "update":
        print(manager.update(int(argument)))
    
    elif operation  == "delete":
        print(manager.delete(int(argument)))
    
    logger.debug("Fin")
    logger.debug("     ")