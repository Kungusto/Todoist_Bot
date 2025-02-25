from aiogram.types import Message, CallbackQuery
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
        await message.answer("📋 Мои задачи", reply_markup=settings.task_keyboard)

    async def add_task(self, message: Message, state: FSMContext):
        """Запрашивает у пользователя задачу и ждёт её ввод."""
        await UserInputHandler.get_user_input(message, state, "Введите новую задачу:")

        current_state = await state.get_state()
        print(f"📌 Текущее состояние FSM: {current_state}")  # 🔍 Дебаг

    async def settings(self, message: Message):
        await message.answer("⚙ Открываем настройки...")

    async def task_selected(self, callback: CallbackQuery):
        """Обработчик нажатий на задачи"""
        from src.api import settings
        await callback.message.answer(f"Вы выбрали задачу: {callback.data}",
                                      reply_markup=settings.task_edit_keyboard)
        await callback.answer()  # Закрываем всплывающее уведомление

class ButtonEditTaskHandler(BaseHandler):
    pass



