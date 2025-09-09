"""
Database Access Objects for CRUD operations.

Created for all models in the database.
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from api.exceptions import NotFoundError
from api.schemas.training_plan import TrainingPlanUpdate
from .base_crud import BaseCRUD
from .models import TrainingPlanModel, UserModel, ActivityLevelModel


class UserCRUD(BaseCRUD[UserModel]):
    """DAO class for CRUD operations with UserModel."""
    _model = UserModel

    @classmethod
    async def create(cls, data: BaseModel, session: AsyncSession) -> UserModel:
        entry = await super().create(data, session=session)
        # need to additionally refresh database relations
        await session.refresh(entry, attribute_names=["training_plan"])
        return entry

class TrainingPlanCRUD(BaseCRUD[TrainingPlanModel]):
    """
    DAO class for CRUD operations with TrainingPlanModel.
    """
    _model = TrainingPlanModel

    @classmethod
    async def get_by_user_id(cls,
                             user_id: int,
                             session: AsyncSession) -> None | TrainingPlanModel:
        """Get a training plan for a user using their ID.

        Args:
            user_id (`int`)
            session (`AsyncSession`): an asynchronous database session
        """
        query = select(cls._model).filter_by(user_id=user_id)
        result = await session.execute(query)
        # there can be only one entry or none
        entry = result.scalar_one_or_none()
        return entry

    @classmethod
    async def create_for_user(cls,
                              user_id: int,
                              plan_data: BaseModel,
                              session: AsyncSession):
        """Create a training plan for the user by their id.

        Args:
            user_id (`int`)
            session (`AsyncSession`): an asynchronous database session
        """
        plan_data_dict = plan_data.model_dump(exclude_unset=True)
        entry = cls._model(**plan_data_dict, user_id=user_id)
        session.add(instance=entry)
        await session.flush()
        return entry

    @classmethod
    async def update_by_user_id(cls,
                                user_id: int,
                                plan_data: TrainingPlanUpdate,
                                session: AsyncSession) -> TrainingPlanModel:
        """Update a training plan with new data by the user_id field.

        Args:
            user_id (`int`)
            plan_data (`TrainingPlanUpdate`): a pydantic model instance with new data
            session (`AsyncSession`): an asynchronous database session
        """
        update_data_dict = plan_data.model_dump(exclude_unset=True)
        # there can be only one entry or none
        query = select(cls._model).filter_by(user_id=user_id)
        entry = await session.execute(query)
        entry = entry.scalar_one_or_none()

        if entry is None:
            raise NotFoundError(
                f"There is no plan for user with such ID: {user_id}.")

        for key, value in update_data_dict.items():
            setattr(entry, key, value)
        await session.flush()
        return entry

    @classmethod
    async def delete_by_user_id(cls,
                                user_id: int,
                                session: AsyncSession) -> TrainingPlanModel:
        """Delete an entry by the user_id field.

        Args:
            user_id (`int`)
            session (`AsyncSession`): an asynchronous database session
        """
        query = select(cls._model).filter_by(user_id=user_id)
        entry = await session.execute(query)
        entry = entry.scalar_one_or_none()

        if entry is None:
            raise NotFoundError(
                f"There is no plan for user with such ID: {user_id}.")

        await session.delete(entry)
        await session.flush()
        return entry


class ActivityLevelCRUD(BaseCRUD[ActivityLevelModel]):
    """
    DAO class for CRUD operations with ActivityLevelModel.
    """
    _model = ActivityLevelModel
