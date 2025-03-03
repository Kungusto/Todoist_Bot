import asyncio
from datetime import datetime
from src.schemas.tasks_first_step import TaskStepOne
from src.utils.init_dbmanager import get_db

user_id = 1

# Функция для получения задач и сохранения их в глобальной переменной setup.task_buttons
async def GetTask():
    from src.api import setup
    global user_id
    user_id = user_id
    async for db in get_db():
        result = await db.tasks_frst_stp.get_filtered(user_id=user_id)
        tasks_dict = []  # Объявляем tasks_dict сразу

        if result:
            for task_index, task in enumerate(result):
                task_data = [
                    task.title,                             # Название задачи
                    [],                                     # Подзадачи (оставляем пустым)
                    task.priority,                          # Приоритет
                    [],                                     # Статус (оставляем пустым)
                    task.complation_due.strftime("%Y-%m-%d")  # Дата завершения
                ]
                tasks_dict.append(task_data)
        else:
            tasks_dict = []

        setup.task_buttons = tasks_dict  # Теперь это глобальная переменная
        print("Загруженные задачи:", setup.task_buttons)

# Функция для добавления новой задачи (если её нет)
async def AddTaskIfNotExist():
    from src.api import setup
    async for db in get_db():
        result = await db.tasks_frst_stp.get_filtered(user_id=user_id)
        if not result:
            # Получаем последний ID
            last_task = await db.tasks_frst_stp.get_filtered(user_id=user_id)
            new_id = (max([task.id for task in last_task], default=0) + 1) if last_task else 1

            new_task = TaskStepOne(
                id=new_id,  # Добавляем id, если он не должен передаваться вручную
                user_id=user_id,
                title="Полить цветы",
                description="Описание для полить цветы",
                complation_due=datetime(2025, 3, 10, 14, 0),
                priority=1
            )

            print(f"user_id перед вставкой: {user_id}")  # Выведет 1 или None?
            await db.tasks_frst_stp.add(new_task)
            await db.commit()
            print("Новая задача добавлена.")

# Функция для обновления задач
async def EditTaskData():
    from src.api import setup
    async for db in get_db():
        result = await db.tasks_frst_stp.get_filtered(user_id=user_id)
        if not result:
            print("Нет задач для обновления.")
            return

        # Загружаем актуальные задачи в глобальную переменную
        await GetTask()
        if not setup.task_buttons:
            print("Глобальная переменная task_buttons пуста.")
            return

        # Берем новые данные для обновления из первой записи глобального списка
        new_task_data = setup.task_buttons[0]
        title = new_task_data[0]
        description = None
        priority = new_task_data[2]
        due_date_str = new_task_data[4]
        try:
            complation_due = datetime.strptime(due_date_str, "%Y-%m-%d")
        except Exception as e:
            print("Ошибка преобразования даты:", e)
            return

        print("Новые данные для обновления:", title, priority, complation_due)

        # Проходим по каждой задаче и обновляем её данные
        for task in result:
            # Создаем новый объект TaskStepOne с новыми данными
            task_data_to_edit = TaskStepOne(
                title=title,
                description=description,
                complation_due=complation_due,
                priority=priority
            )
            if task.id:
                await db.tasks_frst_stp.edit(task_data_to_edit, id=task.id)
            else:
                await db.tasks_frst_stp.add(task_data_to_edit)
        await db.commit()
        print(f"Все задачи для пользователя {user_id} обновлены.")
        await GetTask()  # Обновляем глобальные данные

async def main():
    from src.api import setup
    # Сначала проверяем, есть ли задачи. Если нет – добавляем новую.
    await AddTaskIfNotExist()
    # Затем обновляем задачи.
    await EditTaskData()

if __name__ == "__main__":
    asyncio.run(main())
