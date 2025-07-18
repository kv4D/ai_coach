from functools import wraps
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from config import config


engine = create_async_engine(url=config.api_db_url)

# use to work with database
session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_db_session():
    """
    Provides session to endpoint as a dependency.
    Don't forget to use 'session.commit()' when
    making changes in database.
    """
    async with session_maker() as session:
            yield session

def connect(commit: bool = True):
    """
    Decorator creates database session for a method and closes it.
    Experimental feature, use get_db_session() instead.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            async with session_maker() as session:
                try:
                    result = await func(*args, session=session, **kwargs)
                    if commit:
                        await session.commit()
                    return result
                except Exception as e:
                    # rollback changes if something's wrong
                    await session.rollback()
                    raise e
                finally:
                    await session.close()
        return wrapper
    return decorator
