from aiogram.filters import Command
from aiogram import Dispatcher, F, Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext


from src.api.settings import commands
from src.api.UserInputHandler import UserInputHandler

class Register:
    def __init__(self, dp: Dispatcher, router: Router, handler, button_handler, button_edit_task_handler):
        self.dp = dp
        self.handler = handler
        self.button_handler = button_handler
        self.router = router
        self.button_edit_task_handler = button_edit_task_handler

    def register_commands(self):
        """Регистрирует команды бота."""
        for command in commands:
            method = getattr(self.handler, f"{command}_command", None)
            if method:
                self.dp.message.register(method, Command(command))

    def register_navigation(self):
        """Регистрируем кнопки внизу."""
        self.dp.message.register(self.button_handler.list_tasks, F.text == "📋 Список задач")
        self.dp.message.register(self.button_handler.add_task, F.text == "➕ Добавить задачу")
        self.dp.message.register(self.button_handler.settings, F.text == "⚙ Настройки")

    def register_fsm_handler(self):
        """Регистрирует обработчики пользовательского ввода."""
        self.dp.message.register(self.handle_user_input_task, UserInputHandler.waiting_for_input)
        self.dp.message.register(self.handle_user_input_task_edit, UserInputHandler.waiting_for_edit)

    def register_task(self):
        from src.api import settings
        settings.task_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=task[0], callback_data=f"task:{index}")]
                for index, task in enumerate(settings.task_buttons)
            ]
        )

    def register_task_callbacks(self):
        """Регистрируем обработчик нажатий на задачи."""
        self.dp.callback_query.register(self.button_handler.task_selected, lambda c: c.data.startswith("task:"))

    def register_task_edit(self):
        """Регистрируем обработчик редактирования"""
        from src.api import settings

        print("Регистрируем обработчик редактирования")  # Проверяем, вызывается ли метод

        settings.task_edit_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=btn[0], callback_data=btn[1] if len(btn) > 1 else btn[0])]
                for btn in settings.task_edit_buttons
            ]
        )

        print("Клавиатура редактирования создана:", settings.task_edit_buttons)  # Проверяем кнопки

    def register_task_edit_callbacks(self):
        # Регистрация обработчика на кнопки вида edit_task:{index}
        self.dp.callback_query.register(self.button_edit_task_handler.edit_task_selected,
                                        lambda c: c.data.startswith("edit_task:"))

        print("Обработчик edit_task_selected зарегистрирован!")  # Проверяем, дошли ли до регистрации

    async def handle_user_input_task(self, message: Message, state: FSMContext):
        """Обрабатывает ввод пользователя и добавляет задачу."""
        from src.api import settings

        current_state = await state.get_state()

        if not current_state:
            await message.answer("⚠ Ошибка: FSM-состояние потеряно!")
            return

        user_input = message.text  # Получаем текст сообщения

        if not user_input:
            await message.answer("⚠ Пожалуйста, введите задачу!")
            return

        settings.task_buttons.append([user_input])  # Добавляем задачу
        self.register_task()

        await message.answer(f"✅ Задача добавлена: {user_input}")

        await state.clear()  # Очищаем состояние

    async def handle_user_input_task_edit(self, message: Message, state: FSMContext, callback_query: CallbackQuery):
        """Обрабатывает ввод пользователя и изменяет существующую задачу."""
        from src.api import settings

        # Проверяем текущее состояние
        current_state = await state.get_state()
        if not current_state:
            await message.answer("⚠ Ошибка: FSM-состояние потеряно!")
            return

        # Получаем индекс редактируемой задачи
        user_data = await state.get_data()
        task_index = user_data.get("editing_task_index")

        if task_index is None:
            await message.answer("⚠ Ошибка: индекс задачи не найден. Попробуйте заново.")
            return

        user_input = message.text.strip()  # Получаем текст нового названия задачи

        if not user_input:
            await message.answer("⚠ Пожалуйста, введите текст для изменения задачи!")
            return

        # Обновляем задачу в списке
        settings.task_buttons[task_index] = [user_input]

        # Пересоздаём клавиатуру с задачами
        self.register_task()

        await message.answer(f"✅ Задача обновлена: {user_input}")

        # Очищаем состояние после изменения
        await state.clear()

    def register_all(self):
        """Регистрирует все команды, кнопки и обработчики FSM."""
        print("Вызов register_all()")
        self.register_commands()
        self.register_navigation()
        self.register_fsm_handler()
        self.register_task_callbacks()
        self.register_task()
        self.register_task_edit()
        self.register_task_edit_callbacks()

