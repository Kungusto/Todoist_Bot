from aiogram import Dispatcher, Router
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class Register:
    def __init__(self, dp: Dispatcher = None, router: Router = None, misc=None):
        self.dp = dp
        self.router = router
        self.misc = misc

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

    def register_all(self):
        """Регистрирует все команды, кнопки и обработчики FSM."""
        self.register_misc_keyboard()
        self.register_misc_keyboard_callback()
