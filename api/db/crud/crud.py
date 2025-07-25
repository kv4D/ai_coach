from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel as PydanticModel
from schemas.training_plan import TrainingPlanUpdate
from exceptions import AlreadyExistError, NotFoundError
from .base import BaseCRUD
from db.models.models import TrainingPlanModel, UserModel, ActivityLevelModel


class UserCRUD(BaseCRUD[UserModel]):
    _model = UserModel


class TrainingPlanCRUD(BaseCRUD[TrainingPlanModel]):
    _model = TrainingPlanModel
    
    @classmethod
    async def get_by_user_id(cls, user_id: int, session: AsyncSession) -> None | TrainingPlanModel:
        """Get the training plan for a user by their id.

        Args:
            user_id (int): user id in database
            session (AsyncSession): asynchronous database session

        Returns:
            None | TrainingPlanModel: entry or None
        """
        query = select(cls._model).filter_by(user_id=user_id)
        result = await session.execute(query)
        
        # there can be only one entry or none
        entry = result.scalar_one_or_none()
        return entry
    
    @classmethod
    async def create_for_user(cls, 
                              user_id: int, 
                              plan_data: PydanticModel, 
                              session: AsyncSession) -> TrainingPlanModel:
        """Create a training plan for the user by their id.

        Args:
            user_id (int): user id in database
            session (AsyncSession): asynchronous database session

        Returns:
            None | TrainingPlanModel: entry or None
        """
        # check for existing plan
        result = await session.execute(select(cls._model).filter_by(user_id=user_id))
        exists = result.scalar_one_or_none()
        if exists:
            raise AlreadyExistError(f"User with ID={user_id} already has a plan.")
        
        plan_data_dict = plan_data.model_dump()
        instance = cls._model(**plan_data_dict, user_id=user_id)
        session.add(instance=instance)
        await session.flush()
        return instance

    @classmethod
    async def update_by_user_id(cls,
                                user_id: int,
                                plan_data: TrainingPlanUpdate,
                                session: AsyncSession):
        update_data_dict = plan_data.model_dump(exclude_unset=True)
        
        query = select(cls._model).filter_by(user_id=user_id)
        result = await session.execute(query)
        
        # there can be only one entry or none
        entry = result.scalar_one_or_none()
        
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
                                session: AsyncSession):
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
    _model = ActivityLevelModel
    
    @classmethod
    async def get_by_level(cls, level: int, session: AsyncSession) -> None | ActivityLevelModel:
        """Get the activity level info according to its level.

        Args:
            level: activity level
            session (AsyncSession): asynchronous database session

        Returns:
            None | TDBModel: entry or None
        """
        query = select(cls._model).filter_by(level=level)
        result = await session.execute(query)
        
        # there can be only one entry or none
        entry = result.scalar_one_or_none()
        
        if entry is None:
            raise NotFoundError(f"There is no level with such number: {level}.")
        
        return entry
