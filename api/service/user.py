from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from db.crud.crud import UserCRUD
from schemas.user import User, UserInput, UserUpdate
from schemas.utils import models_validate
from exceptions import AlreadyExistError, NotFoundError


async def create(user_data: UserInput, session: AsyncSession):
    try:
        user = await UserCRUD.create(user_data, session=session)
        user_data = User.model_validate(user)
        await session.commit()
        return user_data
    except IntegrityError as e:
        await session.rollback()
        error_message = str(e).lower()

        if 'foreign key' in error_message:
            raise NotFoundError("No such activity level.") from e
        if 'unique' in error_message:
            raise AlreadyExistError('There is already a user with such ID.') from e

async def get_all(session: AsyncSession):
    users = await UserCRUD.get_all(session=session)
    if users is None:
        raise NotFoundError('There are no users yet.')
    return models_validate(User, users)

async def get_by_id(user_id: int, session: AsyncSession):
    user = await UserCRUD.get_by_id(user_id, session=session)
    if user is None:
        raise NotFoundError("There is no user with such ID.")
    return User.model_validate(user)

async def update(user_id: int,
                 user_data: UserUpdate,
                 session: AsyncSession):
    try:
        user = await UserCRUD.update_by_id(user_id, user_data, session=session)
        await session.commit()
        return User.model_validate(user)
    except NotFoundError:
        await session.rollback()
        raise

async def delete(user_id: int,
                 session: AsyncSession):
    try:
        await UserCRUD.delete_by_id(user_id, session=session)
        await session.commit()
    except NotFoundError:
        await session.rollback()
        raise
