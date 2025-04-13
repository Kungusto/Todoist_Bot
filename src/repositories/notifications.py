from src.repositories.base import BaseRepository
from src.models.notificatoins import NotificationsORM
from src.schemas.notifications import Notification

class NotificationsRepository(BaseRepository) :
    model = NotificationsORM
    schema = Notification