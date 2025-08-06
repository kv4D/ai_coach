"""Endpoints for TrainingPlan."""
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.ai_request import UserAIRequest
from schemas.training_plan import TrainingPlan, TrainingPlanInput
from db.database import get_db_session
from service import training_plan as service


router = APIRouter(prefix=f"/plan")


@router.post('/create/user/{user_id}')
async def create_user_plan(user_id: int,
                           plan_data: TrainingPlanInput,
                           session: AsyncSession = Depends(get_db_session)) -> TrainingPlan | None:
    """Create training plan for the user with provided ID.

    Args:
        user_id (`int`)
        user_data (`TrainingPlanInput`): new data for the user
        session (`AsyncSession`): an asynchronous database session
    """
    training_plan = await service.create(user_id, plan_data, session=session)
    return training_plan

@router.post('/generate')
async def generate_user_plan(request: UserAIRequest,
                             session: AsyncSession = Depends(get_db_session)):
    training_plan = await service.generate_plan(request, session=session)
    return training_plan

@router.get('/get/user/{user_id}')
async def get_user_plan(user_id: int,
                        session: AsyncSession = Depends(get_db_session)) -> TrainingPlan:
    """Get user's training plan by their id.

    Args:
        user_id (`int`)
        session (`AsyncSession`): asynchronous database session
    """
    return await service.get_user_plan(user_id, session)

@router.delete('/delete/user/{user_id}')
async def delete_plan_by_user_id(user_id: int,
                                 session: AsyncSession = Depends(get_db_session)) -> JSONResponse:
    """Get user's training plan by their id.

    Args:
        user_id (`int`)
        session (`AsyncSession`): asynchronous database session
    """
    await service.delete(user_id, session)
    return JSONResponse(status_code=200,
                        content={'message': f'Training plan of user with ID={user_id} was deleted.'})