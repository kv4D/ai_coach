"""Base Database Access Object for CRUD operations."""
from typing import Generic, TypeVar, Iterable
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from exceptions import NotFoundError
from db.models.base_model import BaseDatabaseModel


# type parameter for BaseModel children
TDBModel = TypeVar("TDBModel", bound=BaseDatabaseModel)

class BaseCRUD(Generic[TDBModel]):
    """
    Base DAO class for CRUD operations for any model.

    Override '_model' to use with some specific model.
    """
    _model: type[TDBModel]

    @classmethod
    async def create(cls, data: BaseModel, session: AsyncSession):
        """Create an entry in the database.

        Args:
            data (`pydantic.BaseModel`): pydantic model instance with required data
            session (`AsyncSession`): an asynchronous database session
        """
        data_dict = data.model_dump(exclude_unset=True)
        entry = cls._model(**data_dict)
        session.add(instance=entry)
        await session.flush()

    @classmethod
    async def get_all(cls, session: AsyncSession) -> Iterable[TDBModel] | None:
        """Get all model's entries in the database.

        Args:
            session (`AsyncSession`): an asynchronous database session
        """
        query = select(cls._model).filter_by()
        result = await session.execute(query)
        entries = result.scalars().all()
        return entries

    @classmethod
    async def get_by_id(cls, entry_id: int, session: AsyncSession) -> None | TDBModel:
        """Get a model entry by the ID/primary key.

        Args:
            entry_id (`int`): entry's ID OR primary key
            session (`AsyncSession`): an asynchronous database session
        """
        return await session.get(cls._model, entry_id)

    @classmethod
    async def update_by_id(cls,
                           entry_id: int,
                           update_data: BaseModel,
                           session: AsyncSession):
        """Update an entry with new data by its ID/primary key.

        Args:
            entry_id (`int`): entry's ID OR primary key
            update_data (`pydantic.BaseModel`): a pydantic model instance with new data
            session (`AsyncSession`): an asynchronous database session
        """
        update_data_dict = update_data.model_dump(exclude_unset=True)
        entry = await session.get(cls._model, entry_id)

        if entry is None:
            raise NotFoundError(
                f"There is no {cls._model.__name__.lower()} entry with such ID: {entry_id}.")

        for key, value in update_data_dict.items():
            setattr(entry, key, value)
        await session.flush()

    @classmethod
    async def delete_by_id(cls, entry_id: int, session: AsyncSession) -> TDBModel:
        """Delete an entry by its ID/primary key.

        Args:
            entry_id (`int`): entry's ID OR primary key
            session (`AsyncSession`): an asynchronous database session
        """
        entry = await session.get(cls._model, entry_id)

        if entry is None:
            raise NotFoundError(
                f"There is no {cls._model.__name__.lower()} entry with such ID: {entry_id}.")

        await session.delete(entry)
        await session.flush()
        return entry
