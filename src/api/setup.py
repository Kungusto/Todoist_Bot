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
#задачи их свойства
task_buttons = [
    ["кота", [], 1, 1, "2030-02-20"],
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
    ["1️⃣ Высокий (🔥 Срочно)", "High", "🔥 Срочно", 1],
    ["2️⃣ Средний (⏳ Обычный)", "Medium", "⏳ Обычный", 2],
    ["3️⃣ Низкий (✅ Можно подождать)", "Low", "✅ Можно подождать", 3],
]

task_priority_edit_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=btn[0], callback_data=btn[1] if len(btn) > 1 else btn[0])]
        for btn in task_priority_edit_buttons
    ]
)

task_status_edit_buttons = [
    ["Новая 📃", "New", 1],
    ["В процессе ⏳", "In_Progress", 2],
    ["Отложена 🔄", "On_Hold", 3],
    ["Завершена ✅", "Completed", 4],
]

task_status_edit_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=btn[0], callback_data=btn[1] if len(btn) > 1 else btn[0])]
        for btn in task_status_edit_buttons
    ]
)

settings_button = [
    ["Вход", "enter"],
    ["Регистрация", "reg"],
]

settings_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=btn[0], callback_data=btn[1] if len(btn) > 1 else btn[0])]
        for btn in settings_button
    ]
)



auth_button = [
    ["Вход", "enter"],
    ["Регистрация", "register"],
]

auth_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=btn[0], callback_data=btn[1] if len(btn) > 1 else btn[0])]
        for btn in auth_button
    ]
)

user_id = "14"
nickname = "Deimos"
password = "1s"
active_codes = {}  # Словарь для хранения кодов подтверждения


