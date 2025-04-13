from datetime import datetime
from aiogram.types import CallbackQuery

from src.api.handlers import ButtonNavHandler
from src.api.register import Register
from src.api.misc.register import Register as MiscRegister
from src.api import data

class Misc:
    async def misc_notifications(self, callback: CallbackQuery):
        from src.api import setup
        await data.get_notifications()
        await callback.message.answer("*Уведомления*\n", reply_markup=setup.notifications_keyboard, parse_mode="MarkdownV2")
        await callback.answer()

    async def misc_settings(self, callback: CallbackQuery):
        from src.api import setup
        await callback.message.answer("*Настройки*\n", reply_markup=setup.misc_settings_keyboard, parse_mode="MarkdownV2")
        await callback.answer()

    async def misc_task_filter(self, callback: CallbackQuery):
        from src.api import setup
        await callback.message.answer("*Фильтр задач*\n", reply_markup=setup.misc_task_filter_keyboard, parse_mode="MarkdownV2")
        await callback.answer()

    async def misc_task_sorting(self, callback: CallbackQuery):
        from src.api import setup
        await callback.message.answer("*Сортировка задач*\n", reply_markup=setup.misc_task_sorting_keyboard, parse_mode="MarkdownV2")
        await callback.answer()

    async def misc_profile(self, callback: CallbackQuery):
        from src.api import setup
        await callback.message.answer("*Личный профиль*\n", reply_markup=setup.misc_profile_keyboard, parse_mode="MarkdownV2")
        await callback.answer()

class Sort_Task:
    def __init__(self, nav_handler: ButtonNavHandler, register: Register):
        self.nav_handler = nav_handler
        self.register = register

    async def update_sort_setting(self, value: int):
        """Обновляет метод сортировки в setup.settings и сохраняет в БД."""
        from src.api import setup, data

        setup.settings["task_sort"] = value
        await data.set_settings()  # Сохраняем в БД

    async def sort_date_asc(self, callback: CallbackQuery):
        from src.api import setup
        setup.task_buttons.sort(key=lambda x: datetime.strptime(x[4], "%Y-%m-%d-%H-%M-%S"))

        await self.update_sort_setting(1)  # 1 — сортировка по дате (возрастание)
        await callback.message.answer("✅ Задачи отсортированы по дате (по возрастанию)")

        self.register.register_all()
        await self.nav_handler.list_tasks(callback.message)
        await callback.answer()

    async def sort_date_desc(self, callback: CallbackQuery):
        from src.api import setup
        setup.task_buttons.sort(key=lambda x: datetime.strptime(x[4], "%Y-%m-%d-%H-%M-%S"), reverse=True)

        await self.update_sort_setting(2)  # 2 — сортировка по дате (убывание)
        await callback.message.answer("✅ Задачи отсортированы по дате (по убыванию)")

        self.register.register_all()
        await self.nav_handler.list_tasks(callback.message)
        await callback.answer()

    async def sort_priority(self, callback: CallbackQuery):
        from src.api import setup
        setup.task_buttons.sort(key=lambda x: x[2])

        await self.update_sort_setting(3)  # 3 — сортировка по приоритету
        await callback.message.answer("✅ Задачи отсортированы по приоритету")

        self.register.register_all()
        await self.nav_handler.list_tasks(callback.message)
        await callback.answer()

    async def sort_alphabetically(self, callback: CallbackQuery):
        from src.api import setup
        setup.task_buttons.sort(key=lambda x: x[0].lower())

        await self.update_sort_setting(4)  # 4 — сортировка по алфавиту
        await callback.message.answer("✅ Задачи отсортированы по алфавиту")

        self.register.register_all()
        await self.nav_handler.list_tasks(callback.message)
        await callback.answer()

    async def sort_reset(self, callback: CallbackQuery):
        from src.api import setup
        setup.task_buttons = setup.task_buttons.copy()

        await self.update_sort_setting(0)  # 0 — сброс сортировки
        await callback.message.answer("✅ Сортировка сброшена, восстановлен исходный порядок")

        self.register.register_all()
        await self.nav_handler.list_tasks(callback.message)
        await callback.answer()

class FilterTask:
    def __init__(self, nav_handler: ButtonNavHandler, register: Register):
        self.nav_handler = nav_handler
        self.register = register

    async def update_filter_setting(self, value: int):
        """Обновляет метод фильтра в setup.settings и сохраняет в БД."""
        from src.api import setup, data

        setup.settings["task_filter"] = value
        await data.set_settings()  # Сохраняем в БД


    async def get_active_tasks(self, callback: CallbackQuery):
        """Фильтрует только активные (в процессе) задачи."""
        from src.api import setup
        tasks = [task for task in setup.task_buttons if task[3] == 1 or task[3] == 2]

        # Выводим сообщение после фильтрации
        await callback.message.answer("🔵 *Активные задачи отфильтрованы*",
            parse_mode="MarkdownV2"
        )
        await self.update_filter_setting(0)
        self.register.register_task(tasks)
        await self.nav_handler.list_tasks(callback.message)  # Переход к отображению задач
        await callback.answer()

    async def get_completed_tasks(self, callback: CallbackQuery):
        """Фильтрует завершённые задачи."""
        from src.api import setup
        tasks = [task for task in setup.task_buttons if task[3] == 4]

        # Выводим сообщение после фильтрации
        await callback.message.answer(
            "✅ *Завершённые задачи отфильтрованы*",
            parse_mode="MarkdownV2"
        )
        await self.update_filter_setting(1)
        self.register.register_task(tasks)
        await self.nav_handler.list_tasks(callback.message)  # Переход к отображению задач
        await callback.answer()

    async def get_overdue_tasks(self, callback: CallbackQuery):
        """Фильтрует просроченные задачи."""
        from src.api import setup
        from datetime import date
        today = date.today().strftime("%Y-%m-%d")
        tasks = [task for task in setup.task_buttons if task[4] < today]

        # Выводим сообщение после фильтрации
        await callback.message.answer(
            "⏳ *Просроченные задачи отфильтрованы*",
            parse_mode="MarkdownV2"
        )
        await self.update_filter_setting(2)
        self.register.register_task(tasks)
        await self.nav_handler.list_tasks(callback.message)  # Переход к отображению задач
        await callback.answer()

    async def get_high_priority_tasks(self, callback: CallbackQuery):
        """Фильтрует задачи с высоким приоритетом."""
        from src.api import setup
        tasks = [task for task in setup.task_buttons if task[2] == 3]

        # Выводим сообщение после фильтрации
        await callback.message.answer(
            "⚠ *Задачи с высоким приоритетом отфильтрованы*",
            parse_mode="MarkdownV2"
        )
        await self.update_filter_setting(3)
        self.register.register_task(tasks)
        await self.nav_handler.list_tasks(callback.message)  # Переход к отображению задач
        await callback.answer()

    async def get_today_tasks(self, callback: CallbackQuery):
        """Фильтрует задачи, которые запланированы на сегодня."""
        from src.api import setup
        from datetime import date
        today = date.today().strftime("%Y-%m-%d")
        tasks = [task for task in setup.task_buttons if task[4] == today]

        # Выводим сообщение после фильтрации
        await callback.message.answer(
            "📅 *Задачи на сегодня отфильтрованы*",
            parse_mode="MarkdownV2"
        )
        await self.update_filter_setting(4)
        self.register.register_task(tasks)
        await self.nav_handler.list_tasks(callback.message)  # Переход к отображению задач
        await callback.answer()

    async def get_all_tasks(self, callback: CallbackQuery):
        """Убирает фильтрацию и показывает все задачи"""
        from src.api import setup
        tasks = setup.task_buttons

        # Выводим сообщение после снятия фильтрации
        await callback.message.answer(
            "📋 *Все задачи отображаются*",
            parse_mode="MarkdownV2"
        )
        await self.update_filter_setting(5)
        self.register.register_task("all")
        await self.nav_handler.list_tasks(callback.message)  # Переход к отображению задач
        await callback.answer()

class Settings:
    async def disable_notifications(self, callback: CallbackQuery):
        """Отключает уведомления и обновляет кнопку."""
        from src.api import setup

        # Отключаем уведомления
        setup.settings["notifications"] = False
        await callback.message.answer("🔕 Уведомления отключены!")

        # Обновляем кнопки для отображения актуального состояния
        await data.set_settings()
        await self.update_misc_settings_buttons()

        await callback.answer()

    async def set_time_format(self, callback: CallbackQuery):
        """Меняет формат времени и обновляет кнопку."""
        from src.api import setup

        # Переключаем формат времени
        if setup.settings["time_format"] == 24:
            setup.settings["time_format"] = 12
        else:
            setup.settings["time_format"] = 24

        await callback.message.answer(
            f"⏰ Формат времени изменён! Теперь: {'24ч' if setup.settings['time_format'] == 24 else '12ч'}")

        # Обновляем кнопки для отображения актуального состояния
        await data.set_settings()
        await self.update_misc_settings_buttons()
        await callback.answer()

    async def set_auto_delete(self, callback: CallbackQuery):
        """Изменяет настройки автоудаления и обновляет кнопку."""
        from src.api import setup

        # Переключаем время автоудаления (например, между 7 и 30 днями)
        if setup.settings["auto_delete"] == 7:
            setup.settings["auto_delete"] = 30
        else:
            setup.settings["auto_delete"] = 7

        await callback.message.answer(
            f"🗑 Настройки автоудаления завершённых задач изменены: {setup.settings['auto_delete']} дней")

        # Обновляем кнопки для отображения актуального состояния
        await data.set_settings()
        await self.update_misc_settings_buttons()
        await callback.answer()

    async def set_ai(self, callback: CallbackQuery):
        """Включает или выключает искусственный интеллект и обновляет кнопку."""
        from src.api import setup
        is_ai = "выключён" if setup.settings["ai"] else "включён"

        # Переключаем состояние ИИ
        setup.settings["ai"] = not setup.settings["ai"]

        await callback.message.answer(f"Режим искусственного интеллекта {is_ai}")

        # Обновляем кнопки для отображения актуального состояния
        await data.set_settings()
        await self.update_misc_settings_buttons()
        await callback.answer()

    async def set_language(self, callback: CallbackQuery):
        """Переключает язык интерфейса и обновляет кнопку."""
        from src.api import setup

        # Меняем язык интерфейса (просто пример, нужно добавить логику для смены языка)
        if setup.settings["language"] == "Russian":
            setup.settings["language"] = "English"
        else:
            setup.settings["language"] = "Russian"

        await callback.message.answer(f"🌐 Язык интерфейса изменён на {setup.settings['language']}")

        # Обновляем кнопки для отображения актуального состояния
        await data.set_settings()
        await self.update_misc_settings_buttons()
        await callback.answer()

    async def update_misc_settings_buttons(self):
        """Обновляет все кнопки для отображения актуального состояния настроек."""
        from src.api import setup

        # Функция для создания текста кнопки для включения/выключения с красивым вводом
        def toggle_button(setting, on_text="Включить", off_text="Выключить"):
            if setup.settings.get(setting):
                return f"❌ {off_text}"  # Если включено, значит можно выключить
            else:
                return f"✅ {on_text}"  # Если выключено, значит можно включить

        # Обновление кнопок с учётом текущих настроек
        setup.misc_settings_buttons = [
            [toggle_button('notifications', 'Включить уведомления', 'Выключить уведомления'), "toggle_notifications"],
            [f"⏰ *Установить формат времени* ({'24ч' if setup.settings['time_format'] == 24 else '12ч'})",
             "set_time_format"],
            [f"🗑 *Автоудаление завершённых задач* ({setup.settings['auto_delete']} дней)", "set_auto_delete"],
            [toggle_button('ai', 'Включить искусственный интеллект', 'Выключить искусственный интеллект'), "toggle_ai"],
            ["🌐 *Смена языка*", "set_language"]
        ]

class Notification:
    async def delete_notification(self, callback: CallbackQuery):
        from src.api import setup
        if callback.data.startswith("delete_notification:"):
            _, notif_index = callback.data.split(":")
            try:
                notif_index = int(notif_index)
                notification = setup.notifications_button[notif_index]
            except (IndexError, ValueError):
                await callback.message.answer("⚠ *Ошибка\\: уведомление не найдено\\!* Попробуйте снова\\.", parse_mode="MarkdownV2")
                await callback.answer()
                return

            setup.notifications_button.pop(notif_index)
            await data.set_notifications()
            register = MiscRegister()
            register.register_all()
            await callback.message.edit_reply_markup("*Уведомления*\n", reply_markup=setup.notifications_keyboard, parse_mode="MarkdownV2")
            await callback.answer()