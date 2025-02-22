from aiogram.filters import Command
from aiogram import Dispatcher, F
import logging
from api.settings import commands  

class Register:
    def __init__(self, dp: Dispatcher, handler, button_handler):
        self.dp = dp
        self.handler = handler
        self.button_handler = button_handler  # Добавляем обработчик кнопок

    def register_commands(self):
        """Регистрирует команды бота."""
        for command in commands:
            method = getattr(self.handler, f"{command}_command", None)
            if method:
                self.dp.message.register(method, Command(command))
    def register_navigation(self):
        """Регистрируем кнопки внизу"""
        self.dp.message.register(self.button_handler.list_tasks, F.text == "📋 Список задач")
        self.dp.message.register(self.button_handler.add_task, F.text == "➕ Добавить задачу")
        self.dp.message.register(self.button_handler.settings, F.text == "⚙ Настройки")

    def register_all(self):
        """Регистрирует все команды и кнопки."""
        self.register_commands()
        self.register_navigation()
        