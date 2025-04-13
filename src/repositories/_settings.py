from src.models._settings import SettingsOrm
from src.schemas._settings import Setting
from src.repositories.base import BaseRepository

class SettingsRepository(BaseRepository) :
    schema = Setting 
    model = SettingsOrm