from sqlalchemy.ext.asyncio import AsyncSession
from db.crud.crud import TrainingPlanCRUD
from schemas.training_plan import TrainingPlan


async def create(plan_data: dict, user_id: int, session: AsyncSession):
    """Create new activity level"""
    try:
        plan = await TrainingPlanCRUD.create_for_user(user_id, session=session, **plan_data)
        await session.commit()
        return plan.id
    except Exception as e:
        await session.rollback()
        raise e

async def get_user_plan(user_id: int, session: AsyncSession):
    """Get info about the level in the database by its value"""
    plan = await TrainingPlanCRUD.get_by_user_id(user_id, session=session)
    if plan:
        return TrainingPlan.model_validate(plan)
    return {'message': f'Not found with provided user id: {user_id}'}
