import asyncio
import logging
import sys
from pathlib import Path

from aiogram import Bot, Dispatcher, Router

from src.api.handlers import CommandHandler, ButtonNavHandler, ButtonEditTaskHandler, Auth
from src.api.register import Register
from src.api import setup

sys.path.append(str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.INFO)

bot = Bot(token=setup.token)

dp = Dispatcher()
router = Router()

handler = CommandHandler(bot, dp)

auth = Auth()
button_nav_handler = ButtonNavHandler(bot, dp)
button_edit_task_handler = ButtonEditTaskHandler(bot, dp)
register = Register(dp, router, handler, button_nav_handler, button_edit_task_handler, auth)
register.register_all()

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot has been stopped.")
        sys.exit(0)