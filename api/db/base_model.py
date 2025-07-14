from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import func
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from config import config


class BaseModel(AsyncAttrs, DeclarativeBase):
    """Base abstract database model"""
    __abstract__ = True
    
    id: Mapped[int] = mapped_column(primary_key=True, 
                                    autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), 
                                                 onupdate=func.now())