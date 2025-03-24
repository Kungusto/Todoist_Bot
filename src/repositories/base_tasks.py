from datetime import datetime, timedelta

from sqlalchemy import select
from src.repositories.base import BaseRepository
from src.models.tasks_first_step import TasksFirstStepOrm
from src.schemas.tasks_first_step import TaskStepOne

class BaseTasksRepository(BaseRepository) : 
    async def get_tasks_x_to_complete(self, before_completing_the_task: timedelta) : 
        query = (
            select(TasksFirstStepOrm)
        )
        model = await self.session.execute(query)
        first_tasks = [TaskStepOne.model_validate(task) for task in model.scalars().all()]
        print(first_tasks)