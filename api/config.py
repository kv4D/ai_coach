"""API config, contains all required config for the API."""
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# path to the env file
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = BASE_DIR / '.env'


class Config(BaseSettings):
    """Config model, contains all required config for the API."""
    HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_PORT: str

    AI_API_KEY: str
    AI_MODEL_NAME: str
    AI_API_MAX_RETRIES: int = 10

    model_config = SettingsConfigDict(env_file=ENV_PATH,
                                      env_file_encoding='utf-8',
                                      extra='ignore')

    @property
    def api_db_url(self) -> str:
        """Database URL for the API."""
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.HOST}:{self.DB_PORT}/{self.DB_NAME}")


# import this to get the configuration
config = Config()  # type: ignore
