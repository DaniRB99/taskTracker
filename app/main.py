#!/python3
import logging.config
import logging
import yaml # type: ignore
import os
import json
import argparse
from datetime import datetime
from enum import StrEnum, auto


JSON_PATH:str = ".\\data.json"
MASK:str = "%d/%m/%Y %H:%M:%S"

logger:logging.Logger

#ENUM STATUS
class Status(StrEnum):
    TODO = auto()
    IN_PROGRESS = auto()
    FINISHED = auto()
    
    @classmethod
    def to_list(cls)-> list:
        outputList:list = list()
        for i, value in enumerate(cls):            
            outputList.append(value.name)
        return outputList
    
    #does the value exists in the enum
    @classmethod
    def _missing_(cls, value):
        try:
            value = value.lower()
        except:
            return None
        
        for status in list(cls):
            if status.value == value:
                return status
        return None
    
    #functions to manage status output in the arguments
    @classmethod
    def to_list_mark(cls)-> list:
        return list(map(cls.add_mark, cls.to_list()))
    
    @classmethod
    def _mark_value(cls):
        return "mark_"
    
    @classmethod
    def add_mark(cls, value):
        return cls._mark_value()+str.lower(value)
    
    @classmethod
    def remove_mark(cls,value:str):
        unmarked_value = str(value[value.find(cls._mark_value())+len(cls._mark_value()):].upper())
        return cls._missing_(unmarked_value)

#CLASE TASK
class Task:
    #id sequential
    _idCounter:int = 0
    
    id:int
    name:str
    description:str
    status:Status 
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
            "status":Status.TODO,
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
        taskDict:dict
        taskDict = {
                "id":self.id,
                "name":self.name,
                "description":self.description,
                "status":self.status,
                "createdAt":self.createdAt.strftime(MASK),
                "updatedAt":self.updatedAt.strftime(MASK)
            }
        
        return taskDict
    
    def toStr(self, detailled:bool = False):
        string = f"({self.id}) {self.name} - |{self.status.upper()}|"
        if detailled:
            string = string + f": [{self.description}] created: {self.createdAt} last update: {self.updatedAt}"
            
        return string 
        
#TASK_MANAGER
class TaskManager:
    tasks:list[Task]
    logger:logging
    
    def __init__(self, tasks:list = []):
        self.tasks = tasks
        self.iniSequential()
        self.logger = logging.getLogger("taskManager")
    
    def add(self, taskName:str, taskDesc:str = ""):
        self.logger.debug(f"Adding new task {taskName}")
        newTask = Task.new(taskName, taskDesc)
        self.tasks.append(newTask)
        self.updateJson()
        self.logger.debug(f"ADD (Id: {newTask.id})")
        print(f"New task added! (Id: {newTask.id})")
    
    def update(self, taskId:int, taskName:str = "", taskDesc:str = "", newStatus:Status="") -> str:
        self.logger.debug(f"Updating task {taskId}")
        changed:str = "ok"
        uptTask = self.findTask(taskId)
        if uptTask:
            uptTask.name = taskName if taskName else uptTask.name
            uptTask.description = taskDesc if taskDesc else uptTask.description
            statusOutput = self._change_status(taskId, newStatus)
            uptTask.updatedAt = datetime.now()
            self.updateJson()
            print(f"Task {taskId} updated!")
        else:
            changed = "not found"
            print(f"!!! Task not found!")
        return changed
    
    def _change_status(self, taskId:int, newStatus:Status):
        self.logger.debug(f"Changing status of task {taskId}")
        changed:str = "ok"
        myTask:Task = self.findTask(taskId)
        if myTask and Status._missing_(newStatus):
            myTask.status = newStatus
            myTask.updatedAt = datetime.now()
            changed = f"New status: {newStatus.name}"
        else:
            changed = "not found"

        return changed
    
    def change_status(self, taskId:int, newStatus:Status):
        uptTask = self.findTask(taskId)
        if uptTask:
            changed = self._change_status(taskId, newStatus)
            uptTask.updatedAt = datetime.now()
            self.updateJson()
            print(f"Task {taskId} marked as {newStatus}!")
        else:
            changed = "not found"
            print(f"!!! Task not found!")
        return changed
        
    def delete(self, taskId:int):
        self.logger.debug(f"Deleting task {taskId}")
        popped:str = "Task not found"
        task = self.findTask(taskId)
        try:
            self.tasks.remove(task)
            self.updateJson()
            popped = f"Task deleted successfully (ID:{task.id})"
            print(popped)
        except ValueError:
            popped = f"Task not found! (ID:{taskId})"
            print(popped)

        return popped
        
    def list(self, taskId:int=None, detailled:bool = False, status:Status = None)-> dict:
        self.logger.debug(f"Listing {taskId}")
        task = self.findTask(taskId)
        tasksList = [task] if task else self.tasks
        
        print("(id) task_name - |status|\n")
        for onetask in filter((lambda task, st=status: self.isStatus(task,st)), tasksList):
            print(onetask.toStr(detailled))
    
        
    def findTask(self, taskId:int)->Task | None:
        for i, onetask in enumerate(self.tasks):
            if onetask.id == taskId:
                return onetask
        return None
    
    #Status == None -> True
    #Status -> filter by argument status
    def isStatus(self, task:Task, status:Status):
        return task.status == status or status is None
    
    def iniSequential(self):
        maxId:int = 0
        for taskSaved in self.tasks:
            if taskSaved.id > maxId:
                maxId = taskSaved.id
        Task.updateSequ(maxId)
    
    def updateJson(self):
        newData = {}
        for task in self.tasks:
            newData[task.id] = task.toDict()
            
        with open(JSON_PATH, "w") as jsonIO:
            jsonIO.write(json.dumps(newData, indent=4))
    
#FILE_HANDLER
def loadJson()->dict:
    #create json if it does not exist
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
        tasks.append(Task.load(taskDict[key]))
    
    return tasks
    

def arguments():
    parser = argparse.ArgumentParser(prog="Task Tracker Manager", 
                            description="Task to track the state of the tasks easily with commands via CLI", 
                            epilog="Contact with the email 'dani.rocamora.99@gmail.com' to solve any trouble detected")
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
    
    for status in Status.to_list_mark():
        newStatusParser = subparser.add_parser(status, help="Change task status to " + Status.remove_mark(status))
        newStatusParser.add_argument("taskId", type=int)
    return parser.parse_args()

#Change the directory path to be able to read the config files
#Because task-tracker can be execute from anywhere
def changePathExec():
    chDirOutput = f"Executing script from {os.getcwd()}"
    dirScript = os.path.dirname(os.path.abspath(__file__))
    if os.getcwd() != dirScript:
        os.chdir(dirScript)
        chDirOutput = chDirOutput + f" -- Changed path to {os.getcwd()}"
    else:
        chDirOutput = "Path OK"
    return chDirOutput
 
#options add, update, delete, list
#TODO: evolución del proyecto: conectar con un mongo ?¿
#todo:  .BAT PARA EJECUTAR EL PROGRAMA
if __name__ == "__main__":
    chPath = changePathExec()
    
    with open("config.yaml", "rt") as f:
        config=yaml.safe_load(f.read())
        logging.config.dictConfig(config) 
    logger = logging.getLogger("development")
    logger.debug("-"*30)
    logger.debug("Inicio")
    logger.debug(chPath)
    output:str
    args = arguments()
    logger.debug(f"Arguments: {args}")
    tasks:list = loadTasks()
    manager = TaskManager(tasks)
    
    match args.action:
        case "add":  
            output = manager.add(args.taskName, args.description)
        case "list":
            output = manager.list(args.id, args.detailled,args.status)
        case "update":
            output = manager.update(args.taskId, args.name,  args.description, args.status)
        case "delete":
            output = manager.delete(args.taskId)
        case _:
            if Status.remove_mark(args.action):
                output = manager.change_status(args.taskId, Status.remove_mark(args.action))

    logger.debug(f"output: {output}")
    logger.debug("Fin")
    logger.debug("     ")