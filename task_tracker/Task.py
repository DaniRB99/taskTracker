from datetime import datetime
from enum import StrEnum, auto

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

class Task:
    #id sequential
    _idCounter:int = 0
    
    id:int
    name:str
    description:str
    status:Status 
    createdAt:datetime
    updatedAt:datetime
    
    MASK:str = "%d/%m/%Y %H:%M:%S"
    
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
        obj["createdAt"] = datetime.strptime(obj["createdAt"], cls.MASK)
        obj["updatedAt"] = datetime.strptime(obj["updatedAt"], cls.MASK)
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
                "createdAt":self.createdAt.strftime(self.MASK),
                "updatedAt":self.updatedAt.strftime(self.MASK)
            }
        
        return taskDict
    
    def toStr(self, detailled:bool = False):
        string = f"({self.id}) {self.name} - |{self.status.upper()}|"
        if detailled:
            string = string + f": [{self.description}] created: {self.createdAt} last update: {self.updatedAt}"
            
        return string 
    
    def _change_status(self, newStatus:Status):
        if Status._missing_(newStatus):
            self.status = newStatus
        
if __name__ == "__main__":
    print("Funcional...")