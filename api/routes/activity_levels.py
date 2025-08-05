"""Endpoints for ActivityLevel."""
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.activity_level import ActivityLevel, ActivityLevelInput, ActivityLevelUpdate
from db.database import get_db_session
from service import activity_level as service


router = APIRouter(prefix="/level")


@router.post('/create')
async def create_activity_level(level_data: ActivityLevelInput,
                                session: AsyncSession = Depends(get_db_session)) -> ActivityLevel | None:
    """Create new activity level.

    Use with care: the levels must be relevant.

    Args:
        level_data (`ActivityLevelInput`): new data for the user
        session (`AsyncSession`): an asynchronous database session
    """
    activity_level = await service.create(level_data, session=session)
    return activity_level

@router.get('/all')
async def get_all(session: AsyncSession = Depends(get_db_session)) -> list[ActivityLevel]:
    """Get all activity levels.

    Args:
        session (`AsyncSession`): an asynchronous database session
    """
    levels = await service.get_all_levels(session=session)
    return levels

@router.get('/get/{level}')
async def get_by_level(level: int,
                       session: AsyncSession = Depends(get_db_session)) -> ActivityLevel:
    """Get activity level data by its level number.

    Args:
        level (`int`): ActivityLevel number
        session (`AsyncSession`): an asynchronous database session
    """
    return await service.get_by_level(level, session=session)

@router.patch('/update/{level}')
async def update_activity_level(level: int,
                                level_data: ActivityLevelUpdate,
                                session: AsyncSession = Depends(get_db_session)) -> JSONResponse:
    """Update activity level by its level number.

    Args:
        level (`int`): ActivityLevel number
        level_data (`ActivityLevelUpdate`): new data for the activity level
        session (`AsyncSession`): an asynchronous database session
    """
    await service.update(level, level_data, session=session)
    return JSONResponse(status_code=200,
                        content={"message": f"Activity level with level={level} was updated"})

@router.delete('/delete/{level}')
async def delete_level(level: int,
                       session: AsyncSession = Depends(get_db_session)) -> JSONResponse:
    """Delete the activity level by its number.
            
    Args:
        level (`int`): ActivityLevel number
        session (`AsyncSession`): an asynchronous database session
    """
    await service.delete(level, session=session)
    return JSONResponse(status_code=200,
                        content={"message": f"Activity level with level={level} was deleted"})