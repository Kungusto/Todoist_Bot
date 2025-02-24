from src.database import Base
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from datetime import date

class UsersOrm(Base) :
    __tablename__ = 'Users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[str] = mapped_column(unique=True)
    registrated : Mapped[date] = mapped_column(default=date.today())
    password: Mapped[str] = mapped_column(String(85))
    # day_streak: Mapped[int] = mapped_column(default=0)  - фича