"""Bot config"""
import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env",
                                      env_file_encoding='utf-8',
                                      extra='ignore')
    DB_HOST: str
    TG_BOT_TOKEN: str


# import this to use config
print(os.path.join(os.path.dirname('api'), ".env"))
config = Config() # type: ignore