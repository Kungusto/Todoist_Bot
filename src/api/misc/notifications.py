import asyncio
from datetime import datetime, timedelta

from aiogram.types import CallbackQuery
from src.utils.init_dbmanager import get_db
from src.utils.timezone_utils import get_user_timezone

class Notifications:

    def __init__(self, callback: CallbackQuery):
        self.callback = callback

    async def task_time_out(self):
        """Уведомляет о просроченных задачах с учётом часового пояса пользователя."""
        while True:
            from src.api import setup
            user_tz = await get_user_timezone()
            now = datetime.now(user_tz)

            for task in setup.task_buttons:
                task_time = datetime.strptime(task[4], "%Y-%m-%d-%H-%M").replace(tzinfo=user_tz)
                if task_time < now:
                    if setup.settings["notifications"]:
                        await self.callback.message.answer(
                            f"❌ *Просрочена задача:* {task[0]}!", parse_mode="MarkdownV2"
                        )
                    setup.notifications_button.append(f"❌ *Просрочена задача:* {task[0]}!")

            await asyncio.sleep(60)

    async def task_reminders(self):
        """Уведомления за 1 час и 10 минут до дедлайна с учётом часового пояса пользователя."""
        while True:
            from src.api import setup
            user_tz = await get_user_timezone()
            now = datetime.now(user_tz)

            for task in setup.task_buttons:
                task_time = datetime.strptime(task[4], "%Y-%m-%d-%H-%M").replace(tzinfo=user_tz)

                if now + timedelta(hours=1) >= task_time > now:
                    if setup.settings["notifications"]:
                        await self.callback.message.answer(
                            f"⏳ *Остался 1 час до дедлайна:* {task[0]}!", parse_mode="MarkdownV2"
                        )

                if now + timedelta(minutes=10) >= task_time > now:
                    if setup.settings["notifications"]:
                        await self.callback.message.answer(
                            f"⚠ *Осталось 10 минут до дедлайна:* {task[0]}!", parse_mode="MarkdownV2"
                        )

            await asyncio.sleep(60)

    async def daily_task_summary(self):
        """Отправляет задачи на сегодня в 08:00 по времени пользователя."""
        while True:
            user_tz = await get_user_timezone()
            now = datetime.now(user_tz)
            target_time = now.replace(hour=8, minute=0, second=0, microsecond=0)

            if now > target_time:
                target_time += timedelta(days=1)

            sleep_time = (target_time - now).total_seconds()
            await asyncio.sleep(sleep_time)

            from src.api import setup
            today = now.strftime("%Y-%m-%d")

            today_tasks = [
                task[0] for task in setup.task_buttons
                if task[4].startswith(today)
            ]

            if today_tasks:
                task_list = "\n".join([f"📌 {task}" for task in today_tasks])
                await self.callback.message.answer(f"📅 *Задачи на сегодня:*\n{task_list}", parse_mode="MarkdownV2")
            else:
                await self.callback.message.answer("✅ *На сегодня задач нет!*", parse_mode="MarkdownV2")

    async def technical_notifications(self):
        """Технические уведомления (ошибки подключения)."""
        while True:
            try:
                async for db in get_db():
                    if not db:
                        await self.callback.message.answer(
                            "⚠ *Ошибка подключения к базе данных!* Попробуйте позже."
                        )
                        continue
                    break
            except Exception as e:
                await self.callback.message.answer(f"❌ *Ошибка работы с базой данных:* {str(e)}")

            await asyncio.sleep(300)

    async def start_all_tasks(self):
        """Запускает все асинхронные методы уведомлений."""
        tasks = []
        for attr in dir(self):
            method = getattr(self, attr)
            if callable(method) and asyncio.iscoroutinefunction(method) and attr != "start_all_tasks":
                tasks.append(asyncio.create_task(method()))
        await asyncio.gather(*tasks)