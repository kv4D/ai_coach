from pydantic import BaseModel, ConfigDict


class ActivityLevel(BaseModel):
    """Activity level model"""
    id: int
    description: str
    name: str
    level: int

    model_config = ConfigDict(from_attributes=True)