"""Base model of the API database."""
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs


class BaseDatabaseModel(AsyncAttrs, DeclarativeBase):
    """
    Base abstract database model.

    All of the models must inherit this model.
    """
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), 
                                                 onupdate=func.now())