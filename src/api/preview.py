from src.utils.init_dbmanager import get_db
from src.database import async_session_maker
from src.schemas.tasks_first_step import TaskStepOneAdd

import asyncio

'''
Основной принцип работы с get_db()

пишешь async for db in get_db() : 
    db.*имя таблички*.метод()

Методы работающие для всех таблиц: 
    1. get_all() - тупо возвращает все задачи
    2. add() - принимает на вход pydantic-схему и добавляет исходя из нее строчку в базу данных.    
    После не забудь закомминить: await *сессия*.commit() 
    3. get_filtered() - принимает на вход условия можно написать get_filtered(title="ДЗ") и он вернет все задачи с названием ДЗ. 
    ну ты понял

Методы специально для таблички задач :
    1. get_today_due_tasks() - получает все задачи, которые нужно сделать сегодня
    
Ниже примеры использования репозитория

! если нужен будет какой-то узкий метод, сделаю без проблем
'''

async def get_all_tasks() : 
    '''Получить все текущие задачи'''
    async for db in get_db() : 
        result = await db.tasks_frst_stp.get_all()
        print(result)
        return result

# asyncio.run(get_all_tasks()) 

async def get_all_users() : 
    '''Получить всех юзеров'''
    async for db in get_db() : 
        result = await db.users.get_all()
        print(result)
        return result

# asyncio.run(get_all_users()) 

async def get_all_users(user_id: int) :
    '''Получить все задачи юзера'''
    async for db in get_db() : 
        result = await db.tasks_frst_stp.get_filtered(user_id=user_id)
        print(result)
        return result
    
# asyncio.run(get_all_users(user_id=1))