"""Bot config"""
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / '.env'


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_PATH,
                                      env_file_encoding='utf-8',
                                      extra='ignore')
    DB_HOST: str
    TG_BOT_TOKEN: str
    TG_BOT_STORAGE_PORT: int


# import this to use config
config = Config() # type: ignore