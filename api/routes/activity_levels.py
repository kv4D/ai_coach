from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.activity_level import ActivityLevel, ActivityLevelInput, ActivityLevelUpdate
from db.database import get_db_session
from service import activity_level as service


router = APIRouter(prefix=f"/level")


@router.get('')
def ping() -> str:
    """Test endpoint"""
    return 'Hello, User'

@router.post('/create')
async def create_activity_level(level_data: ActivityLevelInput,
                               session: AsyncSession = Depends(get_db_session)):
    """Create new activity level"""
    return await service.create(level_data, session=session)

@router.get('/all')
async def get_all(session: AsyncSession = Depends(get_db_session)) -> list[ActivityLevel] | None:
    """Get all activity levels in numbers"""
    levels = await service.get_all_levels(session=session)
    return levels

@router.patch('update/{id}')
async def update_activity_level(id: int,
                                level_data: ActivityLevelUpdate,
                                session: AsyncSession = Depends(get_db_session)):
    level = await service.update(id, level_data, session=session)
    return level