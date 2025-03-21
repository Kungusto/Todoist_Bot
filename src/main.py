import asyncio
import logging
import sys
from pathlib import Path

from aiogram import Bot, Dispatcher, Router
sys.path.append(str(Path(__file__).parent.parent))
logging.basicConfig(level=logging.INFO)

from api.misc.notifications import Notifications
from src.api.handlers import CommandHandler, ButtonNavHandler, ButtonEditTaskHandler, Auth
from src.api.register import Register
from src.api.misc.register import Register as MiscRegister
from src.api.misc.handlers import Misc, Sort_Task, FilterTask, Settings
from src.api.misc.notifications import Notifications
from src.api import setup


bot = Bot(token=setup.token)

dp = Dispatcher()
router = Router()

handler = CommandHandler(bot, dp)

auth = Auth()
button_nav_handler = ButtonNavHandler(bot, dp)
button_edit_task_handler = ButtonEditTaskHandler(bot, dp)
register = Register(dp, router, handler, button_nav_handler, button_edit_task_handler, auth)
register.register_all()

misc = Misc()
sort = Sort_Task(button_nav_handler, register)
filter = FilterTask(button_nav_handler, register)
settings = Settings()
misc_register = MiscRegister(dp, router, misc, sort, filter, settings)
misc_register.register_all()

notifications = Notifications(router.callback_query)

async def main():
    await asyncio.gather(notifications.start_all_tasks())
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot has been stopped.")
        sys.exit(0)