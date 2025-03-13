from aiogram.types import CallbackQuery

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
