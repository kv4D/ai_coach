"""Service layer logic for ActivityLevel."""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from exceptions import AlreadyExistError, NotFoundError
from db.crud.crud import ActivityLevelCRUD
from schemas.activity_level import ActivityLevel, ActivityLevelInput, ActivityLevelUpdate
from schemas.utils import models_validate


async def create(level_data: ActivityLevelInput, session: AsyncSession) -> ActivityLevel | None:
    """Create a new activity level in the database.

    Args:
        level_data (`ActivityLevelInput`): data for a new activity level
        session (`AsyncSession`): an asynchronous database session
    """
    try:
        level = await ActivityLevelCRUD.create(level_data, session=session)
        await session.commit()
        return ActivityLevel.model_validate(level)
    except IntegrityError as e:
        await session.rollback()
        error_message = str(e).lower()
        if 'unique' in error_message:
            raise AlreadyExistError('There is already an activity level with such ID.') from e

async def get_by_level(level: int, session: AsyncSession) -> ActivityLevel:
    """Get info about the level in the database by its level number.

    In case of ActivityLevel, **level** field is the ID (primary key).

    Args:
        level (`int`): ActivityLevel number / **level** field
        session (`AsyncSession`): an asynchronous database session
    """
    level_model = await ActivityLevelCRUD.get_by_id(level, session=session)
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
                 session: AsyncSession) -> ActivityLevel:
    """Update the activity level by their level number in the database.

    Args:
        level (`int`): ActivityLevel number / **level** field
        user_data (`UserUpdate`): new data for the user
        session (`AsyncSession`): an asynchronous database session
    """
    try:
        level_model = await ActivityLevelCRUD.update_by_id(level, level_data, session=session)
        await session.commit()
        return ActivityLevel.model_validate(level_model)
    except NotFoundError:
        await session.rollback()
        raise

async def delete(level: int,
                 session: AsyncSession) -> None:    
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