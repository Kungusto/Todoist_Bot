from sqlalchemy import select

from src.repositories.base_tasks import BaseTasksRepository
from src.models.tasks_first_step import TasksFirstStepOrm
from src.schemas.tasks_first_step import TaskStepOne

class TasksStepOneRepository(BaseTasksRepository) : 
    model = TasksFirstStepOrm
    schema = TaskStepOne

    async def get_today_due_tasks(self, user_id: int) :
        '''получить задачи, срок которых истекает сегодня'''
        query = (
            select(self.model)
            .filter_by(user_id=user_id)
            .filter(self.model.complation_due)
        )

        result = await self.session.execute(query)
        return result
    
    async def get_user_tasks(self, user_id: int) :
        query = (
            select(self.model)
            .filter_by(user_id=user_id)
        )

        result = await self.session.execute(query)
        return result