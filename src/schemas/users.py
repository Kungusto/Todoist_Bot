from pydantic import BaseModel
from datetime import date

class UserAdd(BaseModel) : 
    tg_id: int
    registrated: date
    password: str

class UserAddWithHashedPassword(BaseModel) : # пока не актуально
    tg_id: int
    registrated: date
    hashed_password: str

class User(BaseModel)  :
    id: int
    tg_id: int
    registrated: date

class UserEdit(BaseModel) : 
    tg_id: str | None = None
    registration: date | None = None