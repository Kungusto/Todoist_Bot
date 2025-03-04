import asyncio
from datetime import datetime
from src.schemas.tasks_first_step import TaskStepOne, TaskStepOneEdit
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
        # Удаляем все задачи пользователя
        await db.tasks_frst_stp.delete_filtered(user_id=user_id)
        await db.commit()
        print("Удалены все предыдущие задачи пользователя.")

        # Создаём новые задачи
        tasks_to_add = []
        next_id = 1  # Начинаем нумерацию с 1
        for task_data in setup.task_buttons:
            title, _, priority, _, due_date_str = task_data

            try:
                complation_due = datetime.strptime(due_date_str, "%Y-%m-%d")
            except ValueError as e:
                print(f"Ошибка преобразования даты ({due_date_str}):", e)
                continue

            new_task = TaskStepOne(
                id=next_id,
                user_id=user_id,
                title=title,
                description=None,
                complation_due=complation_due,
                priority=priority
            )

            tasks_to_add.append(new_task)
            next_id += 1  # Увеличиваем ID

        if tasks_to_add:
            for task in tasks_to_add:
                await db.tasks_frst_stp.add(task)  # Добавляем каждую задачу
            await db.commit()
            print("Добавлены новые задачи:", [task.title for task in tasks_to_add])
        else:
            print("Нет новых задач для добавления.")


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
