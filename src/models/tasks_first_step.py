from sqlalchemy import String, Integer
from sqlalchemy.orm import mapped_column, Mapped
from src.database import Base

from datetime import datetime

class TasksFirstStepOrm(Base) :
    __tablename__ = 'TasksStep1'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(String(250))
    complation_due: Mapped[datetime] = mapped_column(default=datetime.now())
    priority: Mapped[int] = mapped_column(Integer(), nullable=False)

    