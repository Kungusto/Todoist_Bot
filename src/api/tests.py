# -------- Без этих команд он не видит папку src в импортах
import sys
from pathlib import Path 

sys.path.append(str(Path(__file__).parent.parent.parent))
# --------

from src.utils.init_dbmanager import get_db
from src.database import async_session_maker
from src.schemas.tasks_first_step import TaskStepOneAdd

import asyncio

'''
Основной принцип работы с репозиторием(моим классом)

пишешь async for db in get_db() : 
    db.*имя таблички*.метод()

Методы репозитория на данный момент :

1. get_all() - тупо возвращает все задачи
2. add() - принимает на вход pydantic-схему и добавляет исходя из нее строчку в базу данных. 
После не забудь закомминить: await *сессия*.commit() 
3. get_filtered() - принимает на вход условия можно написать get_filtered(title="ДЗ") и он вернет все задачи с названием ДЗ. 
ну ты понял

! если нужен будет какой-то узкий метод, сделаю без проблем
'''

# Получить все задачи
async def add_models() : 
    async for db in get_db() : 
        result = await db.tasks_frst_stp.get_all()
        print(result)
        return result

asyncio.run(add_models()) # эта штука запускает асинхронную функцию