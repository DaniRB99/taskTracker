import os
import json
import logging
from datetime import datetime
from task_tracker.Task import Task, Status
from pathlib import Path

class TaskRepository:
    tasks:list[Task]
    logger:logging
    jsonPath:str
    
    def __init__(self, tasks:list = []):
        self.tasks = tasks
        self.iniSequential()
        self.logger = logging.getLogger("TaskRepository")
    
    @classmethod
    def loadJson(cls, jsonPath:str)->dict:
        if not os.path.exists(jsonPath):
            os.makedirs(jsonPath[:jsonPath.find("\\")])
        if not os.path.exists(jsonPath) or not os.path.isfile(jsonPath):
            with open(jsonPath, "w") as jsonIO:
                jsonIO.write(json.dumps({}, indent=4))
                return {}
            
        with open(jsonPath, "r") as jsonIO:
            return dict(json.loads(jsonIO.read()))
    
    @classmethod
    def loadTasks(cls, jsonPath:str):
        taskDict = cls.loadJson(jsonPath)
        cls.jsonPath = jsonPath
        tasks:list = []
        for key in taskDict.keys():
            tasks.append(Task.load(taskDict[key]))
        return cls(tasks)
    
    def add(self, taskName:str, taskDesc:str = ""):
        self.logger.debug(f"Adding new task {taskName}")
        newTask = Task.new(taskName, taskDesc)
        self.tasks.append(newTask)
        self.updateJson()
        self.logger.debug(f"ADD (Id: {newTask.id})")
        print(f"New task added! (Id: {newTask.id})")
    
    def update(self, taskId:int, taskName:str = "", taskDesc:str = "") -> str:
        self.logger.debug(f"Updating task {taskId}")
        uptTask = self.findTask(taskId)
        if not uptTask:
            print(f"!!! Task not found!")
            return
        
        uptTask.name = taskName if taskName else uptTask.name
        uptTask.description = taskDesc if taskDesc else uptTask.description
        uptTask.updatedAt = datetime.now()
        self.updateJson()
        print(f"Task {taskId} updated!")
    
    def change_status(self, taskId:int, newStatus:Status):
        self.logger.debug(f"Changing status of task {taskId} to {newStatus}")
        uptTask = self.findTask(taskId)
        if not uptTask:
            print(f"!!! Task not found!")
            return
        
        uptTask._change_status(newStatus)
        uptTask.updatedAt = datetime.now()
        self.updateJson()
        print(f"Task {taskId} marked as {newStatus}!")
        
    def delete(self, taskId:int):
        self.logger.debug(f"Deleting task {taskId}")
        task = self.findTask(taskId)
        try:
            self.tasks.remove(task)
            self.updateJson()
            print(f"Task deleted successfully (ID:{task.id})")
        except ValueError as err:
            self.logger.debug(f"Task not found {taskId}: {err.args[0]}")
            print(f"Task not found! (ID:{taskId})")
    
    #TODO: Mejora de output: que se muestren las columnas organizadas para cada campo
    def list(self, taskId:int=None, detailled:bool = False, status:Status = None)-> dict:
        self.logger.debug(f"Listing {taskId}")
        task = self.findTask(taskId)
        tasksList = [task] if task else self.tasks
        
        print("(id) task_name - |status|")
        print("-------------------------")
        for onetask in filter((lambda task, st=status: self.isStatus(task,st)), tasksList):
            print(onetask.toStr(detailled))
    
        
    def findTask(self, taskId:int)->Task | None:
        for i, onetask in enumerate(self.tasks):
            if onetask.id == taskId:
                return onetask
        return None
    
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
            
        with open(self.jsonPath, "w") as jsonIO:
            jsonIO.write(json.dumps(newData, indent=4))
    
if __name__ == "__main__":
    manager = TaskRepository.loadTasks("data\\tasks.json")