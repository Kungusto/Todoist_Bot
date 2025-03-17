from src.repositories.base import BaseRepository
from src.models.tasks_second_step import TasksFirstStepORM
from src.schemas.tasks_second_step import TaskStepTwo

class TasksStepTwoRepository(BaseRepository) :
    model = TasksFirstStepORM
    schema = TaskStepTwo