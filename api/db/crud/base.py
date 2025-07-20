from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel as PydanticModel
from typing import Generic, TypeVar, Iterable
from db.models.base_model import BaseModel

# Type parameter for BaseModel children
TDBModel = TypeVar("TDBModel", bound=BaseModel)

class BaseCRUD(Generic[TDBModel]):
    """
    Base class for CRUD operations for different models. 
    Override '_model' to use with specific model.
    """
    _model: type[TDBModel]
    
    @classmethod
    async def create(cls, data: PydanticModel, session: AsyncSession) -> TDBModel:
        """Create a model entry in the database.

        Args:
            session (AsyncSession): asynchronous database session

        Returns:
            TDBModel: created model instance
        """
        data_dict = data.model_dump(exclude_unset=True)
        instance = cls._model(**data_dict)
        session.add(instance=instance)

        await session.flush()
        return instance

    @classmethod
    async def get_all(cls, session: AsyncSession) -> Iterable[TDBModel]:
        """Get all model entries in the database.

        Args:
            session (AsyncSession): asynchronous database session

        Returns:
            Iterable[TDBModel]: list of entries
        """
        query = select(cls._model).filter_by()
        result = await session.execute(query)
        # extract as model's objects
        entries = result.scalars().all()

        return entries

    @classmethod
    async def get_by_id(cls, id: int, session: AsyncSession) -> None | TDBModel:
        """Get a model entry by id.

        Args:
            id (int): entry's id
            session (AsyncSession): asynchronous database session

        Returns:
            None | TDBModel: entry or None
        """
        query = select(cls._model).filter_by(id=id)
        result = await session.execute(query)
        # there can be only one entry or none
        entry = result.scalar_one_or_none()

        return entry
