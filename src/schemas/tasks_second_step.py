from datetime import datetime
from pydantic import BaseModel
from pydantic import conint

class TaskStepTwoAdd(BaseModel) : 
    id_super_task: int
    title : str

class TaskStepTwo(BaseModel) : 
    id: int
    id_super_task: int
    title : str

class TaskStepTwoEdit(BaseModel) :
    id_super_task: int | None = None
    title : str | None = None
