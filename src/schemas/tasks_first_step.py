from pydantic import BaseModel, conint
from datetime import datetime

class TaskStepOneAdd(BaseModel) :
    user_id: str  # Добавляем user_id
    title : str
    description : str | None = None
    complation_due : datetime | None = None
    priority : conint(ge=1, le=3) | None = None # type: ignore
    status : conint(ge=1, le=4) | None = None

class TaskStepOne(TaskStepOneAdd) :
    id : int

class TaskStepOneEdit(BaseModel) :
    user_id: str | None = None
    title : str | None = None
    description : str | None = None
    complation_due : datetime | None = None
    priority : conint(ge=1, le=3) | None = None # type: ignore
    status : conint(ge=1, le=4) | None = None


