from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    """User model"""
    id: int
    username: str
    age: int
    weight: float
    height: float
    gender: str

    model_config = ConfigDict(from_attributes=True)