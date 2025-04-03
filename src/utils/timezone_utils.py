from datetime import tzinfo
from typing import Any

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
