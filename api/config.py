"""API config"""
import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"),
                                      env_file_encoding='utf-8',
                                      extra='ignore')
    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    POSTGRES_DB_NAME: str
    POSTGRES_DB_PORT: str
    
    @property
    def postgres_db_url(self) -> str:
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}:{self.POSTGRES_DB_PORT}/{self.POSTGRES_DB_NAME}")


# import this to use config
config = Config() # type: ignore