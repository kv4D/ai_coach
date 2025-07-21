from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from exceptions import NotFoundError
from db.crud.crud import TrainingPlanCRUD
from schemas.training_plan import TrainingPlan, TrainingPlanInput


async def create(user_id: int, 
                 plan_data: TrainingPlanInput, 
                 session: AsyncSession):
    try:
        plan = await TrainingPlanCRUD.create_for_user(user_id, 
                                                      plan_data, 
                                                      session=session)
        await session.commit()
        return TrainingPlan.model_validate(plan)
    except IntegrityError as e:
        await session.rollback()
        error_message = str(e).lower()
        if 'foreign key' in error_message:
            raise NotFoundError(f"No user with such ID.")

async def get_user_plan(user_id: int, session: AsyncSession):
    plan = await TrainingPlanCRUD.get_by_user_id(user_id, session=session)
    if plan is None:
        raise NotFoundError(f'No training plan for user with this ID: {user_id}')
    plan = TrainingPlan.model_validate(plan)
    return plan
