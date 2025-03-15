from datetime import datetime
from aiogram.types import CallbackQuery

from src.api.handlers import ButtonNavHandler
from src.api.register import Register


class Misc:
    async def misc_notifications(self, callback: CallbackQuery):
        from src.api import setup
        await callback.message.answer("*Уведомления*\n", reply_markup=setup.misc_notifications_keyboard, parse_mode="MarkdownV2")
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
        self.nav_handler = nav_handler  # Передаём объект
        self.register = register

    async def sort_date_asc(self, callback: CallbackQuery):
        from src.api import setup
        setup.task_buttons.sort(key=lambda x: datetime.strptime(x[4], "%Y-%m-%d"))
        await callback.message.answer("✅ Задачи отсортированы по дате (по возрастанию)")
        self.register.register_all()
        await self.nav_handler.list_tasks(callback.message)
        await callback.answer()  # Закрываем кнопку

    async def sort_date_desc(self, callback: CallbackQuery):
        from src.api import setup
        setup.task_buttons.sort(key=lambda x: datetime.strptime(x[4], "%Y-%m-%d"), reverse=True)
        await callback.message.answer("✅ Задачи отсортированы по дате (по убыванию)")
        self.register.register_all()
        await self.nav_handler.list_tasks(callback.message)
        await callback.answer()

    async def sort_priority(self, callback: CallbackQuery):
        from src.api import setup
        setup.task_buttons.sort(key=lambda x: x[2])
        await callback.message.answer("✅ Задачи отсортированы по приоритету")
        self.register.register_all()
        await self.nav_handler.list_tasks(callback.message)
        await callback.answer()

    async def sort_alphabetically(self, callback: CallbackQuery):
        from src.api import setup
        setup.task_buttons.sort(key=lambda x: x[0].lower())
        await callback.message.answer("✅ Задачи отсортированы по алфавиту")
        self.register.register_all()
        await self.nav_handler.list_tasks(callback.message)
        await callback.answer()

    async def sort_reset(self, callback: CallbackQuery):
        from src.api import setup
        setup.task_buttons = setup.task_buttons.copy()
        await callback.message.answer("✅ Сортировка сброшена, восстановлен исходный порядок")
        self.register.register_all()
        await self.nav_handler.list_tasks(callback.message)
        await callback.answer()


