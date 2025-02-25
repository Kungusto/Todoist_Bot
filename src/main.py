import asyncio
import logging
import sys
from pathlib import Path

from aiogram import Bot, Dispatcher, Router
from api.handlers import CommandHandler, ButtonNavHandler
from src.api.register import Register

from src.api import settings
#убрал импорт т. к. появляются ошибки (скорее всего из-за ненастроенной бд), ну ладно так и быть верну


sys.path.append(str(Path(__file__).parent.parent))


logging.basicConfig(level=logging.INFO)

# bot = Bot(token=token) - сорян( мне так не удобно тестить
bot = Bot(token=settings.token)
'''
создаешь файлик .env и пишешь туда(пример) :
    DB_PORT=порт. обычно 5432 (по умолчанию)
    DB_HOST=хост где она размещена. в твоем случае localhost
    DB_PASS=пароль
    DB_NAME=имя базы данных
    DB_USER=под каким пользователем база создана

    TOKEN=8090759361:AAGkfIL43EeWm5NJ7CZt3I8C-ReUZktRH_U
'''

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
