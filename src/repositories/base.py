from sqlalchemy import insert, select, update
from src.database import async_session_maker
from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import delete

from pydantic import BaseModel

class BaseRepository :
    '''
    Все методы возвращают Pydantic-схему. 
    Способы с ними работать:
    1. преобразовать в словарь с помощью .to_dict()
    2. обращаться к атрибутам напримую через точку: *Pydantic-схема*.id
    '''
    model : DeclarativeBase = None
    schema : BaseModel = None 

    def __init__(self, session) :
        self.session = session
    
    async def get_all(self) :
        '''Получает абсолютно все записи таблички и возвращает pydantic-схему'''
        query = (select(self.model))
        result = await self.session.execute(query) 
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]

    async def add(self, data: BaseModel) :
        '''
        Принимает на вход pydantic-схему(ту, в которой айди не указан!), 
        записывает данные в новый столбец
        '''
        print(data.model_dump())
        add_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        query = await self.session.execute(add_stmt)
        result = query.scalars().first()
        return self.schema.model_validate(result, from_attributes=True)
        
    async def get_filtered(self, *filter, **filter_by) :
        '''
        Получить данные с фильтрами. Аргументы:
        1. **filter_by работает когда мы вызываем: get_filtered(user_id=1) 
        в этом случае мы получим всех юзеров с первым айдишником
        2. *filter принимает более сложные условия. скорей всего тебе не поднадобиться
        '''
        query = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]

    async def edit(self, data: BaseModel, **filter_by) :
        update_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=True))
            .returning(self.model)
        )
        result = await self.session.execute(update_stmt)
        return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]


    async def delete_filtered(self, *filter, **filter_by):
        """
        Удаляет записи с указанными фильтрами.
        Пример использования: await repo.delete_filtered(user_id=1)
        """
        delete_stmt = delete(self.model).filter(*filter).filter_by(**filter_by)
        await self.session.execute(delete_stmt)