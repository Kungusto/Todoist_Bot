from aiogram import Dispatcher, Router
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Глобальные переменные
# Глобальные переменные
global main_dp, main_router, main_misc, main_sort, main_filter, main_settings, main_notification

class Register:
    def __init__(self, dp: Dispatcher = None, router: Router = None,
                 misc=None, sort=None, filter=None, settings=None, notification=None):
        global main_dp, main_router
        global main_misc, main_sort, main_filter, main_settings, main_notification

        if dp is None:
            self.dp = main_dp
            self.router = main_router
        else:
            self.dp = dp
            self.router = router
            main_dp = self.dp
            main_router = self.router

        if misc is None:
            self.misc = main_misc
            self.sort = main_sort
            self.filter = main_filter
            self.settings = main_settings
            self.notification = main_notification
        else:
            self.misc = misc
            self.sort = sort
            self.filter = filter
            self.settings = settings
            self.notification = notification

            # Обновляем глобальные переменные
            main_misc = self.misc
            main_sort = self.sort
            main_filter = self.filter
            main_settings = self.settings
            main_notification = self.notification



    def register_misc_keyboard(self):
        from src.api import setup

        setup.misc_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=btn[0], callback_data=btn[1])]
                for btn in setup.misc_buttons
            ]
        )

    def register_misc_keyboard_callback(self):
        # Регистрация всех обработчиков кнопок из секции "Прочее"
        self.dp.callback_query.register(self.misc.misc_notifications, lambda c: c.data == "misc_notifications")
        self.dp.callback_query.register(self.misc.misc_settings, lambda c: c.data == "misc_settings")
        self.dp.callback_query.register(self.misc.misc_task_filter, lambda c: c.data == "misc_task_filter")
        self.dp.callback_query.register(self.misc.misc_task_sorting, lambda c: c.data == "misc_task_sorting")
        self.dp.callback_query.register(self.misc.misc_profile, lambda c: c.data == "misc_profile")

    def register_misc_task_sorting_keyboard(self):
        from src.api import setup
        setup.misc_task_sorting_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=btn[0], callback_data=btn[1])]
                for btn in setup.misc_task_sorting_buttons
            ]
        )

    def register_misc_task_filter_keyboard(self):
        from src.api import setup
        setup.misc_task_filter_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=btn[0], callback_data=btn[1])]
                for btn in setup.misc_task_filter_buttons
            ]
        )

    def register_misc_settings_buttons(self):
        from src.api import setup  # если нужно
        settings = setup.settings  # или откуда ты берёшь текущие настройки

        # Функция для создания текста кнопки для включения/выключения с красивым вводом
        def toggle_button(setting, on_text="Включить", off_text="Выключить"):
            if settings.get(setting):
                return f"❌ {off_text}"  # Если включено, значит можно выключить
            else:
                return f"✅ {on_text}"  # Если выключено, значит можно включить

        # Кнопки для настроек с красивыми надписями и эмодзи
        setup.misc_settings_buttons = [
            [toggle_button('notifications', 'Включить уведомления', 'Выключить уведомления'), "notifications"],
            [f"⏰ Установить формат времени ({'24ч' if settings['time_format'] == 24 else '12ч'})", "set_time_format"],
            [f"🗑 Автоудаление завершённых задач ({settings['auto_delete']} дней)", "set_auto_delete"],
            [toggle_button('ai', 'Включить искусственный интеллект', 'Выключить искусственный интеллект'), "set_ai"],
            ["🌐 *Смена языка*", "set_language"]
        ]

    def register_misc_settings_keyboard(self):
        from src.api import setup
        setup.misc_settings_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=btn[0], callback_data=btn[1])]
                for btn in setup.misc_settings_buttons
            ]
        )

    def register_misc_notifications_keyboard(self):
        from src.api import setup
        setup.notifications_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=notif[0], callback_data=f"delete_notification:{i}")]
                for i, notif in enumerate(setup.notifications_button)
            ]
        )

    def register_misc_task_sorting_keyboard_callback(self):
        """Регистрация обработчиков для сортировки задач"""
        self.dp.callback_query.register(self.sort.sort_date_asc, lambda c: c.data == "sort_date_asc")
        self.dp.callback_query.register(self.sort.sort_date_desc, lambda c: c.data == "sort_date_desc")
        self.dp.callback_query.register(self.sort.sort_priority, lambda c: c.data == "sort_priority")
        self.dp.callback_query.register(self.sort.sort_alphabetically, lambda c: c.data == "sort_alphabetically")
        self.dp.callback_query.register(self.sort.sort_reset, lambda c: c.data == "sort_reset")

    def register_misc_task_filter_keyboard_callback(self):
        self.dp.callback_query.register(self.filter.get_active_tasks, lambda c: c.data == "filter_active")
        self.dp.callback_query.register(self.filter.get_completed_tasks, lambda c: c.data == "filter_completed")
        self.dp.callback_query.register(self.filter.get_overdue_tasks, lambda c: c.data == "filter_overdue")
        self.dp.callback_query.register(self.filter.get_high_priority_tasks, lambda c: c.data == "filter_high_priority")
        self.dp.callback_query.register(self.filter.get_today_tasks, lambda c: c.data == "filter_today")

    def register_misc_settings_keyboard_callback(self):
        """Регистрация обработчиков для настроек"""
        self.dp.callback_query.register(self.settings.disable_notifications, lambda c: c.data == "notifications")
        self.dp.callback_query.register(self.settings.set_time_format, lambda c: c.data == "set_time_format")
        self.dp.callback_query.register(self.settings.set_auto_delete, lambda c: c.data == "set_auto_delete")
        self.dp.callback_query.register(self.settings.set_ai, lambda c: c.data == "set_ai")
        self.dp.callback_query.register(self.settings.set_language, lambda c: c.data == "set_language")

    def register_misc_notifications_keyboard_callback(self):
        self.dp.callback_query.register(
            self.notification.delete_notification,
            lambda c: c.data.startswith("delete_notification:")
        )

    def register_all(self):
        """Регистрирует все команды, кнопки и обработчики FSM."""
        self.register_misc_settings_buttons()
        self.register_misc_keyboard()
        self.register_misc_keyboard_callback()
        self.register_misc_task_sorting_keyboard()
        self.register_misc_task_filter_keyboard()
        self.register_misc_settings_keyboard()
        self.register_misc_notifications_keyboard()
        self.register_misc_task_sorting_keyboard_callback()
        self.register_misc_task_filter_keyboard_callback()
        self.register_misc_settings_keyboard_callback()
        self.register_misc_notifications_keyboard_callback()