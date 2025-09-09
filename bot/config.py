"""Bot config."""
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# .env path
# you can change it
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / '.env'


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_PATH,
                                      env_file_encoding='utf-8',
                                      extra='ignore')
    HOST: str
    BOT_TOKEN: str
    BOT_STORAGE_PORT: int
    API_BASE_URL: str = "http://localhost:8000"


# import this to use config
config = Config()  # type: ignore
