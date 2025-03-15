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
        from src.api import setup, data
        setup.task_buttons.sort(key=lambda x: datetime.strptime(x[4], "%Y-%m-%d-%M-%S"))
        await callback.message.answer("✅ Задачи отсортированы по дате (по возрастанию)")
        self.register.register_all()
        await self.nav_handler.list_tasks(callback.message)
        await data.set_task()
        await callback.answer()  # Закрываем кнопку

    async def sort_date_desc(self, callback: CallbackQuery):
        from src.api import setup, data
        setup.task_buttons.sort(key=lambda x: datetime.strptime(x[4], "%Y-%m-%d-%M-%S"), reverse=True)
        await callback.message.answer("✅ Задачи отсортированы по дате (по убыванию)")
        self.register.register_all()
        await self.nav_handler.list_tasks(callback.message)
        await data.set_task()
        await callback.answer()

    async def sort_priority(self, callback: CallbackQuery):
        from src.api import setup, data
        setup.task_buttons.sort(key=lambda x: x[2])
        await callback.message.answer("✅ Задачи отсортированы по приоритету")
        self.register.register_all()
        await self.nav_handler.list_tasks(callback.message)
        await data.set_task()
        await callback.answer()

    async def sort_alphabetically(self, callback: CallbackQuery):
        from src.api import setup, data
        setup.task_buttons.sort(key=lambda x: x[0].lower())
        await callback.message.answer("✅ Задачи отсортированы по алфавиту")
        self.register.register_all()
        await self.nav_handler.list_tasks(callback.message)
        await data.set_task()
        await callback.answer()

    async def sort_reset(self, callback: CallbackQuery):
        from src.api import setup, data
        setup.task_buttons = setup.task_buttons.copy()
        await callback.message.answer("✅ Сортировка сброшена, восстановлен исходный порядок")
        self.register.register_all()
        await self.nav_handler.list_tasks(callback.message)
        await data.set_task()
        await callback.answer()

class FilterTask:
    def __init__(self, nav_handler: ButtonNavHandler, register: Register):
        self.nav_handler = nav_handler
        self.register = register

    async def get_active_tasks(self, callback: CallbackQuery):
        """Фильтрует только активные (в процессе) задачи."""
        from src.api import setup
        tasks = [task for task in setup.task_buttons if task[3] == 1 or task[3] == 2]
        self.register.register_task(tasks)
        await callback.answer()

    async def get_completed_tasks(self, callback: CallbackQuery):
        """Фильтрует завершённые задачи."""
        from src.api import setup
        tasks = [task for task in setup.task_buttons if task[3] == 4]
        print(tasks)
        self.register.register_task(tasks)
        await callback.answer()

    async def get_overdue_tasks(self, callback: CallbackQuery):
        """Фильтрует просроченные задачи."""
        from src.api import setup
        from datetime import date
        today = date.today().strftime("%Y-%m-%d")
        tasks = [task for task in setup.task_buttons if task[4] < today]
        self.register.register_task(tasks)
        await callback.answer()

    async def get_high_priority_tasks(self, callback: CallbackQuery):
        """Фильтрует задачи с высоким приоритетом."""
        from src.api import setup
        tasks = [task for task in setup.task_buttons if task[2] == 3]
        self.register.register_task(tasks)
        await callback.answer()

    async def get_today_tasks(self, callback: CallbackQuery):
        """Фильтрует задачи, которые запланированы на сегодня."""
        from src.api import setup
        from datetime import date
        today = date.today().strftime("%Y-%m-%d")
        tasks = [task for task in setup.task_buttons if task[4] == today]
        self.register.register_task(tasks)
        await callback.answer()

    async def get_all_tasks(self, callback: CallbackQuery):
        """Убирает фильтрацию"""
        self.register.register_task("all")
        await callback.answer()


