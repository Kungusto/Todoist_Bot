from api.Handlers import CommandHandler
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


nav_buttons = [
    ["📋 Список задач"],  # Одна кнопка в строке
    ["➕ Добавить задачу", "⚙ Настройки"],  # Две кнопки в строке
]

nav_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=btn) for btn in row] for row in nav_buttons],
    resize_keyboard=True  # Подгоняет размер под экран
)

buttons = [
    func[:-8] for func in dir(CommandHandler)  
    if callable(getattr(CommandHandler, func)) and func.endswith("_command")
]

commands = [
    func[:-8] for func in dir(CommandHandler)  
    if callable(getattr(CommandHandler, func)) and func.endswith("_command")
]

token = "8090759361:AAGkfIL43EeWm5NJ7CZt3I8C-ReUZktRH_U"
