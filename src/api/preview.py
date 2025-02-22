# -------- Без этих команд он не видит папку src в импортах (потом закомментить. он также есть и в main.py). при тестах не комментить
import sys
from pathlib import Path 

sys.path.append(str(Path(__file__).parent.parent.parent))
# --------

from src.utils.init_dbmanager import get_db
from src.database import async_session_maker
from src.schemas.tasks_first_step import TaskStepOneAdd
from src.schemas.users import UserEdit

import asyncio

'''
Основной принцип работы с get_db()

пишешь async for db in get_db() : 
    db.*имя таблички*.метод()

Методы работающие для всех таблиц: 
    1. get_all() - тупо возвращает все задачи
    2. add() - принимает на вход pydantic-схему (используй те которые оканчиваются на Add) и добавляет исходя из нее строчку в базу данных.    
    После не забудь закомминить: await *сессия*.commit() 
    3. get_filtered() - принимает на вход условия можно написать get_filtered(title="ДЗ") и он вернет все задачи с названием ДЗ. 
    ну ты понял
    4. edit() - принимает на вход Pydantic-схему и дополнительные фильтры. 
    если вернул: "{'status': 'OK'}" значит все выполнилось

Методы специально для таблички задач :
    1. get_today_due_tasks(user_id: int) - получает все задачи, которые нужно сделать сегодня
    
Ниже примеры использования репозитория

! если нужен будет какой-то узкий метод, сделаю без проблем
'''

# ----------------------------------------------------- ПРИМЕРЫ ------------------------------------------------------ #

## Самый легкий метод get_all()
async def get_all_tasks() : 
    '''Получить все текущие задачи'''
    async for db in get_db() : # так во всех функциях
        result = await db.tasks_frst_stp.get_all()
        print(result)
        return result

# asyncio.run(get_all_tasks()) 


# ----------------------------------------------------------------

## Пример метода get_all()
async def get_all_users() : 
    '''Получить всех юзеров'''
    async for db in get_db() : 
        result = await db.users.get_all()
        print(result)
        return result

# asyncio.run(get_all_users())  # получить всех пользователей

# ----------------------------------------------------------------

## Пример метода get_filtered()
async def get_user_tasks(user_id: int) :
    '''Получить все задачи юзера'''
    async for db in get_db() : 
        result = await db.tasks_frst_stp.get_filtered(user_id=user_id)
        print(result)
        return result
    
# asyncio.run(get_users_tasks(user_id=1)) # получить все задачи, принадлежащие юзеру с первым айди

# ----------------------------------------------------------------

## Пример метода edit()
async def edit_user(data, *filter, **filter_by) : 
    '''Изменить уже имеющуюся табличку'''
    async for db in get_db() :
        result = await db.users.edit(data, *filter, **filter_by)
        print(result)
        await db.commit()
        return result

# data_to_edit = UserEdit(tg_id='123456789') # создаем Pydantic-схему
# asyncio.run(edit_user(data_to_edit, id=1)) # изменить данные в строчке пользователя с айдишником 1 

