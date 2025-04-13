import asyncio
from datetime import datetime, timedelta

from aiogram import Bot
from src.utils.init_dbmanager import get_db
from src.utils.timezone_utils import get_user_timezone
from src.api import data, setup


class Notifications:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def task_time_out(self):
        """Уведомляет о просроченных задачах с учётом часового пояса пользователя."""
        while True:
            user_tz = await get_user_timezone()
            now = datetime.now(user_tz)

            for task in setup.task_buttons:
                task_time_str = task[4]

                # Пропускаем задачу, если время отсутствует
                if not task_time_str:
                    continue

                try:
                    task_time = datetime.strptime(task_time_str, "%Y-%m-%d-%H-%M-%S").replace(tzinfo=user_tz)
                except Exception as e:
                    print(f"Ошибка разбора даты задачи ({task[0]}): {task_time_str} -> {e}")
                    continue

                text = f"❌ *Просрочена задача:* {task[0]}!"

                # Проверка: уже отправлялось ли это уведомление
                already_sent = any(text == notif[0] for notif in setup.notifications_button)

                if task_time < now and not already_sent:
                    if setup.settings["notifications"]:
                        await self.bot.send_message(setup.user_id, text, parse_mode="MarkdownV2")
                    setup.notifications_button.append([text, now.strftime("%Y-%m-%d-%H-%M")])
                    await data.set_notifications()

            await asyncio.sleep(120)

    async def task_reminders(self):
        """Уведомления за 1 час и 10 минут до дедлайна с учётом часового пояса пользователя."""
        while True:
            user_tz = await get_user_timezone()
            now = datetime.now(user_tz)

            for task in setup.task_buttons:
                task_time_str = task[4]

                if not task_time_str:
                    continue

                try:
                    task_time = datetime.strptime(task_time_str, "%Y-%m-%d-%H-%M-%S").replace(tzinfo=user_tz)
                except Exception as e:
                    print(f"Ошибка разбора даты задачи ({task[0]}): {task_time_str} -> {e}")
                    continue

                hour_text = f"⏳ *Остался 1 час до дедлайна:* {task[0]}!"
                min10_text = f"⚠ *Осталось 10 минут до дедлайна:* {task[0]}!"

                if now + timedelta(hours=1) >= task_time > now:
                    already_sent = any(hour_text == notif[0] for notif in setup.notifications_button)
                    if not already_sent and setup.settings["notifications"]:
                        await self.bot.send_message(setup.user_id, hour_text, parse_mode="MarkdownV2")
                        setup.notifications_button.append([hour_text, now.strftime("%Y-%m-%d-%H-%M")])
                        await data.set_notifications()

                elif now + timedelta(minutes=10) >= task_time > now:
                    already_sent = any(min10_text == notif[0] for notif in setup.notifications_button)
                    if not already_sent and setup.settings["notifications"]:
                        await self.bot.send_message(setup.user_id, min10_text, parse_mode="MarkdownV2")
                        setup.notifications_button.append([min10_text, now.strftime("%Y-%m-%d-%H-%M")])
                        await data.set_notifications()

            await asyncio.sleep(120)

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

            today = target_time.strftime("%Y-%m-%d")
            today_tasks = [
                task[0] for task in setup.task_buttons
                if task[4].startswith(today)
            ]

            if today_tasks:
                task_list = "\n".join([f"📌 {task}" for task in today_tasks])
                await self.bot.send_message(setup.user_id, f"📅 *Задачи на сегодня:*\n{task_list}", parse_mode="MarkdownV2")
            else:
                await self.bot.send_message(setup.user_id, "✅ *На сегодня задач нет!*", parse_mode="MarkdownV2")

    async def technical_notifications(self):
        """Технические уведомления (ошибки подключения)."""
        while True:
            try:
                async for db in get_db():
                    if not db:
                        await self.bot.send_message(
                            setup.user_id,
                            "⚠ *Ошибка подключения к базе данных!* Попробуйте позже.",
                            parse_mode="MarkdownV2"
                        )
                        continue
                    break
            except Exception as e:
                await self.bot.send_message(
                    setup.user_id,
                    f"❌ *Ошибка работы с базой данных:* {str(e)}",
                    parse_mode="MarkdownV2"
                )

            await asyncio.sleep(300)

    async def start_all_tasks(self):
        """Запускает все асинхронные методы уведомлений, если пользователь авторизован."""
        from src.api import setup
        while True:
            if setup.user_id == -1 and setup.task_buttons == []:
                print("⛔ Уведомления не запущены: пользователь не авторизован.")
                await asyncio.sleep(1)
            else:
                break

        tasks = []
        for attr in dir(self):
            method = getattr(self, attr)
            if callable(method) and asyncio.iscoroutinefunction(method) and attr != "start_all_tasks":
                tasks.append(asyncio.create_task(method()))

        await asyncio.gather(*tasks)

