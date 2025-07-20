from pydantic import BaseModel, ConfigDict, Field


class ActivityLevel(BaseModel):
    """
    Activity level model.
    Used to define different activity levels of users.
    """
    id: int = Field(frozen=True)
    description: str
    name: str
    level: int = Field(ge=0)

    model_config = ConfigDict(from_attributes=True)
