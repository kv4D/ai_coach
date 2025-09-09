"""Service layer logic for ActivityLevel."""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError as PydanticValidationError
from api.exceptions import AlreadyExistError, NotFoundError, UnexpectedError, ValidationError
from api.database.crud import ActivityLevelCRUD
from api.schemas.activity_level import ActivityLevel, ActivityLevelInput, ActivityLevelUpdate
from api.schemas.utils import models_validate


async def create(level_data: ActivityLevelInput, session: AsyncSession):
    """Create a new activity level in the database.

    Args:
        level_data (`ActivityLevelInput`): data for a new activity level
        session (`AsyncSession`): an asynchronous database session
    """
    try:
        await ActivityLevelCRUD.create(level_data, session=session)
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        error_message = str(exc).lower()
        if 'unique' in error_message:
            raise AlreadyExistError(
                f'There is already an activity level with this number: {level_data.level}.'
            ) from exc
        raise
    except PydanticValidationError as exc:
        await session.rollback()
        raise ValidationError(f"Validation error:\n{str(exc)}") from exc
    except Exception as exc:
        await session.rollback()
        raise UnexpectedError(f"An error occurred:\n{str(exc)}.") from exc


async def get_by_level(level: int, session: AsyncSession) -> ActivityLevel:
    """Get info about the level in the database by its level number.

    In case of ActivityLevel, **level** field is the ID (primary key).

    Args:
        level (`int`): ActivityLevel number / **level** field
        session (`AsyncSession`): an asynchronous database session
    """
    level_model = await ActivityLevelCRUD.get_by_id(level, session=session)
    if level_model is None:
        raise NotFoundError(f"There is no activity level with level={level}.")
    return ActivityLevel.model_validate(level_model)


async def get_all_levels(session: AsyncSession) -> list[ActivityLevel]:
    """Get all activity levels in the database.

    Args:
        session (`AsyncSession`): an asynchronous database session
    """
    levels = await ActivityLevelCRUD.get_all(session=session)
    if levels is None:
        raise NotFoundError("There are no levels yet.")
    return models_validate(ActivityLevel, levels)


async def update(level: int,
                 level_data: ActivityLevelUpdate,
                 session: AsyncSession):
    """Update the activity level by their level number in the database.

    Args:
        level (`int`): ActivityLevel number / **level** field
        user_data (`UserUpdate`): new data for the user
        session (`AsyncSession`): an asynchronous database session
    """
    try:
        await ActivityLevelCRUD.update_by_id(level, level_data, session=session)
        await session.commit()
    except NotFoundError:
        await session.rollback()
        raise
    except PydanticValidationError as exc:
        await session.rollback()
        raise ValidationError(f"Validation error:\n{str(exc)}") from exc
    except Exception as exc:
        await session.rollback()
        raise UnexpectedError(f"An error occurred:\n{str(exc)}") from exc


async def delete(level: int,
                 session: AsyncSession):
    """Delete the activity level by their level number in the database.

    Args:
        level (`int`): ActivityLevel number / **level** field
        session (`AsyncSession`): an asynchronous database session
    """
    try:
        await ActivityLevelCRUD.delete_by_id(level, session=session)
        await session.commit()
    except NotFoundError:
        await session.rollback()
        raise
    except Exception as exc:
        await session.rollback()
        raise UnexpectedError(f"An error occurred:\n{str(exc)}") from exc
