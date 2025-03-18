from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

class SettingsOrm(Base) :
    __tablename__ = "SettingsTable"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("Users.id"))
    # дальше сказал сам допишешь
    '''
    mapped_column : 
        unique = True - каждая строчка столбца уникальна
        nullable = True/False  - может ли быть пустым
    вроде все. остальное врят-ли пригодится
    '''
