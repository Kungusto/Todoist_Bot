from pydantic import BaseModel
from datetime import datetime

class Notification(BaseModel) :
    id : int
    user_id: int
    title: str
    time: datetime
    
class NoficicationAdd(BaseModel) :
    user_id: int
    title: str
    time: datetime
    
class NotificationEdit(BaseModel) :
    user_id: int | None = None
    title: str | None = None
    time: datetime | None = None
