from dotenv import load_dotenv
import os
from pathlib import Path

from pydantic_settings import BaseSettings

# Путь к .env файлу
env_path = Path(__file__).resolve().parent.parent / ".env"

# Загружаем .env
load_dotenv(env_path)

# Проверка переменных
print("DB_HOST:", os.getenv("DB_HOST"))
print("DB_PORT:", os.getenv("DB_PORT"))
print("DB_NAME:", os.getenv("DB_NAME"))
print("DB_USER:", os.getenv("DB_USER"))
print("DB_PASS:", os.getenv("DB_PASS"))
print("TOKEN:", os.getenv("TOKEN"))


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
