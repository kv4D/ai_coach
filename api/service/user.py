from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from db.crud.crud import UserCRUD
from schemas.user import User, UserInput, UserUpdate
from schemas.utils import models_validate
from exceptions import AlreadyExistError, NotFoundError


async def create(user_data: UserInput, session: AsyncSession):
    try:
        user = await UserCRUD.create(user_data, session=session)
        await session.commit()
        return User.model_validate(user)
    except IntegrityError as e:
        await session.rollback()
        error_message = str(e).lower()
        
        if 'foreign key' in error_message:
            raise NotFoundError(f"No activity level with such ID.")
        if 'unique' in error_message:
            raise AlreadyExistError(f'There is already a user with such ID.')

async def get_all(session: AsyncSession):
    users = await UserCRUD.get_all(session=session)
    if users is None:
        raise NotFoundError('There are no users yet.')
    return models_validate(User, users)

async def get_by_id(id: int, session: AsyncSession):
    user = await UserCRUD.get_by_id(id=id, session=session)
    if user is None:
        raise NotFoundError("There is no user with such ID.")
    return User.model_validate(user)

async def update(id: int, 
                 user_data: UserUpdate, 
                 session: AsyncSession):
    try:
        user = await UserCRUD.update_by_id(id, user_data, session=session)
        await session.commit()
        return User.model_validate(user)
    except NotFoundError:
        await session.rollback()
        raise