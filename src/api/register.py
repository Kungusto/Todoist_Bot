from aiogram import Dispatcher, Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from src.api.setup import commands
from src.api.userInputHandler import UserInputHandler
from src.api.data import set_task
from src.api.data import *
from src.api.ai import AI

global main_dp, main_handler, main_button_handler, main_router, main_button_edit_task_handler, main_auth, tasks

class Register:
    def __init__(self, dp: Dispatcher = None, router: Router = None, handler=None, button_handler=None,
                 button_edit_task_handler=None, auth=None):
        # Объявляем глобальные переменные здесь
        global main_dp, main_handler, main_button_handler, main_router, main_button_edit_task_handler, main_auth

        if dp is None:
            self.dp = main_dp
            self.router = main_router
            self.handler = main_handler
            self.button_handler = main_button_handler
            self.button_edit_task_handler = main_button_edit_task_handler
            self.auth = main_auth
        else:
            # Инициализируем переданными параметрами, если они есть
            self.dp = dp
            self.router = router
            self.handler = handler
            self.button_handler = button_handler
            self.button_edit_task_handler = button_edit_task_handler
            self.auth = auth

            # Обновляем глобальные переменные
            main_dp = self.dp
            main_router = self.router
            main_handler = self.handler
            main_button_handler = self.button_handler
            main_button_edit_task_handler = self.button_edit_task_handler
            main_auth = self.auth


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
        self.dp.message.register(self.auth.process_enter, UserInputHandler.waiting_for_enter)
        self.dp.message.register(self.auth.process_enter_password, UserInputHandler.waiting_for_enter_password)
        self.dp.message.register(self.auth.process_enter_code, UserInputHandler.waiting_for_code)
        self.dp.message.register(self.auth.process_register, UserInputHandler.waiting_for_reg)
        self.dp.message.register(self.auth.process_register_password, UserInputHandler.waiting_for_reg_password)

        self.dp.message.register(self.handle_user_input_task, UserInputHandler.waiting_for_input)
        self.dp.message.register(self.handle_user_input_task_edit, UserInputHandler.waiting_for_edit)
        self.dp.message.register(self.handle_user_input_subtask, UserInputHandler.waiting_for_subtask)
        self.dp.message.register(self.handle_user_input_deadline, UserInputHandler.waiting_for_deadline)

    def register_task(self, task_buttons=None):
        from src.api import setup
        global tasks

        if task_buttons is None:
            task_buttons = tasks
        elif task_buttons == "all":
            task_buttons = setup.task_buttons
            tasks = setup.task_keyboard

        # Используем оригинальные индексы задач из setup.task_buttons
        task_indices = [setup.task_buttons.index(task) for task in task_buttons if task in setup.task_buttons]

        setup.task_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=setup.task_buttons[i][0], callback_data=f"task:{i}")]
                for i in task_indices
            ]
        )

    def register_task_priority(self):
        from src.api import setup

        setup.task_priority_edit_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=btn[0], callback_data=btn[1] if len(btn) > 1 else btn[0])]
                for btn in setup.task_priority_edit_buttons
            ]
        )

    def register_auth(self):
        from src.api import setup
        setup.auth_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=btn[0], callback_data=btn[1])]
                for btn in setup.auth_button
            ]
        )

    def register_auth_callbacks(self):
        self.dp.callback_query.register(self.auth.enter, lambda c: c.data.startswith("enter"))
        self.dp.callback_query.register(self.auth.register, lambda c: c.data.startswith("register"))

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

    def register_task_status(self):
        from src.api import setup
        setup.task_status_edit_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=btn[0], callback_data=btn[1] if len(btn) > 1 else btn[0])]
                for btn in setup.task_status_edit_buttons
            ]
        )

    def register_task_edit_callbacks(self):
        # Регистрация обработчика на кнопки вида edit_task:{index}
        self.dp.callback_query.register(self.button_edit_task_handler.edit_task_selected,
                                        lambda c: c.data.startswith("edit_task:"))

    def register_subtask_callbacks(self):
        # Регистрация обработчика на кнопки вида add_subtasks:{index}
        self.dp.callback_query.register(self.button_edit_task_handler.subtask_selected,
                                        lambda c: c.data.startswith("add_subtasks:"))

    def register_task_priority_callbacks(self):
        self.dp.callback_query.register(self.button_edit_task_handler.priority_selected,
                                        lambda c: c.data.startswith("change_priority:"))
        self.dp.callback_query.register(self.button_edit_task_handler.priority_selected,
                                        lambda c: c.data.startswith("Low"))
        self.dp.callback_query.register(self.button_edit_task_handler.priority_selected,
                                        lambda c: c.data.startswith("Medium"))
        self.dp.callback_query.register(self.button_edit_task_handler.priority_selected,
                                        lambda c: c.data.startswith("High"))

    def register_task_deadline_callbacks(self):
        self.dp.callback_query.register(self.button_edit_task_handler.deadline_selected,
                                        lambda c: c.data.startswith("change_deadline:"))

    def register_task_status_callbacks(self):
        self.dp.callback_query.register(self.button_edit_task_handler.status_selected,
                                        lambda c: c.data.startswith("change_status:"))
        self.dp.callback_query.register(self.button_edit_task_handler.status_selected,
                                        lambda c: c.data.startswith("New"))
        self.dp.callback_query.register(self.button_edit_task_handler.status_selected,
                                        lambda c: c.data.startswith("In_Progress"))
        self.dp.callback_query.register(self.button_edit_task_handler.status_selected,
                                        lambda c: c.data.startswith("On_Hold"))
        self.dp.callback_query.register(self.button_edit_task_handler.status_selected,
                                        lambda c: c.data.startswith("Completed"))

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
        if setup.settings["ai"]:
            ai = AI(user_input)
            ok = await ai.get_task()
            if not ok: await message.answer("Ошибка добавления задачи. Попробуйте снова.")
        else: setup.task_buttons.append([user_input, None, None, None, None])

        self.register_all()
        await message.answer(f"✅ Задача добавлена: {user_input}")
        await set_task()
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

        setup.task_buttons[task_index][0] = user_input
        self.register_task("all")
        await message.answer(f"✅ Задача обновлена: {user_input}")
        await set_task()
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
        self.register_task("all")
        print(f"ПОдзадача: {setup.task_buttons}")
        await message.answer(f"✅ Подзадача добавлена: {subtask_text}")
        await set_task()
        await state.clear()

    async def handle_user_input_deadline(self, message: Message, state: FSMContext):
        """Обрабатывает ввод пользователя и добавляет дедлайн."""
        from src.api import setup
        from src.api.ai import AI
        from src.utils.timezone_utils import get_format_deadline
        print("handle_user_input_deadline")
        user_data = await state.get_data()
        task_index = user_data.get("deadline_index")
        if task_index is None:
            await message.answer("⚠ Ошибка: индекс задачи не найден. Попробуйте заново.")
            return

        deadline_text = message.text.strip()
        if not deadline_text:
            await message.answer("⚠ Пожалуйста, введите дедлайн!")
            return

        ai = AI(deadline_text)
        deadline_text = await ai.get_data()

        if deadline_text is None:
            await message.answer("⚠ Пожалуйста, введите корректную дату выполнения задачи!")
            return

        if isinstance(deadline_text, datetime):
            # Форматируем дедлайн в соответствии с настройками времени
            deadline_text = get_format_deadline(deadline_text)
        else:
            # Если это не datetime, просто приводим к строке
            deadline_text = str(deadline_text)

            # Обновляем дедлайн задачи
        setup.task_buttons[task_index][4] = deadline_text

        self.register_task("all")
        print(setup.task_buttons)
        deadline_text = deadline_text.replace("\\-", "-")
        await message.answer(f"✅ Дедлайн добавлен: {deadline_text}")
        await set_task()
        await state.clear()

    def register_all(self):
        """Регистрирует все команды, кнопки и обработчики FSM."""
        print("Вызов register_all()")
        self.register_commands()
        self.register_navigation()
        self.register_fsm_handler()
        self.register_task("all")
        self.register_task_callbacks()
        self.register_task_edit()
        self.register_task_edit_callbacks()
        self.register_subtask_callbacks()
        self.register_task_priority_callbacks()
        self.register_task_deadline_callbacks()
        self.register_auth()
        self.register_auth_callbacks()
        self.register_task_status()
        self.register_task_status_callbacks()
        self.register_task_priority()
        self.register_task_priority_callbacks()