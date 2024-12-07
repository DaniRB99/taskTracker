#!/python3
import sys
from datetime import datetime
import os
import json

JSON_PATH:str = ".\\data.json"

#CLASE TASK

#TASK_MANAGER
class task:
    #id sequential
    idCounter:int = 0
    
    id:int
    name:str
    description:str
    status:str #"planned" | "ongoing" | "finished"
    createdAt:datetime
    updatedAt:datetime
    
    def __init__(self, name:str) -> None:
        self.name = name
        self.id = self.nextId()
        self.description = ""
        self.status = "planned"
        self.createdAt = datetime.now()
        self.updatedAt = datetime.now()

    def __init__(self, obj:dict) -> None:
        self.id = obj["id"]
        self.name = obj["name"]
        self.description = obj["description"]
        self.status = obj["status"]
        self.createdAt = obj["createdAt"]
        self.updatedAt = obj["updatedAt"]
    
    def nextId(self) -> int:
        task.idCounter+=1
        return task.idCounter
    
    def toDict(self) -> dict:
        taskDict:dict = {
            "id":self.id,
            "name":self.name,
            "description":self.description,
            "status":self.status,
            "createdAt":self.createdAt.strftime("%d/%m/%Y %H:%M:%S"),
            "updatedAt":self.updatedAt.strftime("%d/%m/%Y %H:%M:%S")
        }
        return taskDict

#FILE_HANDLER
def loadJson()->dict:
    if not os.path.exists(JSON_PATH) or not os.path.isfile(JSON_PATH):
         with open(JSON_PATH, "w") as jsonIO:
             jsonIO.write(json.dumps({}, indent=4))
             return {}
         
    with open(JSON_PATH, "r") as jsonIO:
        return dict(json.loads(jsonIO.read()))

def loadTasks() -> list[task]:
    taskDict = loadJson()
    tasks:list = []
    for key in taskDict.keys():
        tasks.append(task(taskDict[key]))
    
    return tasks
    
def updateJson(newData:dict):
    with open(JSON_PATH, "w") as jsonIO:
        jsonIO.write(json.dumps(newData, indent=4))
        

#options add, update, delete, list
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("No operation argument indicated")
        print("Use example: \n\n\t> python main.py add myNewTask\n")
        exit(code=1)
    
    tasks:list = loadTasks()
    print(f"Tasks readed: {tasks}")
    if sys.argv[1] == "add":        
        newTask = task(sys.argv[2])
        print(f"New task added! (Id: {newTask.id})")
        tasks[newTask.id] = newTask.toDict()
        updateJson(tasks)
        
    elif sys.argv[1] == "list":
        for onetask in tasks:
            print(onetask )
    elif sys.argv[1] == "update":
        pass
    elif sys.argv[1] == "delete":
        pass