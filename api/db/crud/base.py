from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Sequence, TypeVar, Generic
from db.models import BaseModel

# Type parameter for BaseModel children
T = TypeVar("T", bound=BaseModel)

class BaseCRUD(Generic[T]):
    """
    Base class for CRUD operations for different models. 
    Override '_model' to use with specific model.
    """
    _model: type[T]
    
    @classmethod
    async def create(cls, session: AsyncSession, **kwargs):
        """
        Create an entry in the database.
        """
        instance = cls._model(**kwargs)
        session.add(instance=instance)
        await session.flush()
        return instance
    
    @classmethod
    async def get_all(cls, session: AsyncSession,  **filter_kwargs) -> Sequence[BaseModel]:
        # TODO: it is possible to replace filter_kwargs with Pydantic Model
        # filters won't apply if there are none
        query = select(cls._model).filter_by(**filter_kwargs)
        
        result = await session.execute(query)
        
        # extract as model's objects
        entries = result.scalars().all()
        return entries
    
    @classmethod
    async def get_by_id(cls, id: int, session: AsyncSession):
        query = select(cls._model).filter_by(id=id)
        result = await session.execute(query)
        
        # there can be only one entry or none
        entry = result.scalar_one_or_none()
        return entry
        