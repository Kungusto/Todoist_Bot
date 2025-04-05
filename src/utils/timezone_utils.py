from datetime import tzinfo
from typing import Any
from datetime import datetime

from src.utils.init_dbmanager import get_db

async def get_user_timezone() -> tzinfo | None | Any:
    """Определяет часовой пояс текущего пользователя, если не найден – использует серверное время."""
    from src.api.setup import user_id

    if not user_id:
        raise ValueError("User ID не установлен. Установите текущего пользователя.")

    async for db in get_db():
        user_data = await db.users.get_filtered(tg_id=user_id)
        if user_data and "timezone" in user_data:
            return user_data["timezone"]

    from datetime import datetime
    return datetime.now().astimezone().tzinfo

def get_format_deadline(deadline: datetime) -> str:
    """Форматирует дедлайн в соответствии с настройками времени."""
    from src.api.setup import settings
    time_format = settings["time_format"]

    if time_format == 24:
        return deadline.strftime("%Y-%m-%d %H:%M:%S")  # 24-часовой формат
    elif time_format == 12:
        return deadline.strftime("%Y-%m-%d %I:%M:%S %p")  # 12-часовой формат (AM/PM)
    else:
        return deadline.strftime("%Y-%m-%d %H:%M:%S")  # По умолчанию 24-часовой формат
