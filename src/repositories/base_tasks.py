from datetime import datetime
from src.repositories.base import BaseRepository


class BaseTasksRepository(BaseRepository) : 
    async def get_tasks_x_to_complete(self, before_completing_the_task: datetime) : 
        ...