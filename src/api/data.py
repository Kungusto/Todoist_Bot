import asyncio
from datetime import datetime
from src.schemas.tasks_first_step import TaskStepOne, TaskStepOneEdit, TaskStepOneAdd
from src.utils.init_dbmanager import get_db

user_id = 1

# Функция для получения задач и сохранения их в глобальной переменной setup.task_buttons
async def GetTask():
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

# Функция для добавления новых задач, если их нет
async def AddTasksIfNotExist():
    from src.api import setup
    global user_id
    async for db in get_db():
        # Получаем существующие задачи пользователя
        existing_tasks = await db.tasks_frst_stp.get_filtered(user_id=user_id)
        existing_titles = {task.title for task in existing_tasks}  # Множество с заголовками существующих задач

        tasks_to_add = []
        tasks_to_update = []

        for task_data in setup.task_buttons:
            title, _, priority, _, due_date_str = task_data

            try:
                complation_due = datetime.strptime(due_date_str, "%Y-%m-%d")
            except ValueError as e:
                print(f"Ошибка преобразования даты ({due_date_str}):", e)
                continue

            # Если задача с таким названием уже существует, будем обновлять её
            if title in existing_titles:
                existing_task = next(task for task in existing_tasks if task.title == title)
                updated_task = TaskStepOneEdit(
                    title=title,
                    description=None,
                    complation_due=complation_due,
                    priority=priority
                )
                await db.tasks_frst_stp.edit(updated_task, id=existing_task.id)
                tasks_to_update.append(title)
            else:
                # Иначе добавляем новую задачу
                new_task = TaskStepOneAdd(
                    user_id=user_id,
                    title=title,
                    description=None,
                    complation_due=complation_due,
                    priority=priority
                )
                tasks_to_add.append(new_task)

        # Если есть новые задачи для добавления
        if tasks_to_add:
            for task in tasks_to_add:
                await db.tasks_frst_stp.add(task)  # Добавляем каждую задачу
            await db.commit()
            print("Добавлены новые задачи:", [task.title for task in tasks_to_add])

        # Если есть обновленные задачи
        if tasks_to_update:
            await db.commit()
            print("Обновлены задачи:", tasks_to_update)

        if not tasks_to_add and not tasks_to_update:
            print("Нет новых задач для добавления или обновления.")

# Функция для обновления задач
async def EditTaskData():
    from src.api import setup
    async for db in get_db():
        existing_tasks = await db.tasks_frst_stp.get_filtered(user_id=user_id)
        if not existing_tasks:
            print("Нет задач для обновления.")
            return

        await GetTask()
        if not setup.task_buttons:
            print("Глобальная переменная task_buttons пуста.")
            return

        updated_tasks = []
        for task_data in setup.task_buttons:
            title, _, priority, _, due_date_str = task_data
            try:
                complation_due = datetime.strptime(due_date_str, "%Y-%m-%d")
            except ValueError as e:
                print(f"Ошибка преобразования даты ({due_date_str}):", e)
                continue

            for task in existing_tasks:
                if task.title == title:
                    updated_task = TaskStepOneEdit(
                        title=title,
                        description=None,
                        complation_due=complation_due,
                        priority=priority
                    )
                    await db.tasks_frst_stp.edit(updated_task, id=task.id)
                    updated_tasks.append(title)
                    break

        if updated_tasks:
            await db.commit()
            print("Обновлены задачи:", updated_tasks)
        else:
            print("Нет задач для обновления.")

        await GetTask()

async def main():
    await AddTasksIfNotExist()
    await EditTaskData()

if __name__ == "__main__":
    asyncio.run(main())
