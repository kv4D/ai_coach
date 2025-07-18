from typing import Self
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db.base_model import BaseModel
from .base import BaseCRUD
from db.models import UserModel, ActivityLevelModel


class UserCRUD(BaseCRUD[UserModel]):
    _model = UserModel

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
        return entry
