import asyncio
from datetime import datetime, timedelta

from aiogram.types import CallbackQuery

from src.utils.init_dbmanager import get_db

class Notifications:

    def __init__(self, callback: CallbackQuery):
        self.callback = callback

    async def task_time_out(self):
        while True:
            from src.api import setup
            for task in setup.task_buttons:
                if datetime.strptime(task[4], "%Y-%m-%d-%H-%M") < datetime.now():
                    if setup.settings["notifications"]: # <-- обязательно!
                        await self.callback.message.answer(f"*Просрочена задача: *{task[0]}!", parse_mode="MarkdownV2")# <-- обязательно!
                    setup.notifications_button.append(f"*Просрочена задача: *{task[0]}!")# <-- обязательно!
            await asyncio.sleep(60)

    async def task_time_less(self):
        while True:
            from src.api import setup
            for task in setup.task_buttons:
                if datetime.strptime(task[4], "%Y-%m-%d-%H-%M") < datetime.now():
                    await asyncio.sleep(60)  # Временный заглушка (добавишь логику позже)
                #потом допишешь по аналогии с task_time_out
                
    async def main_notification(self) : 
        while True :
            async for db in get_db() :
                print("ТЕСТ")
                await asyncio.sleep(15)
                target_tasks = await db.tasks.get_tasks_x_to_complete(timedelta(hours=2))
                await self.callback.message.answer(target_tasks)
                

# в main ничего делать не надо!!!
# только тут методы напиши и всё

    async def start_all_tasks(self): #<-- это не менять!!!
        """Автоматически запускает все асинхронные методы класса"""
        tasks = []
        for attr in dir(self):
            method = getattr(self, attr)
            if callable(method) and asyncio.iscoroutinefunction(method) and attr != "start_all_tasks":
                tasks.append(asyncio.create_task(method()))
        await asyncio.gather(*tasks)
