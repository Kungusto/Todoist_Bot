from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey

class TasksSecondStepORM(Base) : 
    __tablename__ = 'TasksStep2'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True) 
    id_super_task: Mapped[int] = mapped_column(ForeignKey('TasksStep1.id'))    
    title: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
