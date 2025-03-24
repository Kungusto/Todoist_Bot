from src.repositories.base import BaseRepository
from src.models.tasks_second_step import TasksSecondStepORM
from src.schemas.tasks_second_step import TaskStepTwo

class TasksStepTwoRepository(BaseRepository) :
    model = TasksSecondStepORM
    schema = TaskStepTwo