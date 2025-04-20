from src.models.tasks_second_step import TasksSecondStepORM
from src.schemas.tasks_second_step import TaskStepTwo
from src.repositories.base_tasks import BaseTasksRepository

class TasksStepTwoRepository(BaseTasksRepository) :
    model = TasksSecondStepORM
    schema = TaskStepTwo