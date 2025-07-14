from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from config import config


engine = create_async_engine(url=config.postgres_db_url)
async_sessionmaker = async_sessionmaker(engine, expire_on_commit=False)