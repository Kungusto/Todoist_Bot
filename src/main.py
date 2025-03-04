import asyncio
import logging
import sys
from pathlib import Path

from aiogram import Bot, Dispatcher, Router
from api.handlers import CommandHandler, ButtonNavHandler, ButtonEditTaskHandler
from src.api.register import Register
from src.api import setup

#from src.config import settings
#убрал импорт т. к. появляются ошибки (скорее всего из-за ненастроенной бд)


sys.path.append(str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.INFO)

bot = Bot(token=setup.token)


dp = Dispatcher()
router = Router()

handler = CommandHandler(bot, dp)

button_nav_handler = ButtonNavHandler(bot, dp)  # Создаём экземпляр обработчика кнопок
button_edit_task_handler = ButtonEditTaskHandler(bot, dp)
register = Register(dp, router, handler, button_nav_handler, button_edit_task_handler)  # Передаём его в register
register.register_all()

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot has been stopped.")
        sys.exit(0)
