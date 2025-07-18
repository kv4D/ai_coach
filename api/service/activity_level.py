from sqlalchemy.ext.asyncio import AsyncSession
from db.crud.crud import ActivityLevelCRUD
from schemas.activity_level import ActivityLevel


async def create(level_data: dict, session: AsyncSession):
    """Create new activity level"""
    try:
        level = await ActivityLevelCRUD.create(session=session, **level_data)
        await session.commit()
        return level.id
    except Exception as e:
        await session.rollback()
        raise e

async def get_info_by_level(level: int, session: AsyncSession):
    """Get info about the level in the database by its value"""
    level_model = await ActivityLevelCRUD.get_by_level(level=level, session=session)
    return ActivityLevel.model_validate(level_model)

async def get_all_levels(session: AsyncSession):
    """Get all 'level' fields of activity levels in the database"""
    levels = await ActivityLevelCRUD.get_all(session=session)
    levels = [level.level for level in levels]
    return levels
