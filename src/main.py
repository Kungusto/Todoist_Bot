# -------- Без этих команд он не видит папку src в импортах
import sys
from pathlib import Path 

sys.path.append(str(Path(__file__).parent.parent))
# --------

from src.config import settings

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command 
from api.settings import commands
from api.settings import token
from api.handlers import CommandHandler, ButtonNavHandler
from api.register import Register


logging.basicConfig(level=logging.INFO)

# bot = Bot(token=token) - сорян( мне так не удобно тестить
bot = Bot(token=settings.TOKEN) # ща объясню что это
'''
создаешь файлик .env и пишешь туда(пример) :
    DB_PORT=*порт. обычно 5432 (по умолчанию)*
    DB_HOST=*хост где она размещена. в твоем случае localhost*
    DB_PASS=*пароль*
    DB_NAME=*имя базы данных*
    DB_USER=*под каким пользователем база создана*

    TOKEN=8090759361:AAGkfIL43EeWm5NJ7CZt3I8C-ReUZktRH_U
'''
dp = Dispatcher()

handler = CommandHandler(bot, dp)

button_handler = ButtonNavHandler(bot, dp)  # Создаём экземпляр обработчика кнопок
register = Register(dp, handler, button_handler)  # Передаём его в register
register.register_all()

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot has been stopped.")
        sys.exit(0)
