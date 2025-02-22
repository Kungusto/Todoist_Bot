from aiogram.types import Message
from api import config  

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
        await message.answer(
            "Привет! Я твой Todoist-бот.\nДля начала работы с задачами используйте команды или кнопки внизу.",
            reply_markup=config.nav_keyboard  # Теперь клавиатура подключена правильно
        )

    async def help_command(self, message: Message):
        await message.answer(
            "Доступные команды:\n"
            "/start - запуск бота\n"
            "/help - помощь по боту\n"
            "/create - создание новой задачи\n"
            "/tasks - показать все задачи"
        )

class ButtonHandler:
    async def list_tasks(self, message: Message):
        await message.answer("📋 Вот ваши задачи: ...")
    
    async def add_task(self, message: Message):
        await message.answer("Введите новую задачу:")
    
    async def settings(self, message: Message):
        await message.answer("⚙ Открываем настройки...")
        