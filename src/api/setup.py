from src.api.handlers import CommandHandler
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

current_state = 0

'''
1 - это старт и помощь
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
"""
0 - title (Название задачи)
1 - subtasks (Подзадачи, список)
2 - priority (Приоритет, где 1 - низкий, 2 - средний, 3 - высокий)
3 - status (Статус, где 1 - новая, 2 - в процессе, 3 - отложено, 4 - завершена)
4 - deadline (Крайний срок в формате YYYY-MM-DD)
"""
task_buttons = [
    # ["Полить цветы", [], 1, 1, "2030-02-20-00-00-00"],
    # ["Покормить кота", [], 2, 2, "2020-12-01-00-00-00"],
    # ["Закончить отчёт", ["Написать ввод", "Сделать расчёты"], 3, 1, "2025-03-25-00-00-00"],
    # ["Купить продукты", ["Молоко", "Хлеб", "Яйца"], 2, 1, "2025-03-18-00-00-00"],
    # ["Записаться к врачу", [], 3, 3, "2025-04-10-00-00-00"],
    # ["Позвонить маме", [], 1, 1, "2025-03-15-00-00-00"],
    # ["Подготовиться к экзамену", ["Прочитать главы 1-3", "Решить тесты"], 3, 1, "2025-05-10-00-00-00"],
    # ["Оплатить счета", [], 2, 1, "2025-03-28-00-00-00"],
    # ["Прочитать книгу", [], 1, 3, "2025-06-01-00-00-00"],
    # ["Сделать зарядку", [], 2, 1, "2025-05-14-00-00-00"],
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


# Кнопки для раздела "Прочее"
misc_buttons = [
    ["🔔 Уведомления", "misc_notifications"],
    ["🔢 Сортировка задач", "misc_task_sorting"],
    ["✅ Какие задачи показывать", "misc_task_filter"],
    ["⚙ Настройки", "misc_settings"],
    ["👤 Личный профиль", "misc_profile"],
]

misc_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=btn[0], callback_data=btn[1])]
        for btn in misc_buttons
    ]
)

# Кнопки для "Уведомлений"
misc_notifications_buttons = [
    ["📢 Показываю уведомления", "toggle_notifications"],
    ["🕒 Напоминания о задачах", "toggle_reminders"],
    ["⏳ Напоминать о просроченных задачах", "toggle_overdue"],
    ["🚀 Интервал напоминаний (3ч, 6ч, 12ч)", "set_notification_interval"],
]

misc_notifications_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=btn[0], callback_data=btn[1])]
        for btn in misc_notifications_buttons
    ]
)
settings = {
    "notifications": False,
    "time_format": 24,
    "auto_delete": 7,
    "ai": True,
    "task_sort": 4,
    "task_filter": 0,
    "language": "Russian"
}


notification_fun = "🔕 Отключить уведомления" if settings["notifications"] else "🔔 Включить уведомления"
# Кнопки для "Настроек"
misc_settings_buttons = [
    [notification_fun, "notifications"],
    ["⏰ Установить формат времени (24ч / 12ч)", "set_time_format"],
    ["🗑 Автоудаление завершённых задач (7/30 дней)", "set_auto_delete"],
    ["Искусственный интеллект", "set_ai"],
    ["🌐 Смена языка", "set_language"],
]

misc_settings_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=btn[0], callback_data=btn[1])]
        for btn in misc_settings_buttons
    ]
)

# Кнопки для фильтрации задач
misc_task_filter_buttons = [
    ["📌 Только активные", "filter_active"],
    ["❌ Показывать завершённые", "filter_completed"],
    ["🔴 Показывать просроченные", "filter_overdue"],
    ["⚠ Показывать с высоким приоритетом", "filter_high_priority"],
    ["📅 Показывать задачи на сегодня", "filter_today"],
    ["📝 Показывать все", "filter_all"],
]

misc_task_filter_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=btn[0], callback_data=btn[1])]
        for btn in misc_task_filter_buttons
    ]
)

# Кнопки для сортировки задач
misc_task_sorting_buttons = [
    ["🔼 По дате (раньше → позже)", "sort_date_asc"],
    ["🔽 По дате (позже → раньше)", "sort_date_desc"],
    ["⚡ По приоритету (высокий → низкий)", "sort_priority"],
    ["🔠 По алфавиту", "sort_alphabetically"],
    ["🔄 Сброс сортировки", "sort_reset"],
]

misc_task_sorting_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=btn[0], callback_data=btn[1])]
        for btn in misc_task_sorting_buttons
    ]
)

# Кнопки для "Личного профиля"
misc_profile_buttons = [
    ["✏ Изменить имя", "edit_name"],
    ["📦 Экспорт задач (JSON / TXT)", "export_tasks"],
    ["🔄 Сброс всех настроек", "reset_settings"],
    ["📊 Статистика по задачам", "task_statistics"],
]

misc_profile_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=btn[0], callback_data=btn[1])]
        for btn in misc_profile_buttons
    ]
)

notifications_button = []

notifications_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=notif[0], callback_data=f"task:{i}")]
        for i, notif in enumerate(notifications_button)
    ]
)

id = -1
user_id = -1
nickname = -1
password = -1
active_codes = {}  # Словарь для хранения кодов подтверждения