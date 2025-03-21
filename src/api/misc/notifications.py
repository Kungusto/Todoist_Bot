import asyncio
from datetime import datetime

from aiogram.types import CallbackQuery

class Notifications:
    # async def notifications():
    #     from src.api import setup
    #
    #     #     while True :
    #     #         notifications = setup.notifications
    #     #         tasks = setup.task_buttons
    #     #         current_time = datetime.now("%Y-%m-%d-%M-%S")
    #     #         for task in tasks:
    #     #             if datetime.strptime(task[4], "%Y-%m-%d-%M-%S") >= current_time :
    #     #                 ...
    #     #         asyncio.sleep(60)
    #     while True:
    #         notifications = setup.notifications
    #         tasks = setup.task_buttons
    #         current_time = datetime.now("%Y-%m-%d-%M-%S")
    #         for task in tasks:
    #             if datetime.strptime(task[4], "%Y-%m-%d-%M-%S") >= current_time:
    #                 ...
    #         asyncio.sleep(60)

    def __init__(self, callback: CallbackQuery):
        self.callback = callback

    async def task_time_out(self):
        while True:
            from src.api import setup
            for task in setup.task_buttons:
                if datetime.strptime(task[4], "%Y-%m-%d-%M-%S") < datetime.now():
                    if setup.settings["notifications"]: # <-- обязательно!
                        await self.callback.message.answer(f"*Просрочена задача: *{task[0]}!", parse_mode="MarkdownV2")# <-- обязательно!
                    setup.notifications_button.append(f"*Просрочена задача: *{task[0]}!")# <-- обязательно!
            await asyncio.sleep(60)

    async def task_time_less(self):
        while True:
            from src.api import setup
            for task in setup.task_buttons:
                if datetime.strptime(task[4], "%Y-%m-%d-%M-%S") < datetime.now():
                    pass
                #потом допишешь по аналогии с task_time_out

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
