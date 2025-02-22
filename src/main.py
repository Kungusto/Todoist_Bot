import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command 
from api.config import commands
from api.config import token
from api.Handlers import CommandHandler, ButtonHandler
from api.Register import Register

logging.basicConfig(level=logging.INFO)

bot = Bot(token=token)
dp = Dispatcher()

handler = CommandHandler(bot, dp)

button_handler = ButtonHandler()  # Создаём экземпляр обработчика кнопок
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
