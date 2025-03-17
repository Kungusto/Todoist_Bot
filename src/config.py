from dotenv import load_dotenv
from pathlib import Path


# Путь к .env файлу
env_path = Path(__file__).resolve().parent.parent / ".env"

# Загружаем .env
load_dotenv(env_path)

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    TOKEN: str

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"



# Инициализация
settings = Settings()
