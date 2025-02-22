from pydantic import BaseModel
from datetime import date

class UserAdd(BaseModel) :
    tg_id: int
    registrated: date

class User(UserAdd)  :
    id: int