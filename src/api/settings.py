from src.api.handlers import CommandHandler
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


token = "8090759361:AAGkfIL43EeWm5NJ7CZt3I8C-ReUZktRH_U"


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
#тут будет получение всех задач

task_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text=task[0], callback_data=task[0])] for task in task_buttons]
)

task_edit_buttons = [
    ["Изменить"],
    ["Добавить описание"],
    ["Добавить подзадачи"],
    ["Изменить приоритет"],
    ["Изменить статус"],
    ["Изменить время выполнения"],
]

task_edit_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text=task_edit[0], callback_data=task_edit[0])] for task_edit in task_edit_buttons]
)

#subtask_keyboard[task_keyboard.long] как-нибудь потом