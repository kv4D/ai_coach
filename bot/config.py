"""Bot config"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from os import getenv


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env',
                                      env_file_encoding='utf-8',
                                      extra='ignore')
    
    db_host: str
    bot_token: str
