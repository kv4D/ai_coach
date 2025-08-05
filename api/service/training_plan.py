"""Service layer logic for TrainingPlan."""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from exceptions import NotFoundError
from db.crud.crud import TrainingPlanCRUD
from schemas.training_plan import TrainingPlan, TrainingPlanInput, TrainingPlanUpdate


async def create(user_id: int, 
                 plan_data: TrainingPlanInput, 
                 session: AsyncSession) -> TrainingPlan | None:
    """Create a new training plan for the user in the database.

    Args:
        user_id (`int`)
        plan_data (`ActivityLevelInput`): data for a new training plan
        session (`AsyncSession`): an asynchronous database session
    """
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

async def get_user_plan(user_id: int, session: AsyncSession) -> TrainingPlan:
    """Get the training plan for the user in the database.

    Args:
        user_id (`int`)
        session (`AsyncSession`): an asynchronous database session
    """
    plan = await TrainingPlanCRUD.get_by_user_id(user_id, session=session)
    if plan is None:
        raise NotFoundError(f'No training plan for user with this ID: {user_id}')
    plan = TrainingPlan.model_validate(plan)
    return plan

async def update_user_plan(user_id: int, 
                           plan_data: TrainingPlanUpdate, 
                           session: AsyncSession) -> None:
    """Update the training plan for the user in the database.

    Yoy can change plan's content, but not the user who owns the plan.

    Args:
        user_id (`int`)
        plan_data (`TrainingPlanUpdate`): new data for the training plan
        session (`AsyncSession`): an asynchronous database session
    """
    try:
        await TrainingPlanCRUD.update_by_user_id(user_id, plan_data, session=session)
        await session.commit()
    except NotFoundError:
        await session.rollback()
        raise

async def delete(user_id: int, session: AsyncSession) -> None:
    """Delete the training plan for the user in the database.

    Args:
        user_id (`int`)
        session (`AsyncSession`): an asynchronous database session
    """
    try:
        await TrainingPlanCRUD.delete_by_id(user_id, session=session)
        await session.commit()
    except NotFoundError:
        await session.rollback()
        raise