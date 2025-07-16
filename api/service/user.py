from db.crud.crud import UserCRUD
from db.database import connect
from asyncio import run
from sqlalchemy.ext.asyncio import AsyncSession


@connect
async def create(user_data: dict, session: AsyncSession):
    user = await UserCRUD.create(session=session, **user_data)
    return user.id

@connect
async def get_all(session: AsyncSession):
    users = await UserCRUD.get_all(session=session)
    return users
