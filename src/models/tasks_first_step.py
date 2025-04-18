from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from src.database import Base
from datetime import datetime

class TasksFirstStepOrm(Base):
    __tablename__ = 'TasksStep1'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('Users.id'))
    title: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    complation_due: Mapped[datetime | None] = mapped_column(default=datetime.now)  # Исправлено
    priority: Mapped[int | None] = mapped_column(Integer())
    status: Mapped[int | None] = mapped_column(Integer(), default=1)

    # important: Mapped[bool] = mapped_column(default=False, nullable=False) - пока его нет в миграциях. я не понял что ты имел ввиду
