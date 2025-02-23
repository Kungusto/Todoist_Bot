import asyncio
from aiogram import types, Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
from api import settings
import logging


from aiogram.types import Message
from api import settings  

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

class CommandHandler(BaseHandler):  
    def __init__(self, bot, dispatcher):
        super().__init__(bot, dispatcher)

    async def start_command(self, message: Message):  
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
        sent_message = await message.answer("📋 Мои задачи", reply_markup=settings.task_keyboard)

    async def add_task(self, message: Message):
        sent_message = await message.answer("Введите новую задачу:")

    async def settings(self, message: Message):
        sent_message = await message.answer("⚙ Открываем настройки...")