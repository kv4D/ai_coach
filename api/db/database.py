"""Database related tools. Use to get sessions."""
from functools import wraps
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from config import config


engine = create_async_engine(url=config.api_db_url)

# use to work with database
session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_db_session():
    """
    Provides session to an endpoint as a dependency.

    Don't forget to use 'session.commit()' when
    making changes in database.

    Otherwise changes will be lost.
    """
    async with session_maker() as session:
            yield session

def connect(commit: bool = True):
    """
    ! DON'T USE, THIS IS AN EXAMPLE !

    Decorator creates database session for a method and closes it.
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
