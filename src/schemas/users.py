from pydantic import BaseModel
from datetime import date


class UserAdd(BaseModel) :
    tg_id: str
    nickname: str
    registrated: date
    password: str

class UserAddWithHashedPassword(BaseModel) : # пока не актуально
    tg_id: str
    registrated: date
    hashed_password: str

class User(BaseModel)  :
    id: int
    tg_id: str
    nickname: str
    registrated: date
    password: str

class UserEdit(BaseModel) :
    tg_id: str | None = None
    nickname: str | None = None
    #registration: date | None = None не нужно т.к. пользователю незачем изменять дату регистрации
    password: str | None = None

class AllInfoAboutUser(BaseModel) :
    user_id: int
    completed_tasks_count: int
    