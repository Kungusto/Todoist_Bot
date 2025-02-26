from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from src.api.UserInputHandler import UserInputHandler


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
            "Привет! Я твой Todoist-бот.\nДля начала работы с задачами используйте команды или кнопки внизу.",
            reply_markup=settings.nav_keyboard
        )

    async def help_command(self, message: Message):
        await message.answer(
            "Доступные команды:\n"
            "/start - запуск бота\n"
            "/help - помощь по боту\n"
            "/create - создание новой задачи\n"
            "/tasks - показать все задачи"
        )

class ButtonNavHandler(BaseHandler):
    async def list_tasks(self, message: Message):
        from src.api import settings
        settings.current_state = 2
        await message.answer("📋 Мои задачи", reply_markup=settings.task_keyboard)

    async def add_task(self, message: Message, state: FSMContext):
        """Запрашивает у пользователя задачу и ждёт её ввод."""
        await UserInputHandler.get_user_input(message, state, "Введите новую задачу:")

    async def settings(self, message: Message):
        await message.answer("⚙ Открываем настройки...")

    async def task_selected(self, callback: CallbackQuery, state: FSMContext):
        """Обработчик нажатий на задачи"""
        from src.api import settings

        if callback.data.startswith("task:"):
            _, task_index = callback.data.split(":")  # Разделяем строку
            task_index = int(task_index)  # Преобразуем в число

            # Получаем название задачи
            try:
                task_name = settings.task_buttons[task_index][0]
            except IndexError:
                await callback.answer("⚠ Ошибка: задача не найдена!")
                return

            # Сохраняем индекс задачи
            await state.update_data(editing_task_index=task_index)

            # Обновляем кнопки
            for button in settings.task_edit_buttons:
                parts = button[1].split(":")
                if len(parts) == 2 and parts[1].isdigit():
                    button[1] = f"{parts[0]}:{task_index}"
            settings.task_edit_keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text=btn[0], callback_data=btn[1] if len(btn) > 1 else btn[0])]
                    for btn in settings.task_edit_buttons
                ]
            )

            print(settings.task_edit_buttons)

            await callback.message.answer(
                f"Вы выбрали задачу: {task_name}",
                reply_markup=settings.task_edit_keyboard
            )

            settings.current_state = 3
            await callback.answer()


class ButtonEditTaskHandler(BaseHandler):
    async def edit_task_selected(self, callback: CallbackQuery, state: FSMContext):
        """Обработчик выбора задачи для редактирования."""
        from src.api import settings

        # Логируем callback.data, чтобы увидеть, что мы получаем
        print(f"Received callback data: {callback.data}")

        # Разбираем callback_data для получения индекса задачи
        if callback.data.startswith("edit_task:"):
            _, task_index = callback.data.split(":")  # Разделяем строку по ":"
            task_index = int(task_index)  # Преобразуем в число

            # Получаем название задачи
            try:
                task_name = settings.task_buttons[task_index][0]
            except IndexError:
                await callback.message.answer("⚠ Ошибка: задача не найдена! Попробуйте снова.")
                return

            # Сохраняем индекс задачи, которую будем редактировать
            await state.update_data(editing_task_index=task_index)

            # Вместо message передаем callback.message
            await UserInputHandler.get_edit_input(callback.message, state, f'Что вы хотите изменить в задаче "{task_name}"?')

            # Переводим в состояние редактирования
            settings.current_state = 4  # Это состояние для редактирования задачи
            await callback.answer()
