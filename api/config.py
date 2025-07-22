"""API config"""
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / '.env'


class Config(BaseSettings):
    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    API_DB_NAME: str
    API_DB_PORT: str

    model_config = SettingsConfigDict(env_file=ENV_PATH,
                                      env_file_encoding='utf-8',
                                      extra='ignore')
    @property
    def api_db_url(self) -> str:
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}:{self.API_DB_PORT}/{self.API_DB_NAME}")


config = Config() # type: ignore