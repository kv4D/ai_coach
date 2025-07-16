from db.crud.crud import UserCRUD
from db.database import connect
from sqlalchemy.ext.asyncio import AsyncSession


@connect()
async def create(user_data: dict, session: AsyncSession):
    print(user_data)
    print(session, 'session')
    user = await UserCRUD.create(session=session, **user_data)
    return user.id

@connect(commit=False)
async def get_all(session: AsyncSession):
    users = await UserCRUD.get_all(session=session)
    return users

@connect(commit=False)
async def get_by_id(id: int, session: AsyncSession):
    user = await UserCRUD.get_by_id(id=id, session=session)
    return user