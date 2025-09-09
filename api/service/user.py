"""Service layer logic for User."""
from pydantic import ValidationError as PydanticValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from database.crud import ActivityLevelCRUD, UserCRUD
from schemas.user import User, UserInput, UserUpdate
from schemas.utils import models_validate
from schemas.ai_request import UserAIRequest
from schemas.activity_level import ActivityLevel
from exceptions import AlreadyExistError, NotFoundError, ValidationError, \
    UnexpectedError
from llm.ai_client import AIClient


async def create(user_data: UserInput, session: AsyncSession):
    """Create a new user in the database.

    Args:
        user_data (`UserInput`): data for a new user
        session (`AsyncSession`): an asynchronous database session
    """
    try:
        await UserCRUD.create(user_data, session=session)
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        error_message = str(exc).lower()
        if 'foreign key' in error_message:
            raise NotFoundError(
                f"No such activity level: {user_data.activity_level}") from exc
    except AlreadyExistError as exc:
        await session.rollback()
        raise AlreadyExistError(
            f'There is already a user with such ID: {user_data.id}') from exc
    except PydanticValidationError as exc:
        await session.rollback()
        raise ValidationError(f"Validation error:\n{str(exc)}") from exc
    except Exception as exc:
        await session.rollback()
        raise UnexpectedError(f"An error occurred:\n{str(exc)}.") from exc


async def set_activity_level(user: User, session: AsyncSession):
    """Set activity level for user."""
    if user.activity_level:
        activity_level = await ActivityLevelCRUD.get_by_id(user.activity_level, session)
        if activity_level:
            user.activity_level_info = ActivityLevel.model_validate(
                activity_level)


async def get_all(session: AsyncSession) -> list[User]:
    """Get all users in the database.

    Args:
        session (`AsyncSession`): an asynchronous database session
    """
    users = await UserCRUD.get_all(session=session)

    if users is None:
        raise NotFoundError('There are no users.')

    users = models_validate(User, users)

    for user in users:
        await set_activity_level(user, session=session)

    return users


async def get_by_id(user_id: int, session: AsyncSession) -> User:
    """Get the user by their ID in the database.

    Args:
        user_id (`int`)
        session (`AsyncSession`): an asynchronous database session
    """
    user = await UserCRUD.get_by_id(user_id, session=session)

    if user is None:
        raise NotFoundError(f"There is no user with such ID: {user_id}.")

    user = User.model_validate(user)
    await set_activity_level(user, session=session)

    return user


async def update(user_id: int,
                 user_data: UserUpdate,
                 session: AsyncSession):
    """Update the user by their ID in the database.

    Args:
        user_id (`int`)
        user_data (`UserUpdate`): new data for the user
        session (`AsyncSession`): an asynchronous database session
    """
    try:
        await UserCRUD.update_by_id(user_id, user_data, session=session)
        await session.commit()
    except NotFoundError:
        await session.rollback()
        raise
    except PydanticValidationError as exc:
        await session.rollback()
        raise ValidationError(f"Validation error:\n{str(exc)}") from exc
    except Exception as exc:
        await session.rollback()
        raise UnexpectedError(f"An error occurred:\n{str(exc)}.") from exc


async def delete(user_id: int,
                 session: AsyncSession) -> None:
    """Delete the user by their ID in the database.

    Args:
        user_id (`int`)
        session (`AsyncSession`): an asynchronous database session
    """
    try:
        await UserCRUD.delete_by_id(user_id, session=session)
        await session.commit()
    except NotFoundError:
        await session.rollback()
        raise
    except Exception as exc:
        await session.rollback()
        raise UnexpectedError(f"An error occurred:\n{str(exc)}.") from exc


async def get_ai_answer(request: UserAIRequest,
                        session: AsyncSession) -> str:
    """Answer user's request/answer with AI.

    Args:
        user_id (`int`)
        user_request (`str`): user's message to AI
        session (`AsyncSession`): an asynchronous database session
    """
    user = await get_by_id(request.user_id, session)
    response = await AIClient.generate_user_response(user, request.content)
    return response
