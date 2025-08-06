from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from db.crud.crud import ActivityLevelCRUD, UserCRUD
from schemas.user import User, UserInput, UserUpdate
from schemas.utils import models_validate
from schemas.activity_level import ActivityLevel
from exceptions import AlreadyExistError, NotFoundError


async def create(user_data: UserInput, session: AsyncSession):
    try:
        user = await UserCRUD.create(user_data, session=session)
        user = User.model_validate(user)
        await session.commit()
        return user
    except IntegrityError as e:
        await session.rollback()
        error_message = str(e).lower()

        if 'foreign key' in error_message:
            raise NotFoundError("No such activity level.") from e
        if 'unique' in error_message:
            raise AlreadyExistError('There is already a user with such ID.') from e
    except:
        await session.rollback()
        raise

async def set_activity_level(user: User, session: AsyncSession):
    if user.activity_level:
        activity_level = await ActivityLevelCRUD.get_by_id(user.activity_level, session)
        user.activity_level_info = ActivityLevel.model_validate(activity_level)

async def get_all(session: AsyncSession) -> list[User]:
    """Get all users in the database.

    Args:
        session (`AsyncSession`): an asynchronous database session
    """
    users = await UserCRUD.get_all(session=session)

    users = models_validate(User, users)

    if users is None:
        raise NotFoundError('There are no users.')

    for user in users:
        await set_activity_level(user, session=session)

    return users

async def get_by_id(user_id: int, session: AsyncSession):
    user = await UserCRUD.get_by_id(user_id, session=session)
    if user is None:
        raise NotFoundError("There is no user with such ID.")

    user = User.model_validate(user)
    await set_activity_level(user, session=session)

    return user

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
