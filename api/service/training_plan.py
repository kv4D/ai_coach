"""Service layer logic for TrainingPlan."""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError as PydanticValidationError
from exceptions import NotFoundError, UnexpectedError, ValidationError
from db.crud.crud import TrainingPlanCRUD
from schemas.training_plan import TrainingPlan, TrainingPlanInput, TrainingPlanUpdate
from schemas.ai_request import UserAIRequest
from service.user import get_by_id
from llm.ai_client import AIClient


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
    except IntegrityError as exc:
        await session.rollback()
        error_message = str(exc).lower()
        if 'foreign key' in error_message:
            raise NotFoundError(f"There is no user with such ID: {user_id}.") from exc
        raise
    except Exception as exc:
        await session.rollback()
        raise UnexpectedError(f"An error occurred:\n{str(exc)}.") from exc
    

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
    except PydanticValidationError as exc:
        raise ValidationError(f"Validation error:\n{str(exc)}") from exc
    except Exception as exc:
        await session.rollback()
        raise UnexpectedError(f"An error occurred:\n{str(exc)}.") from exc

async def generate_plan(request: UserAIRequest, session: AsyncSession):
    """Generate TrainingPlan using AI.

    You can generate a new plan or update an existing one.

    Args:
        request (`UserAIRequest`): data for making request
        session (`AsyncSession`): an asynchronous database session
    """
    user = await get_by_id(request.user_id, session)
    plan_description = await AIClient.generate_user_plan(user, request.content)

    if user.training_plan:
        plan = TrainingPlanUpdate(plan_description=plan_description)
        return await update_user_plan(user.id, plan, session=session)

    plan = TrainingPlanInput(plan_description=plan_description)
    return await create(request.user_id, plan, session=session)

async def get_user_plan(user_id: int, session: AsyncSession) -> TrainingPlan:
    """Get the training plan for the user in the database.

    Args:
        user_id (`int`)
        session (`AsyncSession`): an asynchronous database session
    """
    plan = await TrainingPlanCRUD.get_by_user_id(user_id, session=session)
    if plan is None:
        raise NotFoundError(f'There is no training plan for user with this ID: {user_id}')
    plan = TrainingPlan.model_validate(plan)
    return plan

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
    except Exception as exc:
        await session.rollback()
        raise UnexpectedError(f"An error occurred:\n{str(exc)}.") from exc
