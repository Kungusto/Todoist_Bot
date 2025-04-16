from sqlalchemy import select, func

from src.repositories.base import BaseRepository
from src.models.users import UsersOrm
from src.models.tasks_first_step import TasksFirstStepOrm
from src.schemas.users import User
from src.schemas.users import AllInfoAboutUser

class UsersRepository(BaseRepository)  :
    model = UsersOrm
    schema = User

    async def get_tg_id_by_id(self, id):
        query = select(UsersOrm).filter_by(id=id)
        result = await self.session.execute(query)
        user = result.scalars().first()
        return user.tg_id if user else None

    async def get_id_by_tg_id(self, tg_id):
        query = select(UsersOrm).filter_by(tg_id=tg_id)
        result = await self.session.execute(query)
        user = result.scalars().first()
        return user.id if user else None
    
    async def all_info_about_user(self, id: int) : 
        query = (
            select(
            UsersOrm.id.label("user_id"),
            func.count("*").label("completed_tasks_count")
        )
        .join(TasksFirstStepOrm, TasksFirstStepOrm.user_id == UsersOrm.id)
        .filter(TasksFirstStepOrm.status == 4)
        .filter(UsersOrm.id == id)
        .group_by(UsersOrm.id)        
        )
        result = await self.session.execute(query)
        user_data = result.all()
        return AllInfoAboutUser(user_id=id, completed_tasks_count=user_data[0][1])