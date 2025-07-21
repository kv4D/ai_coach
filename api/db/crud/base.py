from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel as PydanticModel
from typing import Generic, TypeVar, Iterable
from exceptions import NotFoundError
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
            TDBModel: created model entry
        """
        data_dict = data.model_dump(exclude_unset=True)
        entry = cls._model(**data_dict)
        session.add(instance=entry)

        await session.flush()
        return entry

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
    async def get_by_id(cls, entry_id: int, session: AsyncSession) -> None | TDBModel:
        """Get a model entry by id.

        Args:
            id (int): entry's id
            session (AsyncSession): asynchronous database session

        Returns:
            None | TDBModel: entry or None
        """
        return await session.get(cls._model, entry_id)

    @classmethod
    async def update_by_id(cls, entry_id: int, update_data: PydanticModel, session: AsyncSession):
        update_data_dict = update_data.model_dump(exclude_unset=True)
        entry = await session.get(cls._model, entry_id)
        
        if entry is None:
            raise NotFoundError(
                f"There is no {cls._model.__name__.lower()} entry with such ID: {entry_id}.")
        
        for key, value in update_data_dict.items():
            setattr(entry, key, value)
        await session.flush()
        return entry

    @classmethod
    async def delete_by_id(cls, entry_id: int, session: AsyncSession):
        entry = await session.get(cls._model, entry_id)

        if entry is None:
            raise NotFoundError(
                f"There is no {cls._model.__name__.lower()} entry with such ID: {entry_id}.")

        await session.delete(entry)
        await session.flush()
        return entry