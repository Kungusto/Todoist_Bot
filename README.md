# Todoist Bot

## Описание
Telegram-бот для управления задачами, аналогичный Todoist. Позволяет создавать, редактировать, удалять и управлять задачами через удобные кнопки в чате Telegram.

## Функционал
- Создание задач
- Удаление задач
- Редактирование задач
- Добавление подзадач
- Отметка выполнения задач
- Интерактивные кнопки для удобной навигации

## Технологии
- Python
- Aiogram (Telegram Bot API)
- PostgreSQL (База данных)
- Pydantic (Валидация данных)
- Pydantic-settings (Загрузка переменных окружения)

## Установка
### 1. Клонирование репозитория
```bash
git clone git@github.com:Kungusto/Todoist_Bot.git
cd Todoist_Bot
```

### 2. Создание виртуального окружения и установка зависимостей
```bash
python -m venv .venv
source .venv/bin/activate  # Для Linux/Mac
.venv\Scripts\activate    # Для Windows
pip install -r requirements.txt
```

### 3. Настройка переменных окружения
Создайте файл `.env` в корне проекта и добавьте в него:
```ini
DB_PORT=5432
DB_HOST=localhost
DB_PASS=yourpassword
DB_NAME=yourdbname
DB_USER=yourdbuser
TOKEN=your_bot_token
```
Замените `yourpassword`, `yourdbname`, `yourdbuser`, `your_bot_token` на реальные данные.

### 4. Запуск бота
```bash
python src/main.py
```

## Использование
После запуска бота введите `/start`, чтобы начать работу.

## Контакты
Авторы: [Kungusto](https://github.com/Kungusto) и [DeimosCreator](https://github.com/DeimosCreator).

