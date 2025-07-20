from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from db.crud.crud import UserCRUD
from schemas.user import User
from schemas.utils import models_validate
from exceptions import AlreadyExistError, NotFoundError


async def create(user_data: User, session: AsyncSession):
    try:
        user = await UserCRUD.create(user_data, session=session)
        user = User.model_validate(user)
        await session.commit()
        return user
    except IntegrityError as e:
        await session.rollback()
        error_message = str(e).lower()
        
        if 'foreign key' in error_message:
            raise NotFoundError(f"No activity level with such ID.")
        if 'unique' in error_message:
            raise AlreadyExistError(f'There is already a user with such ID.')

async def get_all(session: AsyncSession):
    users = await UserCRUD.get_all(session=session)
    users = models_validate(User, users)
    if users is None:
        raise NotFoundError('There are no users yet.')
    return users

async def get_by_id(id: int, session: AsyncSession) -> User:
    user = await UserCRUD.get_by_id(id=id, session=session)
    user = User.model_validate(user)
    if user is None:
        raise NotFoundError("There is no user with such ID.")
    return user
