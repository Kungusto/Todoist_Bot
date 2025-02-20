from sqlalchemy import insert, select
from src.database import async_session_maker
from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase

class BaseRepository :
    model : DeclarativeBase = None
    schema : BaseModel = None 

    def __init__(self, session) :
        self.session = session
    
    async def get_all(self) :
        query = (select(self.model))
        result = await self.session.execute(query) 
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]

    async def add(self, data) :
        add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        query = await self.session.execute(add_stmt)
        result = query.scalars().first()
        return self.schema.model_validate(result, from_attributes=True)
        
    async def get_filtered(self, *filter, **filter_by) :
        query = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]
