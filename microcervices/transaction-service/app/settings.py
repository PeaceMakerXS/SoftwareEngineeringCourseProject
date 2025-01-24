from dotenv import find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    model_config = SettingsConfigDict(
        env_file=find_dotenv()
    )


settings = Settings()

def get_db_url():
    return (f'postgresql+asyncpg://{settings.DB_USER}@'
            f'{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}')