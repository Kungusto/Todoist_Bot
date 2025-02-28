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
        from src.api import settings
        settings.current_state = 1
        await message.answer(
            "**Привет\\!** Я твой *Todoist\\-бот*\\.\n"
            "Для начала работы с задачами используйте команды или кнопки внизу\\.",
            reply_markup=settings.nav_keyboard,
            parse_mode="MarkdownV2"
        )

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
        from src.api import settings
        settings.current_state = 2
        await message.answer(
            "📋 *Мои задачи*",
            reply_markup=settings.task_keyboard,
            parse_mode="MarkdownV2"
        )

    async def add_task(self, message: Message, state: FSMContext):
        """Запрашивает у пользователя задачу и ждёт её ввод."""
        await UserInputHandler.get_user_input(message, state, "*Введите новую задачу\\:*", parse_mode="MarkdownV2")

    async def settings(self, message: Message):
        await message.answer("⚙ *Открываем настройки\\.\\.\\.*", parse_mode="MarkdownV2")

    async def task_selected(self, callback: CallbackQuery, state: FSMContext):
        """Обработчик нажатий на задачу из списка."""
        from src.api import settings

        if callback.data.startswith("task:"):
            _, task_index = callback.data.split(":")
            task_index = int(task_index)

            try:
                task_name = settings.task_buttons[task_index][0]
            except IndexError:
                await callback.answer("⚠ *Ошибка\\: задача не найдена\\!*", parse_mode="MarkdownV2")
                return

            # Сохраняем индекс выбранной задачи для редактирования
            await state.update_data(editing_task_index=task_index)

            # Обновляем callback_data для кнопок редактирования, включая подзадачу
            for button in settings.task_edit_buttons:
                parts = button[1].split(":")
                if len(parts) == 2 and parts[1].isdigit():
                    button[1] = f"{parts[0]}:{task_index}"

            settings.task_edit_keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text=btn[0], callback_data=btn[1])]
                    for btn in settings.task_edit_buttons
                ]
            )

            print(settings.task_edit_buttons)

            # Извлекаем подзадачи для выбранной задачи
            subtasks = settings.task_buttons[task_index][1] if len(settings.task_buttons[task_index]) > 1 else []
            formatted_subtasks = "\n".join([f"• {sub}" for sub in subtasks]) if subtasks else "Нет подзадач"

            # Проверяем, есть ли приоритет у задачи
            if len(settings.task_priority) > task_index and settings.task_priority[task_index][0]:
                priority = settings.task_priority[task_index]
            else:
                priority = "Не установлен"

            await callback.message.answer(
                f"*Вы выбрали задачу\\:*\n"
                f"`{task_name}`\n\n"
                f"*Приоритет:* `{priority}`\n\n"
                f"*Подзадачи:*\n{formatted_subtasks}",
                reply_markup=settings.task_edit_keyboard,
                parse_mode="MarkdownV2"
            )

            settings.current_state = 3
            await callback.answer()


class ButtonEditTaskHandler(BaseHandler):
    async def edit_task_selected(self, callback: CallbackQuery, state: FSMContext):
        """Обработчик редактирования основной задачи."""
        from src.api import settings

        print(f"Received callback data: {callback.data}")

        if callback.data.startswith("edit_task:"):
            _, task_index = callback.data.split(":")
            task_index = int(task_index)

            try:
                task_name = settings.task_buttons[task_index][0]
            except IndexError:
                await callback.message.answer("⚠ *Ошибка\\: задача не найдена\\!* Попробуйте снова\\.", parse_mode="MarkdownV2")
                return

            await state.update_data(editing_task_index=task_index)

            await UserInputHandler.get_edit_input(
                callback.message, state, f"*Что вы хотите изменить в задаче* `{task_name}`\\?", parse_mode="MarkdownV2"
            )

            await callback.answer()

    async def subtask_seleted(self, callback: CallbackQuery, state: FSMContext):
        """Обработчик для добавления подзадачи."""
        from src.api import settings

        if callback.data.startswith("add_subtasks:"):
            _, task_index = callback.data.split(":")
            task_index = int(task_index)

            try:
                task_name = settings.task_buttons[task_index][0]
                await callback.message.answer(
                    f"*Какой приоритет вы хотите поставить в задаче* `{task_name}`\\? ",
                    reply_markup=settings.task_priority_edit_keyboard,
                    parse_mode="MarkdownV2"
                )
            except Exception as e:
                print(f"Error while sending message: {e}")
                await callback.message.answer("⚠ Произошла ошибка при отправке сообщения. Попробуйте позже.")

            # Обновляем состояние с отдельным ключом для подзадачи
            await state.update_data(subtask_index=task_index)

            await callback.answer()

    async def priority_selected(self, callback: CallbackQuery, state: FSMContext):
        from src.api import settings
        print(f"Received callback data: {callback.data}")

        if callback.data.startswith("change_priority:"):
            _, priority_index = callback.data.split(":")
            priority_index = int(priority_index)

            try:
                task_name = settings.task_buttons[priority_index][0]
            except IndexError:
                await callback.message.answer("⚠ *Ошибка\\: задача не найдена\\!* Попробуйте снова\\.",
                                              parse_mode="MarkdownV2")
                return

            # Сохраняем priority_index в состояние
            await state.update_data(priority_index=priority_index)

            await callback.message.answer(
                f"*Какой приоритет вы хотите поставить в задаче* `{task_name}`\\?",
                reply_markup=settings.task_priority_edit_keyboard,
                parse_mode="MarkdownV2"
            )

            await callback.answer()

        elif callback.data in ["Low", "Medium", "High"]:  # Обрабатываем приоритет
            global task_priority
            user_data = await state.get_data()
            priority_index = user_data.get("priority_index")

            if priority_index is None:
                await callback.message.answer("⚠ *Ошибка:* задача не найдена. Попробуйте снова.",
                                              parse_mode="MarkdownV2")
                return

            try:
                task_name = settings.task_buttons[priority_index][0]
            except IndexError:
                await callback.message.answer("⚠ *Ошибка\\: задача не найдена\\!* Попробуйте снова\\.",
                                              parse_mode="MarkdownV2")
                return

            # Устанавливаем новый приоритет
            task_priority_edit_buttons = settings.task_priority_edit_buttons
            for priority in task_priority_edit_buttons:
                if priority[1] == callback.data:
                    task_priority = priority[2]

            settings.task_priority[priority_index] = task_priority

            await callback.message.answer(
                f"*Приоритет задачи* `{task_name}` изменен на *{task_priority.replace('(', '\\(').replace(')', '\\)')}*",
                parse_mode="MarkdownV2"
            )

            await callback.answer()

