"""API config"""
import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env",
                                      env_file_encoding='utf-8',
                                      extra='ignore')
    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    API_DB_NAME: str
    API_DB_PORT: str

    @property
    def api_db_url(self) -> str:
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}:{self.API_DB_PORT}/{self.API_DB_NAME}")


# import this to use config
config = Config() # type: ignore