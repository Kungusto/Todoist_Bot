from aiogram.filters import Command
from aiogram import Dispatcher, F, Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from src.api import settings
from src.api.settings import commands
from src.api.UserInputHandler import UserInputHandler

class Register:
    def __init__(self, dp: Dispatcher, router: Router, handler, button_handler):
        self.dp = dp
        self.handler = handler
        self.button_handler = button_handler
        self.router = router

    def register_commands(self):
        """Регистрирует команды бота."""
        for command in commands:
            method = getattr(self.handler, f"{command}_command", None)
            if method:
                self.dp.message.register(method, Command(command))
                print(f"Команда {command} зарегистрирована.")

    def register_navigation(self):
        """Регистрируем кнопки внизу."""
        self.dp.message.register(self.button_handler.list_tasks, F.text == "📋 Список задач")
        self.dp.message.register(self.button_handler.add_task, F.text == "➕ Добавить задачу")
        self.dp.message.register(self.button_handler.settings, F.text == "⚙ Настройки")

    def register_fsm_handler(self):
        """Регистрирует обработчик пользовательского ввода."""  # Изменено на dp
        self.dp.message.register(self.handle_user_input, UserInputHandler.waiting_for_input)
        print(f"⚡ Регистрируем FSM-хэндлер для {UserInputHandler.waiting_for_input}")

    async def handle_user_input(self, message: Message, state: FSMContext):
        """Обрабатывает ввод пользователя и добавляет задачу."""
        print(f"📩 Входящее сообщение: {message.text}")  # Логируем текст сообщения

        current_state = await state.get_state()
        print(f"📌 Текущее состояние FSM: {current_state}")  # Логируем состояние FSM

        if not current_state:
            await message.answer("⚠ Ошибка: FSM-состояние потеряно!")
            return

        user_input = message.text  # Получаем текст сообщения

        if not user_input:
            await message.answer("⚠ Пожалуйста, введите задачу!")
            return

        print("Получено сообщение")

        settings.task_buttons.append([user_input])  # Добавляем задачу
        settings.task_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=task[0], callback_data=task[0])] for task in settings.task_buttons]
        )
        await message.answer(f"✅ Задача добавлена: {user_input}")

        await state.clear()  # Очищаем состояние

    def register_all(self):
        """Регистрирует все команды, кнопки и обработчики FSM."""
        self.register_commands()
        self.register_navigation()
        self.register_fsm_handler()

