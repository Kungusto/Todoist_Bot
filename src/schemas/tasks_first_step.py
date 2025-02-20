from pydantic import BaseModel
from datetime import datetime

class TaskStepOneAdd(BaseModel) : 
    title : str
    description : str | None = None
    complation_due : datetime
    priority : int

class TaskStepOne(TaskStepOneAdd) :
    id : int
