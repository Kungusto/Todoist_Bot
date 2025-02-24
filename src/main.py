import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, Router, F
from api.settings import token
from api.handlers import CommandHandler, ButtonNavHandler
from api.register import Register

logging.basicConfig(level=logging.INFO)

bot = Bot(token=token)
dp = Dispatcher()
router = Router()

handler = CommandHandler(bot, dp)

button_handler = ButtonNavHandler(bot, dp)  # Создаём экземпляр обработчика кнопок
register = Register(dp, router, handler, button_handler)  # Передаём его в register
register.register_all()

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot has been stopped.")
        sys.exit(0)
