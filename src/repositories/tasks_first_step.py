from src.repositories.base import BaseRepository
from src.models.tasks_first_step import TasksFirstStepOrm
from src.schemas.tasks_first_step import TaskStepOne

class TasksStepOneRepository(BaseRepository) : 
    model = TasksFirstStepOrm
    schema = TaskStepOne
