from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.training_plan import TrainingPlan, TrainingPlanIn
from db.database import get_db_session
from service import training_plan as service


router = APIRouter(prefix=f"/plan")


@router.get('')
def ping() -> str:
    """Test endpoint"""
    return 'Hello, User'

@router.post('/post/user={id}')
async def create_user_plan(plan_data: TrainingPlanIn,
                           id: int,
                           session: AsyncSession = Depends(get_db_session)):
    """Create training plan for the user with provided ID."""
    return await service.create(plan_data.model_dump(), user_id=id, session=session)

@router.get('/get/user={id}')
async def get_user_plan(id: int,
                        session: AsyncSession = Depends(get_db_session)) -> TrainingPlan | dict:
    """Get user's training plan by their id.

    Args:
        id (int): user id in database
        session (AsyncSession, optional): asynchronous database session. Defaults to Depends(get_db_session).
    
    Returns:
        TrainingPlan: user's training plan
    """
    return await service.get_user_plan(id, session)