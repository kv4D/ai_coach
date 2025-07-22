from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.training_plan import TrainingPlan, TrainingPlanInput
from db.database import get_db_session
from service import training_plan as service


router = APIRouter(prefix=f"/plan")


@router.post('/create/user/{user_id}')
async def create_user_plan(user_id: int,
                           plan_data: TrainingPlanInput,
                           session: AsyncSession = Depends(get_db_session)):
    """Create training plan for the user with provided ID."""
    return await service.create(user_id, plan_data, session=session)

@router.get('/get/user/{user_id}')
async def get_user_plan(user_id: int,
                        session: AsyncSession = Depends(get_db_session)) -> TrainingPlan | dict:
    """Get user's training plan by their id.

    Args:
        id (int): user id in database
        session (AsyncSession, optional): asynchronous database session. Defaults to Depends(get_db_session).
    
    Returns:
        TrainingPlan: user's training plan
    """
    return await service.get_user_plan(user_id, session)

@router.delete('/delete/user/{user_id}')
async def delete_plan_by_user_id(user_id: int,
                                 session: AsyncSession = Depends(get_db_session)):
    await service.delete(user_id, session)
    return JSONResponse(status_code=200,
                        content={'message': f'Training plan of user with ID={user_id} was deleted.'})