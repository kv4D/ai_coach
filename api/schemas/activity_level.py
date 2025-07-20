from pydantic import BaseModel, ConfigDict, Field


class ActivityLevel(BaseModel):
    """
    Activity level model.
    """
    id: int = Field(description='Database ID')
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
