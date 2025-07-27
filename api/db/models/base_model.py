from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import func
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncAttrs


class BaseModel(AsyncAttrs, DeclarativeBase):
    """Base abstract database model"""
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), 
                                                 onupdate=func.now())