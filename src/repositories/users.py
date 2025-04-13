from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.models.users import UsersOrm
from src.schemas.users import User


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