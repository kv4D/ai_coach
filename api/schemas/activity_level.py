"""Activity level Pydantic schemas."""
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class ActivityLevel(BaseModel):
    """
    Activity level model.
    """
    description: str = Field(description='About this activity level')
    name: str
    level: int = Field(ge=0,
                       description='Activity level number')

    model_config = ConfigDict(from_attributes=True)

class ActivityLevelInput(BaseModel):
    """
    Activity level model for input.
    Use to create database entries.
    """
    description: str = Field(description='About this activity level')
    name: str
    level: int = Field(ge=0,
                       description='Activity level number')

class ActivityLevelUpdate(BaseModel):
    """
    Activity level model for database update.
    Use to update database entries.
    """
    description: Optional[str] = Field(default=None,
                                       description='About this activity level')
    name: Optional[str] = None
    level: Optional[int] = Field(default=None,
                                 ge=0,
                                 description='Activity level number')
