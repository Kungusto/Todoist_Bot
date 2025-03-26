from src.database import async_session_maker
from src.repositories.base_tasks import BaseTasksRepository
from src.repositories.tasks_first_step import TasksStepOneRepository
from src.repositories.tasks_second_step import TasksStepTwoRepository
from src.repositories.users import UsersRepository
from src.repositories._settings import SettingsRepository

class DBManager : 
    def __init__(self, session_factory) :
        self.session_factory = session_factory
    
    async def __aenter__(self) :
        self.session = self.session_factory()
        
        self.tasks_frst_stp = TasksStepOneRepository(self.session)
        self.tasks_second_stp =  TasksStepTwoRepository(self.session)
        self.users = UsersRepository(self.session)
        self.tasks = BaseTasksRepository(self.session)
        self.settings = SettingsRepository(self.session)

        return self
    
    async def __aexit__(self, *args) : 
        await self.session.rollback()
        await self.session.close()
    
    async def commit(self) : 
        await self.session.commit()
