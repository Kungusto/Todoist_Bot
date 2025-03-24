# -------- Без этих команд он не видит папку src в импортах (потом закомментить. он также есть и в main.py). при тестах не комментить
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Путь к .env файлу
env_path = Path(__file__).resolve().parent.parent / ".env"  # Пример с переходом на два уровня выше
sys.path.append(str(Path(__file__).parent.parent.parent))

# Загружаем .env файл
from dotenv import load_dotenv
load_dotenv(env_path)

# --------
from src.utils.init_dbmanager import get_db
from src.database import async_session_maker
from src.schemas.tasks_first_step import TaskStepOneAdd, TaskStepOneEdit
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

#asyncio.run(get_all_tasks())


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
    '''Изменить уже имеющуюся строчку'''
    async for db in get_db() :
        result = await db.users.edit(data, **filter_by)
        print(result)
        await db.commit()
        return result

# data_to_edit = UserEdit(tg_id='123456789') # создаем Pydantic-схему
# asyncio.run(edit_user(data_to_edit, id=1)) # изменить данные в строчке пользователя с айдишником 1 

# ----------------------------------------------------------------

async def edit_tasks(data, **filter_by) :
    '''изменить существующую задачу'''
    async for db in get_db() :
        result = await db.tasks_frst_stp.edit(data, **filter_by)
        print(result)
        await db.commit()
        return result
    
# data_to_edit = TaskStepOneEdit(title='Хуйня задача')
# asyncio.run(edit_tasks(data_to_edit, id=1))

# ----------------------------------------------------------------

async def get_id_by_tg_id() : 
    async for db in get_db() :
        users = await db.users.get_tg_id_by_id(1)
        print([user.tg_id for user in users])
    
# asyncio.run(get_id_by_tg_id())

async def get_tasks_hour_to_complete() :
    async for db in get_db() : 
        tasks = await db.tasks.get_tasks_x_to_complete(
           timedelta(days=3)
            )
        print(tasks)

asyncio.run(get_tasks_hour_to_complete())