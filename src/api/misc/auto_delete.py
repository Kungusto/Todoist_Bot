import asyncio
from datetime import timedelta
from src.api.data import *


async def delete_task():
    print("вызов")
    await get_task()
    while True:
        from src.api import setup
        # Проверяем каждую задачу
        for task in setup.task_buttons:
            if setup.settings["auto_delete"] == 7 and task[3] == 4:
                deadline = datetime.strptime(task[4], "%Y-%m-%d-%H-%M-%S")
                if deadline + timedelta(days=7) < datetime.now():
                    setup.task_buttons.remove(task)  # Удаляем задачу
                    await set_task()
                    setup.notifications_button.append(f"*Просрочена и удалена задача: *{task[0]}!")
                    print("Просрочена и удалена задача")
                    await asyncio.sleep(60)  # Проверяем задачи каждую минуту

            if setup.settings["auto_delete"] == 30 and task[3] == 4:
                deadline = datetime.strptime(task[4], "%Y-%m-%d-%H-%M-%S")
                if deadline + timedelta(days=30) < datetime.now():
                    setup.task_buttons.remove(task)  # Удаляем задачу
                    await set_task()
                    setup.notifications_button.append(f"*Просрочена и удалена задача: *{task[0]}!")
                    await asyncio.sleep(60)  # Проверяем задачи каждую минуту

        await asyncio.sleep(60)  # Проверяем задачи каждую минуту