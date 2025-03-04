from src.api.handlers import CommandHandler
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from src.utils.init_dbmanager import get_db

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
#задачи их свойства
task_buttons = [
    ["Полить кота", [], 1, 1, "2030-02-20"],
    ["Покормить кота", [], 2, 2, "2020-12-01"],
]

task_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=task[0], callback_data=f"task:{index}")]
            for index, task in enumerate(task_buttons)
        ]
)


task_edit_buttons = [
    ["➡ Редактировать 🔄", "edit_task:0"],
    ["➡ Добавить подзадачу ➕", "add_subtasks:0"],
    ["➡ Изменить приоритет 🔥", "change_priority:0"],
    ["➡ Изменить статус ✅", "change_status:0"],
    ["➡ Изменить дедлайн ⏳", "change_deadline:0"],
]

task_edit_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=btn[0], callback_data=btn[1] if len(btn) > 1 else btn[0])]
        for btn in task_edit_buttons
    ]
)

task_priority_edit_buttons = [
    ["1️⃣ Высокий (🔥 Срочно)", "High", "🔥 Срочно"],
    ["2️⃣ Средний (⏳ Обычный)", "Medium", "⏳ Обычный"],
    ["3️⃣ Низкий (✅ Можно подождать)", "Low", "✅ Можно подождать"],
]

task_priority_edit_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=btn[0], callback_data=btn[1] if len(btn) > 1 else btn[0])]
        for btn in task_priority_edit_buttons
    ]
)
