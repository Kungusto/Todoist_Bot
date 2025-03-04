from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext

from src.api.userInputHandler import UserInputHandler


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
        from src.api import setup, data
        setup.current_state = 1
        await message.answer(
            "**Привет\\!** Я твой *Todoist\\-бот*\\.\n"
            "Для начала работы с задачами используйте команды или кнопки внизу\\.",
            reply_markup=setup.nav_keyboard,
            parse_mode="MarkdownV2"
        )
        data.user_id = message.from_user.id
        await data.GetTask()

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
        setup.current_state = 2
        await message.answer(
            "📋 *Мои задачи*",
            reply_markup=setup.task_keyboard,
            parse_mode="MarkdownV2"
        )

    async def add_task(self, message: Message, state: FSMContext):
        """Запрашивает у пользователя задачу и ждёт её ввод."""
        await UserInputHandler.get_user_input(message, state, "*Введите новую задачу\\:*", parse_mode="MarkdownV2")

    async def settings(self, message: Message):
        await message.answer("⚙ *Открываем настройки\\.\\.\\.*", parse_mode="MarkdownV2")

    async def task_selected(self, callback: CallbackQuery, state: FSMContext):
        """Обработчик нажатий на задачу из списка."""
        from src.api import setup

        if callback.data.startswith("task:"):
            _, task_index = callback.data.split(":")
            task_index = int(task_index)

            try:
                task_name = setup.task_buttons[task_index][0]
            except IndexError:
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

            print(setup.task_edit_buttons)

            task_data = setup.task_buttons[task_index]

            task_name = task_data[0] if len(task_data) > 0 else "Без названия"

            subtasks = setup.task_buttons[task_index][1] if len(setup.task_buttons[task_index]) > 1 else []
            subtasks = "\n".join([f"• {sub}" for sub in subtasks]) if subtasks else "Нет подзадач"

            priority = task_data[2] if len(task_data) > 2 else "Не установлен"
            status = task_data[3] if len(task_data) > 3 else "Не установлен"
            deadline = task_data[4] if len(task_data) > 4 else "Не установлен"

            await callback.message.answer(
                f"*Вы выбрали задачу\\:* `{task_name}`\n\n"
                f"*Подзадачи:*\n{subtasks}\n\n"
                f"*Приоритет:* `{priority}`\n"
                f"*Статус:* `{status}`\n"
                f"*Дедлайн:* `{deadline}`\n\n",
                reply_markup=setup.task_edit_keyboard,
                parse_mode="MarkdownV2"
            )

            setup.current_state = 3
            await callback.answer()


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
        from src.api import setup

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
            global task_priority
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

            if len(setup.task_buttons[priority_index]) < 3:
                setup.task_buttons[priority_index].append(task_priority)
            else:
                setup.task_buttons[priority_index][2] = task_priority

            await callback.message.answer(
                f"*Приоритет задачи* `{task_name}` изменен на *{task_priority.replace('(', '\\(').replace(')', '\\)')}*",
                parse_mode="MarkdownV2"
            )

            await callback.answer()

