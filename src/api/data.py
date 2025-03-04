import asyncio
from datetime import datetime
from src.schemas.tasks_first_step import TaskStepOneEdit, TaskStepOneAdd
from src.utils.init_dbmanager import get_db

user_id = 1


async def GetTask():
    """Загружает задачи из БД в setup.task_buttons."""
    from src.api import setup
    async for db in get_db():
        result = await db.tasks_frst_stp.get_filtered(user_id=user_id)
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


async def SyncTasks():
    """Синхронизирует задачи: добавляет, обновляет и удаляет лишние."""
    from src.api import setup
    async for db in get_db():
        existing_tasks = await db.tasks_frst_stp.get_filtered(user_id=user_id)
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
                new_task = TaskStepOneAdd(
                    user_id=user_id,
                    title=title,
                    description=None,
                    complation_due=complation_due,
                    priority=priority
                )
                tasks_to_add.append(new_task)
            else:
                # Добавляем новую задачу
                new_task = TaskStepOneAdd(
                    user_id=user_id,
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

        await GetTask()


async def main():
    await SyncTasks()


if __name__ == "__main__":
    asyncio.run(main())
