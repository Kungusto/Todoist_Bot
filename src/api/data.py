import asyncio

from src.schemas.tasks_first_step import TaskStepOneEdit, TaskStepOneAdd
from datetime import datetime
from src.schemas.users import UserAdd, UserEdit
from src.utils.init_dbmanager import get_db

class UserNotFoundError(Exception):
    """Исключение, выбрасываемое, если пользователь не найден по tg_id."""
    def __init__(self, message):
        self.message = f"Пользователь с {message} не найден."
        super().__init__(self.message)


async def get_task():
    """Загружает задачи из БД в setup.task_buttons."""
    from src.api import setup
    async for db in get_db():
        result = await db.tasks_frst_stp.get_filtered(user_id=setup.user_id)
        tasks_dict = []

        if result:
            for task in result:
                task_data = [
                    task.title,
                    [],
                    task.priority,
                    [],
                    task.complation_due.strftime("%Y-%m-%d")
                ]
                tasks_dict.append(task_data)

        setup.task_buttons = tasks_dict
        print("Загруженные задачи:", setup.task_buttons)


async def set_task():
    """Синхронизирует задачи: добавляет, обновляет и удаляет лишние."""
    from src.api import setup
    async for db in get_db():
        existing_tasks = await db.tasks_frst_stp.get_filtered(user_id=setup.user_id)
        existing_titles = {task.title for task in existing_tasks}

        new_titles = {task[0] for task in setup.task_buttons}  # Собираем заголовки из setup.task_buttons

        tasks_to_add = []
        tasks_to_update = []
        tasks_to_delete = [task for task in existing_tasks if task.title not in new_titles]  # Ищем лишние задачи

        # Удаляем задачи, которых нет в setup.task_buttons
        for task in tasks_to_delete:
            await db.tasks_frst_stp.delete_filtered(id=task.id)
        if tasks_to_delete:
            await db.commit()
            print("Удалены лишние задачи:", [task.title for task in tasks_to_delete])

        # Обрабатываем добавление и обновление
        for task_data in setup.task_buttons:
            title, _, priority, _, due_date_str = task_data
            try:
                complation_due = datetime.strptime(due_date_str, "%Y-%m-%d")
            except ValueError as e:
                print(f"Ошибка преобразования даты ({due_date_str}):", e)
                continue

            if title in existing_titles:
                existing_task = next(task for task in existing_tasks if task.title == title)

                # Перед обновлением удаляем старую версию задачи
                await db.tasks_frst_stp.delete_filtered(id=existing_task.id)
                await db.commit()
                print(f"Удалена старая версия задачи: {title}")

                # Добавляем обновлённую задачу
                new_task = TaskStepOneEdit(
                    title=title,
                    description=None,
                    complation_due=complation_due,
                    priority=priority
                )
                tasks_to_add.append(new_task)
            else:
                # Добавляем новую задачу
                new_task = TaskStepOneAdd(
                    user_id=setup.user_id,
                    title=title,
                    description=None,
                    complation_due=complation_due,
                    priority=priority
                )
                tasks_to_add.append(new_task)

        # Добавляем новые/обновленные задачи
        if tasks_to_add:
            for task in tasks_to_add:
                await db.tasks_frst_stp.add(task)
            await db.commit()
            print("Добавлены новые задачи:", [task.title for task in tasks_to_add])

        await get_task()

async def get_user_by_tg_id():
    from src.api.setup import user_id as tg_id
    print(tg_id)
    async for db in get_db():
        user = await db.users.get_filtered(tg_id=tg_id)
        if user:
            return user[0]  # Берём первого пользователя из списка
        raise UserNotFoundError(f"tg_id {tg_id}")

async def get_user_by_nickname(nickname: str):
    async for db in get_db():
        users = await db.users.get_filtered(nickname=nickname)
        if users:
            print(users)
            return users
        raise UserNotFoundError(f"nickname {nickname}")

async def set_user():
    """Проверяет, существует ли пользователь в базе данных по tg_id, если нет — добавляет его или обновляет данные."""
    from src.api.setup import user_id, nickname, password  # Берем user_id, nickname и password из setup

    async for db in get_db():
        # Проверим, есть ли пользователь с таким tg_id
        existing_user = await db.users.get_filtered(tg_id=user_id)

        if existing_user:
            # Если пользователь существует, обновляем его nickname и password
            updated_user = UserEdit(
                tg_id=user_id,
                nickname=nickname,
                password=password
            )
            await db.users.edit(updated_user, tg_id=user_id)  # Используем tg_id для фильтрации
            await db.commit()
            print(f"Данные пользователя с tg_id {user_id} были обновлены.")
        else:
            # Если пользователя нет, добавляем нового
            now = datetime.now()
            new_user = UserAdd(
                tg_id=user_id,
                nickname=nickname,
                registrated=now.date(),  # Преобразование datetime в date
                password=password
            )
            await db.users.add(new_user)
            await db.commit()
            print(f"Добавлен новый пользователь с tg_id {user_id}")

async def main():
    await get_user_by_nickname("Deimos")

if __name__ == '__main__':
    asyncio.run(main())