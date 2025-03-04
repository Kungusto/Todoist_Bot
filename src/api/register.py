from aiogram import Dispatcher, Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext


from src.api.setup import commands
from src.api.userInputHandler import UserInputHandler

class Register:
    def __init__(self, dp: Dispatcher, router: Router, handler, button_handler, button_edit_task_handler):
        self.dp = dp
        self.handler = handler
        self.button_handler = button_handler
        self.router = router
        self.button_edit_task_handler = button_edit_task_handler

    def register_commands(self):
        """Регистрирует команды бота."""
        from aiogram.filters import Command
        for command in commands:
            method = getattr(self.handler, f"{command}_command", None)
            if method:
                self.dp.message.register(method, Command(command))

    def register_navigation(self):
        """Регистрируем кнопки внизу."""
        from aiogram import F
        self.dp.message.register(self.button_handler.list_tasks, F.text == "📋 Список задач")
        self.dp.message.register(self.button_handler.add_task, F.text == "➕ Добавить задачу")
        self.dp.message.register(self.button_handler.settings, F.text == "⚙ Настройки")

    def register_fsm_handler(self):
        """Регистрирует обработчики пользовательского ввода."""
        self.dp.message.register(self.handle_user_input_task, UserInputHandler.waiting_for_input)
        self.dp.message.register(self.handle_user_input_task_edit, UserInputHandler.waiting_for_edit)
        self.dp.message.register(self.handle_user_input_subtask, UserInputHandler.waiting_for_subtask)

    def register_task(self):
        from src.api import setup
        setup.task_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=task[0], callback_data=f"task:{index}")]
                for index, task in enumerate(setup.task_buttons)
            ]
        )

    def register_task_callbacks(self):
        """Регистрируем обработчик нажатий на задачи."""
        self.dp.callback_query.register(self.button_handler.task_selected, lambda c: c.data.startswith("task:"))

    def register_task_edit(self):
        """Регистрируем обработчик редактирования."""
        from src.api import setup

        print("Регистрируем обработчик редактирования")  # Проверяем, вызывается ли метод

        setup.task_edit_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=btn[0], callback_data=btn[1])]
                for btn in setup.task_edit_buttons
            ]
        )

        print("Клавиатура редактирования создана:", setup.task_edit_buttons)

    def register_task_edit_callbacks(self):
        # Регистрация обработчика на кнопки вида edit_task:{index}
        self.dp.callback_query.register(self.button_edit_task_handler.edit_task_selected,
                                        lambda c: c.data.startswith("edit_task:"))
        print("Обработчик edit_task_selected зарегистрирован!")

    def register_subtask_callbacks(self):
        # Регистрация обработчика на кнопки вида add_subtasks:{index}
        self.dp.callback_query.register(self.button_edit_task_handler.subtask_selected,
                                        lambda c: c.data.startswith("add_subtasks:"))
        print("Обработчик add_subtasks_selected зарегистрирован!")

    def register_task_priority_callbacks(self):
        self.dp.callback_query.register(self.button_edit_task_handler.priority_selected,
                                        lambda c: c.data.startswith("change_priority:"))
        self.dp.callback_query.register(self.button_edit_task_handler.priority_selected,
                                        lambda c: c.data.startswith("Low"))
        self.dp.callback_query.register(self.button_edit_task_handler.priority_selected,
                                        lambda c: c.data.startswith("Medium"))
        self.dp.callback_query.register(self.button_edit_task_handler.priority_selected,
                                        lambda c: c.data.startswith("High"))

    async def handle_user_input_task(self, message: Message, state: FSMContext):
        """Обрабатывает ввод пользователя и добавляет задачу."""
        from src.api import setup

        current_state = await state.get_state()
        if not current_state:
            await message.answer("⚠ Ошибка: FSM-состояние потеряно!")
            return

        user_input = message.text
        if not user_input:
            await message.answer("⚠ Пожалуйста, введите задачу!")
            return

        setup.task_buttons.append([user_input])

        self.register_task()
        await message.answer(f"✅ Задача добавлена: {user_input}")
        await state.clear()

    async def handle_user_input_task_edit(self, message: Message, state: FSMContext):
        """Обрабатывает ввод пользователя и изменяет существующую задачу."""
        from src.api import setup

        current_state = await state.get_state()
        if not current_state:
            await message.answer("⚠ Ошибка: FSM-состояние потеряно!")
            return

        user_data = await state.get_data()
        task_index = user_data.get("editing_task_index")
        if task_index is None:
            await message.answer("⚠ Ошибка: индекс задачи не найден. Попробуйте заново.")
            return

        user_input = message.text.strip()
        if not user_input:
            await message.answer("⚠ Пожалуйста, введите текст для изменения задачи!")
            return

        setup.task_buttons[task_index] = [user_input]
        self.register_task()
        await message.answer(f"✅ Задача обновлена: {user_input}")
        await state.clear()

    async def handle_user_input_subtask(self, message: Message, state: FSMContext):
        """Обрабатывает ввод пользователя и добавляет подзадачу."""
        from src.api import setup

        user_data = await state.get_data()
        task_index = user_data.get("subtask_index")
        if task_index is None:
            await message.answer("⚠ Ошибка: индекс задачи не найден. Попробуйте заново.")
            return

        subtask_text = message.text.strip()
        if not subtask_text:
            await message.answer("⚠ Пожалуйста, введите текст для подзадачи!")
            return

        # Если для задачи ещё не создан список подзадач, создаём его
        if len(setup.task_buttons[task_index]) == 1:
            setup.task_buttons[task_index].append([])

        setup.task_buttons[task_index][1].append(subtask_text)
        self.register_task()
        await message.answer(f"✅ Подзадача добавлена: {subtask_text}")
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
        self.register_subtask_callbacks()
        self.register_task_priority_callbacks()