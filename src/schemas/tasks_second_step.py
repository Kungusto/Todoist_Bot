from datetime import datetime
from pydantic import BaseModel


class TaskStepTwoAdd(BaseModel) : 
    id_super_task: int
    title : str
    description : str | None = None
    complation_due : datetime
    priority : conint(ge=1, le=4) # type: ignore

class TaskStepTwo(BaseModel) : 
    id: int
    id_super_task: int
    title : str
    description : str | None = None
    complation_due : datetime
    priority : conint(ge=1, le=4) # type: ignore

class TaskStepTwoEdit(BaseModel) :
    id_super_task: int | None = None
    title : str | None = None
    description : str | None = None 
    complation_due : datetime | None = None
    priority : conint(ge=1, le=4) | None = None # type: ignore
