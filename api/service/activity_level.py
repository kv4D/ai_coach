from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from exceptions import AlreadyExistError, NotFoundError
from db.crud.crud import ActivityLevelCRUD
from schemas.activity_level import ActivityLevel, ActivityLevelInput, ActivityLevelUpdate
from schemas.utils import models_validate


async def create(level_data: ActivityLevelInput, session: AsyncSession):
    """Create new activity level"""
    try:
        level = await ActivityLevelCRUD.create(level_data, session=session)
        await session.commit()
        return ActivityLevel.model_validate(level)
    except IntegrityError as e:
        await session.rollback()
        error_message = str(e).lower()
        if 'unique' in error_message:
            raise AlreadyExistError(f'There is already an activity level with such ID.')

async def get_by_level(level: int, session: AsyncSession):
    """Get info about the level in the database by its value."""
    level_model = await ActivityLevelCRUD.get_by_level(level=level, session=session)
    return ActivityLevel.model_validate(level_model)

async def get_all_levels(session: AsyncSession):
    """Get all 'level' fields of activity levels in the database."""
    levels = await ActivityLevelCRUD.get_all(session=session)
    if levels is None:
        raise NotFoundError("There are no levels yet.")
    return models_validate(ActivityLevel, levels)

async def update(id: int, 
                 level_data: ActivityLevelUpdate, 
                 session: AsyncSession):
    try:
        level = await ActivityLevelCRUD.update_by_id(id, level_data, session=session)
        await session.commit()
        return ActivityLevel.model_validate(level)
    except NotFoundError:
        await session.rollback()
        raise

async def delete(id: int,
                 session: AsyncSession):
    try:
        await ActivityLevelCRUD.delete_by_id(id, session=session)
        await session.commit()
    except NotFoundError:
        await session.rollback()
        raise