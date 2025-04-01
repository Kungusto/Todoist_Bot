import asyncio

from src.schemas.notifications import NoficicationAdd
from src.schemas.tasks_first_step import TaskStepOneAdd
from datetime import datetime

from src.schemas.tasks_second_step import TaskStepTwoAdd
from src.schemas.users import UserAdd, UserEdit
from src.utils.init_dbmanager import get_db
from src.repositories import users

class UserNotFoundError(Exception):
    """Исключение, выбрасываемое, если пользователь не найден."""
    def __init__(self, message):
        self.message = f"Пользователь с {message} не найден."
        super().__init__(self.message)

async def get_task():
    """Загружает задачи из БД в setup.task_buttons."""
    from src.api import setup
    from src.api.register import Register
    async for db in get_db():
        result = await db.tasks_frst_stp.get_filtered(user_id=setup.id)
        tasks_dict = []
        for task in result:
            task_data = [
                task.title,
                [],  # Если подзадачи не заданы, используйте пустой список или 'None'
                task.priority if task.priority is not None else None,  # Проверка на None
                task.status if task.status is not None else 1,
                task.complation_due.strftime("%Y-%m-%d-%H-%M-%S") if task.complation_due else None
            ]
            tasks_dict.append(task_data)

        setup.task_buttons = tasks_dict
        await get_subtask()
        print(f"Загружены задачи: {tasks_dict}")
        # Регистрация задач
        register = Register()
        register.register_all()
        return tasks_dict

async def set_task():
    """Синхронизирует задачи: добавляет, обновляет и удаляет лишние."""
    from src.api import setup
    async for db in get_db():
        existing_tasks = await db.tasks_frst_stp.get_filtered(user_id=setup.id)
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
                    new_complation_due = datetime.strptime(new_due_date_str, "%Y-%m-%d-%H-%M-%S")
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
                new_complation_due = datetime.strptime(new_due_date_str, "%Y-%m-%d-%H-%M-%S")
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
                    complation_due = datetime.strptime(due_date_str, "%Y-%m-%d-%H-%M-%S")
                except Exception as e:
                    print(f"Ошибка преобразования даты ({due_date_str}):", e)
                    complation_due = None

                new_task = TaskStepOneAdd(
                    user_id=setup.id,
                    title=title,
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
        await set_subtask()

async def get_subtask():
    """Загружает подзадачи из БД и добавляет их в соответствующие задачи."""
    from src.api import setup
    async for db in get_db():
        result = await db.tasks_second_stp.get_filtered()
        subtasks_dict = {}

        for subtask in result:
            if subtask.id_super_task not in subtasks_dict:
                subtasks_dict[subtask.id_super_task] = []
            subtasks_dict[subtask.id_super_task].append(subtask.title)

        for task in setup.task_buttons:
            task_id = await db.tasks_frst_stp.get_filtered(title=task[0])
            if task_id and task_id[0].id in subtasks_dict:
                task[1] = subtasks_dict[task_id[0].id]
            else:
                task[1] = []

        print(f"Загружены подзадачи: {subtasks_dict}")
        return setup.task_buttons

async def set_subtask():
    """Синхронизирует подзадачи: добавляет, обновляет и удаляет лишние."""
    from src.api import setup
    async for db in get_db():
        existing_subtasks = await db.tasks_second_stp.get_filtered()
        existing_subtasks_dict = {subtask.id: subtask for subtask in existing_subtasks}

        new_subtasks = []
        updated_subtasks = []

        for task in setup.task_buttons:
            task_id = await db.tasks_frst_stp.get_filtered(title=task[0])
            if not task_id:
                continue
            task_id = task_id[0].id

            existing_task_subtasks = {s.title: s for s in existing_subtasks if s.id_super_task == task_id}
            new_task_subtasks = set(task[1])

            # Подзадачи для удаления (только для текущей задачи)
            deleted_subtasks = [subtask.id for subtask in existing_task_subtasks.values() if
                                subtask.title not in new_task_subtasks]

            # Подзадачи для добавления
            for subtask_title in new_task_subtasks:
                if subtask_title not in existing_task_subtasks:
                    new_subtasks.append(TaskStepTwoAdd(id_super_task=task_id, title=subtask_title))
                elif existing_task_subtasks[subtask_title].title != subtask_title:
                    updated_subtasks.append((existing_task_subtasks[subtask_title], subtask_title))

            # Удаляем подзадачи, которых нет в setup.task_buttons
            if deleted_subtasks:
                for subtask_id in deleted_subtasks:
                    await db.tasks_second_stp.delete_filtered(id=subtask_id)
                await db.commit()
                print(
                    f"Удалены подзадачи: {[existing_subtasks_dict[subtask_id].title for subtask_id in deleted_subtasks]}")

        # Обновляем подзадачи
        if updated_subtasks:
            for subtask, new_title in updated_subtasks:
                subtask.title = new_title
                await db.tasks_second_stp.edit(subtask, id=subtask.id)
            await db.commit()
            print(f"Обновлены подзадачи: {[subtask.title for subtask, _ in updated_subtasks]}")

        # Добавляем новые подзадачи
        if new_subtasks:
            for subtask in new_subtasks:
                await db.tasks_second_stp.add(subtask)
            await db.commit()
            print(f"Добавлены новые подзадачи: {[subtask.title for subtask in new_subtasks]}")

async def get_user_by_tg_id():
    from src.api.setup import user_id as tg_id
    async for db in get_db():
        user = await db.users.get_filtered(tg_id=tg_id)
        if user:
            user = user[0]
            print(user)
            return user
        raise UserNotFoundError(f"tg_id {tg_id}")

async def get_tg_id_by_id():
    from src.api.setup import id
    async for db in get_db():
        user = await db.users.get_filtered(id=id)
        if user:
            users_repo = users.UsersRepository(db.session)
            user_id = await users_repo.get_tg_id_by_id(user[0].id)
            print(user_id)
            return user_id
        raise UserNotFoundError(f"id {id}")

async def get_id_by_tg_id():
    from src.api.setup import user_id as tg_id
    async for db in get_db():
        user = await db.users.get_filtered(tg_id=tg_id)
        if user:
            users_repo = users.UsersRepository(db.session)
            user_id = await users_repo.get_id_by_tg_id(user[0].tg_id)
            print(user_id)
            return user_id
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

async def get_notifications():
    """Загружает уведомления из БД в setup.notifications_button."""
    from src.api import setup
    async for db in get_db():
        result = await db.notifications.get_filtered(user_id=setup.id)
        notifications_list = [[notification.title, notification.time.strftime("%Y-%m-%d-%H-%M")] for notification in result]

        setup.notifications_button = notifications_list
        print(f"Загружены уведомления: {notifications_list}")
        return notifications_list


async def set_notifications():
    """Синхронизирует уведомления: добавляет, обновляет и удаляет лишние."""
    from src.api import setup
    async for db in get_db():
        existing_notifications = await db.notifications.get_filtered(user_id=setup.id)
        existing_titles = {notification.title for notification in existing_notifications}

        new_notifications = {notif[0]: notif for notif in setup.notifications_button}  # Заголовок -> Данные уведомления

        notifications_to_add = []
        notifications_to_delete = []

        # Определяем уведомления для удаления
        for notification in existing_notifications:
            if notification.title not in new_notifications:
                notifications_to_delete.append(notification)

        # Удаляем уведомления, которых нет в setup.notifications_button
        if notifications_to_delete:
            for notification in notifications_to_delete:
                await db.notifications.delete_filtered(id=notification.id)
            await db.commit()
            print(f"Удалены уведомления: {[notification.title for notification in notifications_to_delete]}")

        # Добавляем новые уведомления
        for title, notif_data in new_notifications.items():
            if title not in existing_titles:
                _, time_str = notif_data
                try:
                    notif_time = datetime.strptime(time_str, "%Y-%m-%d-%H-%M")
                except Exception as e:
                    print(f"Ошибка преобразования даты ({time_str}):", e)
                    notif_time = None

                new_notification = NoficicationAdd(
                    user_id=setup.id,
                    title=title,
                    time=notif_time
                )
                notifications_to_add.append(new_notification)

        if notifications_to_add:
            for notification in notifications_to_add:
                await db.notifications.add(notification)
            await db.commit()
            print(f"Добавлены новые уведомления: {[notification.title for notification in notifications_to_add]}")


async def main():
    await get_notifications()

if __name__ == '__main__':
    asyncio.run(main())