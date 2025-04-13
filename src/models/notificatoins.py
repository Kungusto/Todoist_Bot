from src.database import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import ForeignKey
from datetime import datetime

class NotificationsORM(Base) : 
    __tablename__ = 'Notifications'
    id : Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('Users.id'))
    title: Mapped[str] = mapped_column(nullable=False)
    time: Mapped[datetime] = mapped_column(default=datetime.now(), nullable=False)