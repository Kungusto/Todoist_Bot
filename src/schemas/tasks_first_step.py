from pydantic import BaseModel, conint
from datetime import datetime

class TaskStepOneAdd(BaseModel) : 
    title : str
    description : str | None = None
    complation_due : datetime
    priority : conint(ge=1, le=4) # type: ignore

class TaskStepOne(TaskStepOneAdd) :
    id : int

class TaskStepOneEdit(BaseModel) :
    title : str | None = None
    description : str | None = None
    complation_due : datetime | None = None
    priority : conint(ge=1, le=4) | None = None # type: ignore 


