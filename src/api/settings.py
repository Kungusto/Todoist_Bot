import asyncio

from alembic.command import current

from src.api.handlers import CommandHandler
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


token = "8090759361:AAGkfIL43EeWm5NJ7CZt3I8C-ReUZktRH_U"

current_state = 0
'''
1 - это старт и хелп
2 - это все задачи
3 - конкретная задача
'''

nav_buttons = [
    ["📋 Список задач"],  # Одна кнопка в строке
    ["➕ Добавить задачу", "⚙ Настройки"],  # Две кнопки в строке
]

nav_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=btn) for btn in row] for row in nav_buttons],
    resize_keyboard=True  # Подгоняет размер под экран
)

commands = [
    func[:-8] for func in dir(CommandHandler)  
    if callable(getattr(CommandHandler, func)) and func.endswith("_command")
]

task_buttons = [
    ["Полить цветы"],
    ["Покормить кота"],
]

task_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=task[0], callback_data=f"task:{index}")]
            for index, task in enumerate(task_buttons)
        ]
)


task_edit_buttons = [
    ["✏ Изменить", "edit_task:0"],
    ["Добавить описание", "add_description:0"],
    ["Добавить подзадачи", "add_subtasks:0"],
    ["Изменить приоритет", "change_priority:0"],
    ["Изменить статус", "change_status:0"],
    ["Изменить время выполнения", "change_deadline:0"],
]

task_edit_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=btn[0], callback_data=btn[1] if len(btn) > 1 else btn[0])]
        for btn in task_edit_buttons
    ]
)

print("task_edit_buttons:", task_edit_buttons)



#subtask_keyboard[task_keyboard.long] как-нибудь потом

