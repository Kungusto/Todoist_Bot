import asyncio

from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from src.api.userInputHandler import UserInputHandler
from src.api.data import *
import random
from src.utils.escape_md import *
from src.api.misc.auto_delete import *

class BaseHandler:
    def __init__(self, bot, dispatcher):
        self.bot = bot
        self.dispatcher = dispatcher

    async def send_message(self, chat_id: int, text: str):
        await self.bot.send_message(chat_id, text)


class CommandHandler(BaseHandler):
    def __init__(self, bot, dispatcher):
        super().__init__(bot, dispatcher)

    async def start_command(self, message: Message):
        from src.api import setup
        setup.current_state = 1
        setup.user_id = str(message.from_user.id)
        auth = Auth()
        await auth.first(message)

    async def help_command(self, message: Message):
        await message.answer(
            "*Доступные команды\\:*\\n"
            "`/start` \\- запуск бота\\n"
            "`/help` \\- помощь по боту\\n"
            "`/create` \\- создание новой задачи\\n"
            "`/tasks` \\- показать все задачи",
            parse_mode="MarkdownV2"
        )

class ButtonNavHandler(BaseHandler):
    async def list_tasks(self, message: Message):
        from src.api import setup
        print("list_tasks: ", setup.task_buttons)
        setup.current_state = 2
        await message.answer(
            "📋 *Мои задачи*",
            reply_markup=setup.task_keyboard,
            parse_mode="MarkdownV2"
        )

    async def add_task(self, message: Message, state: FSMContext):
        """Запрашивает у пользователя задачу и ждёт её ввод."""
        await state.set_state(UserInputHandler.waiting_for_input)
        await message.answer("*Введите новую задачу\\:*", parse_mode="MarkdownV2")

    async def settings(self, message: Message):
        from src.api import setup
        await message.answer("⚙ *Прочее\\.\\.\\.*", parse_mode="MarkdownV2", reply_markup=setup.misc_keyboard)

    async def task_selected(self, callback: CallbackQuery, state: FSMContext):
        """Обработчик нажатий на задачу из списка."""
        from src.api import setup

        if callback.data.startswith("task:"):
            _, task_index = callback.data.split(":")
            task_index = int(task_index)

            # Логирование
            print(f"Received callback data: {callback.data}")
            print(f"task_index: {task_index}")
            print(f"setup.task_buttons: {setup.task_buttons}")

            # Проверка на допустимость индекса
            if not setup.task_buttons or task_index < 0 or task_index >= len(setup.task_buttons):
                await callback.answer("⚠ *Ошибка\\: задача не найдена\\!*", parse_mode="MarkdownV2")
                return

            # Сохраняем индекс выбранной задачи для редактирования
            await state.update_data(editing_task_index=task_index)

            # Обновляем callback_data для кнопок редактирования, включая подзадачу
            for button in setup.task_edit_buttons:
                parts = button[1].split(":")
                if len(parts) == 2 and parts[1].isdigit():
                    button[1] = f"{parts[0]}:{task_index}"

            setup.task_edit_keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text=btn[0], callback_data=btn[1])]
                    for btn in setup.task_edit_buttons
                ]
            )

            # Логирование выбранной задачи
            task_data = setup.task_buttons[task_index]
            print(f"Selected task data: {task_data}")

            task_name = task_data[0] if len(task_data) > 0 else "Без названия"
            subtasks = task_data[1] if len(task_data) > 1 else []
            subtasks = "\n".join([f"• {sub}" for sub in subtasks]) if subtasks else "Нет подзадач"
            priority = task_data[2] if len(task_data) > 2 else "Не установлен"
            status = task_data[3] if len(task_data) > 3 else "Не установлен"
            deadline = task_data[4] if len(task_data) > 4 else "Не установлен"

            await callback.message.answer(
                f"*Вы выбрали задачу:* `{escape_md(task_name)}`\n\n"
                f"*Подзадачи:*\n{escape_md(subtasks)}\n\n"
                f"*Приоритет:* `{escape_md(priority)}`\n"
                f"*Статус:* `{escape_md(status)}`\n"
                f"*Дедлайн:* `{escape_md(deadline)}`\n\n",
                reply_markup=setup.task_edit_keyboard,
                parse_mode="MarkdownV2"
            )

            setup.current_state = 3
            await callback.answer()

class Auth:
    async def first(self, message: Message):
        from src.api import setup
        try:
            user = await get_user_by_tg_id()
            setup.nickname = user.nickname
            setup.password = user.password
            setup.user_id = user.tg_id
            print(setup.user_id)
            print("До", setup.task_buttons)
            setup.task_buttons = await get_task()
            await message.answer(f"С возвращением, {user.nickname}!", reply_markup=setup.nav_keyboard)

            asyncio.create_task(delete_task())
            print("После", setup.task_buttons)
        except UserNotFoundError:
            await message.answer(
                "**Привет!** Я твой *Todoist-бот*.\nДля начала работы нужно войти или зарегистрироваться.",
                reply_markup=setup.auth_keyboard
            )

    async def enter(self, callback: CallbackQuery, state: FSMContext):
        """Запрашивает логин пользователя для входа."""
        await callback.message.answer("Введите ваш логин:")
        await state.set_state(UserInputHandler.waiting_for_enter)
        await callback.answer()

    async def process_enter(self, message: Message, state: FSMContext):
        """Обрабатывает логин пользователя и запрашивает пароль."""
        try:
            users = await get_user_by_nickname(message.text)

            if not users:
                await message.answer("❌ Пользователь не найден. Попробуйте снова или зарегистрируйтесь.")
                return

            await state.update_data(nickname=message.text)
            await message.answer("Введите ваш пароль:")
            await state.set_state(UserInputHandler.waiting_for_enter_password)
        except UserNotFoundError:
            await message.answer("❌ Пользователь не найден. Попробуйте снова или зарегистрируйтесь.")

    async def process_enter_password(self, message: Message, state: FSMContext):
        """Проверяет пароль и отправляет код подтверждения."""
        from src.api import setup

        user_data = await state.get_data()
        users = await get_user_by_nickname(user_data['nickname'])

        matching_users = [u for u in users if u.password == message.text]

        if not matching_users:
            await message.answer("❌ Неверный пароль. Попробуйте снова.")
            return

        # Генерируем уникальный код для каждого пользователя
        confirmation_codes = {}
        for user in matching_users:
            confirmation_code = str(random.randint(100000, 999999))
            confirmation_codes[user.tg_id] = confirmation_code  # Привязываем код к ID пользователя
            setup.active_codes[user.tg_id] = confirmation_code

            try:
                await message.bot.send_message(user.tg_id, f"🔐 Ваш код подтверждения: {confirmation_code}")
            except Exception:
                pass  # Если не удалось отправить, просто продолжаем

        await message.answer("📩 Код подтверждения отправлен. Введите его ниже:")
        await state.set_state(UserInputHandler.waiting_for_code)

    async def process_enter_code(self, message: Message, state: FSMContext):
        """Проверяет введённый код и входит в систему."""
        from src.api import setup

        user_data = await state.get_data()
        users = await get_user_by_nickname(user_data['nickname'])

        # Ищем пользователя, который ввёл правильный код
        matching_users = [u for u in users if setup.active_codes.get(u.tg_id) == message.text]

        if not matching_users:
            await message.answer("❌ Ошибка: Неверный код или код не запрашивался.")
            return

        # Авторизуем первого совпавшего пользователя
        user = matching_users[0]
        setup.nickname = user.nickname
        setup.password = user.password
        setup.user_id = str(user.tg_id)
        setup.task_buttons = await get_task()

        await set_user()
        await message.answer(f"✅ Успешный вход! Привет, {user.nickname}.", reply_markup=setup.nav_keyboard)
        await state.clear()

        # Удаляем использованный код
        del setup.active_codes[user.tg_id]

    async def register(self, callback: CallbackQuery, state: FSMContext):
        """Начинает процесс регистрации."""
        await callback.message.answer("Введите желаемый логин:")
        await state.set_state(UserInputHandler.waiting_for_reg)
        await callback.answer()

    async def process_register(self, message: Message, state: FSMContext):
        """Переходит к вводу пароля."""
        await state.update_data(nickname=message.text)
        await message.answer("Введите пароль:")
        await state.set_state(UserInputHandler.waiting_for_reg_password)

    async def process_register_password(self, message: Message, state: FSMContext):
        """Сохраняет пользователя и завершает регистрацию."""
        user_data = await state.get_data()
        from src.api import setup

        setup.nickname = user_data['nickname']
        setup.password = message.text
        setup.user_id = str(message.from_user.id)

        await set_user()  # Сохранение в базу

        await message.answer("✅ Вы успешно зарегистрированы и автоматически вошли в систему!",
                             reply_markup=setup.nav_keyboard)
        await state.clear()

class ButtonEditTaskHandler(BaseHandler):
    async def edit_task_selected(self, callback: CallbackQuery, state: FSMContext):
        """Обработчик редактирования основной задачи."""
        from src.api import setup

        print(f"Received callback data: {callback.data}")

        if callback.data.startswith("edit_task:"):
            _, task_index = callback.data.split(":")
            task_index = int(task_index)

            try:
                task_name = setup.task_buttons[task_index][0]
            except IndexError:
                await callback.message.answer("⚠ *Ошибка\\: задача не найдена\\!* Попробуйте снова\\.",
                                              parse_mode="MarkdownV2")
                return

            await state.update_data(editing_task_index=task_index)

            # Устанавливаем корректное состояние для редактирования задачи
            await state.set_state(UserInputHandler.waiting_for_edit)

            await callback.message.answer(
                f"*Введите новый текст для задачи* {task_name}\\:",
                parse_mode="MarkdownV2"
            )

            await callback.answer()

    async def subtask_selected(self, callback: CallbackQuery, state: FSMContext):
        """Обработчик для добавления подзадачи."""
        from src.api import setup
        print(f"Received callback data: {callback.data}")

        if callback.data.startswith("add_subtasks:"):
            _, task_index = callback.data.split(":")
            task_index = int(task_index)

            try:
                task_name = setup.task_buttons[task_index][0]
            except IndexError:
                await callback.message.answer("⚠ *Ошибка\\: задача не найдена\\!* Попробуйте снова\\.",
                                              parse_mode="MarkdownV2")
                return

            await state.update_data(subtask_index=task_index)

            # Устанавливаем корректное состояние для ввода подзадачи
            await state.set_state(UserInputHandler.waiting_for_subtask)

            await callback.message.answer(
                f"*Введите текст подзадачи для* {task_name}\\:",
                parse_mode="MarkdownV2"
            )

            await callback.answer()

    async def priority_selected(self, callback: CallbackQuery, state: FSMContext):
        from src.api import setup, data

        if callback.data.startswith("change_priority:"):
            _, priority_index = callback.data.split(":")
            priority_index = int(priority_index)

            try:
                task_name = setup.task_buttons[priority_index][0]
            except IndexError:
                await callback.message.answer("⚠ *Ошибка\\: задача не найдена\\!* Попробуйте снова\\.",
                                              parse_mode="MarkdownV2")
                return

            # Сохраняем priority_index в состояние
            await state.update_data(priority_index=priority_index)

            await callback.message.answer(
                f"*Какой приоритет вы хотите поставить в задаче* `{task_name}`\\?",
                reply_markup=setup.task_priority_edit_keyboard,
                parse_mode="MarkdownV2"
            )

            await callback.answer()

        elif callback.data in ["Low", "Medium", "High"]:  # Обрабатываем приоритет
            global task_priority, task_priority_index
            user_data = await state.get_data()
            priority_index = user_data.get("priority_index")

            if priority_index is None:
                await callback.message.answer(
                    "⚠ *Ошибка\\:* задача не найдена\\. Попробуйте снова\\.",
                    parse_mode="MarkdownV2"
                )
                return

            try:
                task_name = setup.task_buttons[priority_index][0]
            except IndexError:
                await callback.message.answer("⚠ *Ошибка\\: задача не найдена\\!* Попробуйте снова\\.",
                                              parse_mode="MarkdownV2")
                return

            # Устанавливаем новый приоритет
            task_priority_edit_buttons = setup.task_priority_edit_buttons
            for priority in task_priority_edit_buttons:
                if priority[1] == callback.data:
                    task_priority = priority[2]
                    task_priority_index = priority[3]

            if len(setup.task_buttons[priority_index]) < 3:
                setup.task_buttons[priority_index].append(task_priority_index)
            else:
                setup.task_buttons[priority_index][2] = task_priority_index

            await data.set_task()
            await callback.message.answer(
                f"*Приоритет задачи* `{task_name}` изменен на *{task_priority.replace('(', '\\(').replace(')', '\\)')}*",
                parse_mode="MarkdownV2"
            )

            await callback.answer()

    async def deadline_selected(self, callback: CallbackQuery, state: FSMContext):
        from src.api import setup
        if callback.data.startswith("change_deadline:"):
            _, deadline_index = callback.data.split(":")
            deadline_index = int(deadline_index)

            try:
                task_name = setup.task_buttons[deadline_index][0]
            except IndexError:
                await callback.message.answer("⚠ *Ошибка\\: задача не найдена\\!* Попробуйте снова\\.",
                                              parse_mode="MarkdownV2")
                return

            await state.update_data(deadline_index=deadline_index)

            await state.set_state(UserInputHandler.waiting_for_deadline)

            await callback.message.answer(
                f"*Когда вы хотите завершить задачу* {task_name}\\:",
                parse_mode="MarkdownV2"
            )

            await callback.answer()

    async def status_selected(self, callback: CallbackQuery, state: FSMContext):
        from src.api import setup, data
        if callback.data.startswith("change_status:"):
            _, status_index = callback.data.split(":")
            status_index = int(status_index)

            try:
                task_name = setup.task_buttons[status_index][0]
            except IndexError:
                await callback.message.answer("⚠ *Ошибка\\: задача не найдена\\!* Попробуйте снова\\.",
                                              parse_mode="MarkdownV2")
                return

            # Сохраняем status_index в состояние
            await state.update_data(status_index=status_index)

            await callback.message.answer(
                f"*Какой статус вы хотите поставить в задаче* `{task_name}`\\?",
                reply_markup=setup.task_status_edit_keyboard,
                parse_mode="MarkdownV2"
            )

            await callback.answer()

        elif callback.data in ["New", "In_Progress", "On_Hold", "Completed"]:  # Обрабатываем статус
            global task_status, task_status_index
            user_data = await state.get_data()
            priority_index = user_data.get("status_index")

            if priority_index is None:
                await callback.message.answer(
                    "⚠ *Ошибка\\:* задача не найдена\\. Попробуйте снова\\.",
                    parse_mode="MarkdownV2"
                )
                return

            try:
                task_name = setup.task_buttons[priority_index][0]
            except IndexError:
                await callback.message.answer("⚠ *Ошибка\\: задача не найдена\\!* Попробуйте снова\\.",
                                              parse_mode="MarkdownV2")
                return

            # Устанавливаем новый приоритет
            task_status_edit_buttons = setup.task_status_edit_buttons
            for status in task_status_edit_buttons:
                if status[1] == callback.data:
                    task_status = status[0]
                    task_status_index = status[2]

            print(task_status_index)
            setup.task_buttons[priority_index][3] = task_status_index
            print(setup.task_buttons)

            await data.set_task()
            await callback.message.answer(
                f"*Статус задачи* `{task_name}` изменен на *{task_status.replace('(', '\\(').replace(')', '\\)')}*",
                parse_mode="MarkdownV2"
            )

            await callback.answer()