from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Sequence
from db.models import BaseModel


class BaseCRUD:
    """
    Base class for CRUD operations for different models. 
    Override '_model' to use with specific model.
    """
    _model: type[BaseModel]
    
    @classmethod
    async def create(cls, session: AsyncSession, **kwargs):
        """
        Create an entry in the database.
        """
        instance = cls._model(**kwargs)
        session.add(instance=instance)
        await session.commit()
        return instance
    
    @classmethod
    async def get_all(cls, session: AsyncSession) -> Sequence[BaseModel]:
        query = select(cls._model)
        result = await session.execute(query)
        
        # extract as model's objects
        entries = result.scalars().all()
        return entries
        
        