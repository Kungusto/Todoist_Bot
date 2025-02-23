import asyncio
from aiogram import types, Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
from api import settings
import logging


class BaseHandler:
    def __init__(self, bot: Bot, dispatcher: Dispatcher):
        self.bot = bot
        self.dispatcher = dispatcher
        self.bot_messages = {}  # Храним ID сообщений бота
        self.welcome_message_id = {}  # Храним ID приветственного сообщения

    async def clear_chat(self, chat_id: int):
        """Удаляет все сообщения бота, кроме приветственного"""
        if chat_id in self.bot_messages:
            messages_to_delete = [msg_id for msg_id in self.bot_messages[chat_id] 
                                  if msg_id != self.welcome_message_id.get(chat_id)]
            for msg_id in messages_to_delete:
                await self.safe_delete_message(chat_id, msg_id)

    async def safe_delete_message(self, chat_id: int, message_id: int):
        """Безопасное удаление сообщений"""
        try:
            await self.bot.delete_message(chat_id=chat_id, message_id=message_id)
            self.bot_messages[chat_id].remove(message_id)
            print(f"[INFO] Удалено сообщение {message_id} в чате {chat_id}")
        except Exception as e:
            if "message to delete not found" not in str(e):
                print(f"[ERROR] Ошибка при удалении сообщения {message_id}: {e}")

    async def track_message(self, message: Message, is_welcome=False):
        """Запоминает ID сообщений бота"""
        chat_id = message.chat.id
        if chat_id not in self.bot_messages:
            self.bot_messages[chat_id] = []
        self.bot_messages[chat_id].append(message.message_id)
        if is_welcome:
            self.welcome_message_id[chat_id] = message.message_id
        print(f"[DEBUG] Отслеживается сообщение {message.message_id} в чате {chat_id}")

    

    async def handle_callback(self, callback: CallbackQuery):
        """Обрабатывает callback-запросы от кнопок"""
        
        logging.info(f"CallbackQuery данные: {callback}")
    
        if not callback.message:
            await callback.answer("Ошибка: нет связанного сообщения!", show_alert=True)
            return
    
        chat_id = callback.message.chat.id
        message_id = callback.message.message_id
    
        if self.welcome_message_id.get(chat_id) == message_id:
            new_text = self.get_callback_response(callback.data)
            await self.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=new_text,
                reply_markup=settings.nav_keyboard
            )
        else:
            await self.safe_delete_message(chat_id, message_id)
    
        await callback.answer()
    
    def get_callback_response(self, data: str) -> str:
        """Возвращает текст в зависимости от нажатой кнопки"""
        responses = {
            "list_tasks": "📋 Список ваших задач...",
            "add_task": "Введите новую задачу:",
            "settings": "⚙ Открываем настройки..."
        }
        return responses.get(data, "Неизвестная команда")


class CommandHandler(BaseHandler):
    async def start_command(self, message: Message):
        """Обработчик команды /start"""
        await self.clear_chat(message.chat.id)
        sent_message = await message.answer(
            "Привет! Я твой Todoist-бот.\nДля работы с задачами используй кнопки внизу.",
            reply_markup=settings.nav_keyboard
        )
        await self.track_message(sent_message, is_welcome=True)

    async def help_command(self, message: Message):
        """Обработчик команды /help"""
        await self.clear_chat(message.chat.id)
        sent_message = await message.answer(
            "Доступные команды:\n"
            "/start - запуск бота\n"
            "/help - помощь\n"
            "/create - создать задачу\n"
            "/tasks - показать все задачи"
        )
        await self.track_message(sent_message)


class ButtonNavHandler(BaseHandler):
    @dp.callback_query_handler(lambda c: c.data == "list_tasks")
    async def list_tasks(callback: types.CallbackQuery):
        await callback.answer()  # Закрывает "часики" в кнопке
        await callback.message.edit_text(
            "Ваши задачи:", reply_markup=task_keyboard
        )
    
    async def add_task(self, callback: CallbackQuery):
        """Кнопка 'Добавить задачу'"""
        await self.handle_callback(callback)

    async def settings(self, callback: CallbackQuery):
        """Кнопка 'Настройки'"""
        await self.handle_callback(callback)
        