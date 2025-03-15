from src.schemas.tasks_first_step import TaskStepOneAdd
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
    from src.api.register import Register
    async for db in get_db():
        result = await db.tasks_frst_stp.get_filtered(user_id=setup.user_id)
        print(result)
        tasks_dict = []

        for task in result:
            task_data = [
                task.title,
                [],  # Если подзадачи не заданы, используйте пустой список или 'None'
                task.priority if task.priority is not None else None,  # Проверка на None
                task.status if task.status is not None else 1,
                task.complation_due.strftime("%Y-%m-%d-%M-%S") if task.complation_due else None
            ]
            tasks_dict.append(task_data)

        setup.task_buttons = tasks_dict

        # Регистрация задач
        register = Register()
        register.register_all()

        return tasks_dict

async def set_task():
    """Синхронизирует задачи: добавляет, обновляет и удаляет лишние."""
    from src.api import setup
    async for db in get_db():
        existing_tasks = await db.tasks_frst_stp.get_filtered(user_id=setup.user_id)
        existing_titles = {task.title for task in existing_tasks}

        new_tasks = {task[0]: task for task in setup.task_buttons}  # Заголовок -> Данные задачи

        print("Заголовки задач", existing_titles)
        tasks_to_add = []
        tasks_to_update = []
        tasks_to_delete = []

        # Проверяем, какие задачи нужно удалить (если заголовок не найден в новых задачах)
        for task in existing_tasks:
            if task.title not in new_tasks:
                tasks_to_delete.append(task)
            else:
                new_task_data = new_tasks[task.title]
                _, _, new_priority, new_status, new_due_date_str = new_task_data

                try:
                    new_complation_due = datetime.strptime(new_due_date_str, "%Y-%m-%d-%M-%S")
                except Exception as e:
                    print(f"Ошибка преобразования даты ({new_due_date_str}):", e)
                    new_complation_due = None

                # Проверяем, изменились ли данные задачи
                if (
                        task.priority != new_priority or
                        task.status != new_status or
                        task.complation_due != new_complation_due
                ):
                    tasks_to_update.append((task, new_task_data))

        # Удаляем задачи, которых нет в setup.task_buttons
        if tasks_to_delete:
            for task in tasks_to_delete:
                await db.tasks_frst_stp.delete_filtered(id=task.id)
            await db.commit()
            print("Удалены лишние задачи:", [task.title for task in tasks_to_delete])

        # Обновляем задачи, если они изменились
        updated_tasks = []  # Новый список для обновленных задач
        for task, new_task_data in tasks_to_update:
            new_title, _, new_priority, new_status, new_due_date_str = new_task_data

            try:
                new_complation_due = datetime.strptime(new_due_date_str, "%Y-%m-%d-%M-%S")
            except Exception as e:
                print(f"Ошибка преобразования даты ({new_due_date_str}):", e)
                new_complation_due = None

            # Обновляем поля существующей задачи
            task.title = new_title
            task.priority = new_priority
            task.status = new_status
            task.complation_due = new_complation_due

            updated_tasks.append(task)  # Добавляем обновленную задачу в отдельный список

        if updated_tasks:
            for task in updated_tasks:
                await db.tasks_frst_stp.edit(task, id=task.id)
            await db.commit()
            print("Обновлены задачи:", [task.title for task in updated_tasks])

        # Добавляем новые задачи
        for title, task_data in new_tasks.items():
            if title not in existing_titles:
                _, _, priority, status, due_date_str = task_data
                try:
                    complation_due = datetime.strptime(due_date_str, "%Y-%m-%d-%M-%S")
                except Exception as e:
                    print(f"Ошибка преобразования даты ({due_date_str}):", e)
                    complation_due = None

                new_task = TaskStepOneAdd(
                    user_id=setup.user_id,
                    title=title,
                    description=None,
                    complation_due=complation_due,
                    priority=priority,
                    status=status
                )
                tasks_to_add.append(new_task)

        if tasks_to_add:
            for task in tasks_to_add:
                await db.tasks_frst_stp.add(task)
            await db.commit()
            print("Добавлены новые задачи:", [task.title for task in tasks_to_add])

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
        return None
