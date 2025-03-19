from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.models.users import UsersOrm
from src.schemas.users import User


class UsersRepository(BaseRepository)  :
    model = UsersOrm
    schema = User

    async def get_tg_id_by_id(self, id) : 
        query = select(UsersOrm).filter_by(id=id)
        user = await self.session.execute(query)
        return user.tg_id