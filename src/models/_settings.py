from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

class SettingsOrm(Base) :
    __tablename__ = "SettingsTable"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("Users.id"))
    task_sort: Mapped[int]
    task_filter: Mapped[int]
    notifications: Mapped[bool] 
    time_format: Mapped[int]
    auto_delete: Mapped[int]
    ai: Mapped[bool]
    language: Mapped[str]
    '''
    mapped_column : 
        unique = True - каждая строчка столбца уникальна
        nullable = True/False  - может ли быть пустым
    вроде все. остальное врят-ли пригодится
    '''
    
# "notifications" : False,
# "time_format" : 24,
# "auto_delete" : 7,
# "ai" : True,
# "language" : "Russian"