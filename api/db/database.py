from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from config import config


engine = create_async_engine(url=config.api_db_url)
# use to work with database
session_maker = async_sessionmaker(engine, expire_on_commit=False)


def connect(method):
    """
    Creates database session for method and closes it.
    """
    async def wrapper(*args, **kwargs):
        async with session_maker() as session:
            try:
                return await method(*args, session=session, **kwargs)
            except Exception as e:
                # rollback changes
                await session.rollback()
                raise e
            finally:
                await session.close()
    return wrapper