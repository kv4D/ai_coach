from db.crud.crud import UserCRUD
from sqlalchemy.ext.asyncio import AsyncSession


async def create(user_data: dict, session: AsyncSession):
    """Create new user"""
    try:
        user = await UserCRUD.create(session=session, **user_data)
        await session.commit()
        return user.id
    except Exception as e:
        await session.rollback()
        raise e

async def get_all(session: AsyncSession):
    """Get all users in the database"""
    users = await UserCRUD.get_all(session=session)
    return users

async def get_by_id(id: int, session: AsyncSession):
    """Get a user by their ID"""
    user = await UserCRUD.get_by_id(id=id, session=session)
    return user