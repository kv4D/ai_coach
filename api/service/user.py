"""Service layer logic for User."""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from db.crud.crud import UserCRUD
from schemas.user import User, UserInput, UserUpdate
from schemas.utils import models_validate
from schemas.ai_request import UserAIRequest
from exceptions import AlreadyExistError, NotFoundError
from llm.ai_client import AIClient


async def create(user_data: UserInput, session: AsyncSession) -> User | None:
    """Create a new user in the database.

    Args:
        user_data (`UserInput`): data for a new user
        session (`AsyncSession`): an asynchronous database session
    """
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

async def get_all(session: AsyncSession) -> list[User]:
    """Get all users in the database.

    Args:
        session (`AsyncSession`): an asynchronous database session
    """
    users = await UserCRUD.get_all(session=session)
    if users is None:
        raise NotFoundError('There are no users.')
    return models_validate(User, users)

async def get_by_id(user_id: int, session: AsyncSession) -> User:
    """Get the user by their ID in the database.

    Args:
        user_id (`int`)
        session (`AsyncSession`): an asynchronous database session
    """
    user = await UserCRUD.get_by_id(user_id, session=session)
    if user is None:
        raise NotFoundError("There is no user with such ID.")
    return User.model_validate(user)

async def update(user_id: int,
                 user_data: UserUpdate,
                 session: AsyncSession) -> User:
    """Update the user by their ID in the database.

    Args:
        user_id (`int`)
        user_data (`UserUpdate`): new data for the user
        session (`AsyncSession`): an asynchronous database session
    """
    try:
        user = await UserCRUD.update_by_id(user_id, user_data, session=session)
        await session.commit()
        return User.model_validate(user)
    except NotFoundError:
        await session.rollback()
        raise

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

async def get_ai_answer(request: UserAIRequest,
                        session: AsyncSession) -> str:
    """Answer user's request/answer with AI.
    
    Args:
        user_id (`int`)
        user_request (`str`): user's message to AI
        session (`AsyncSession`): an asynchronous database session
    """
    user = await get_by_id(request.user_id, session)
    response = await AIClient.generate_user_response(user, request.request)
    return response
