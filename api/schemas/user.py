from typing import Optional
from pydantic import BaseModel, ConfigDict, \
    field_validator, Field
from schemas.activity_level import ActivityLevel
from schemas.training_plan import TrainingPlan


class UserValidationMixin:
    @field_validator('gender')
    @classmethod
    def check_gender(cls, gender_str: str) -> str:
        gender_str = gender_str.lower()
        possible_strings = ('male', 'female')
        if gender_str not in possible_strings:
            raise ValueError("Gender is either 'male' or 'female'")
        return gender_str

class User(BaseModel):
    """
    User model, contains physical data about a user.
    Uses metric system for fields (kilograms, centimeters, etc).
    """
    id: int = Field(frozen=True)
    username: str = Field(default='Anon')
    age: int = Field(default=18, gt=0, lt=100)
    weight_kg: float = Field(default=70, gt=0.0, lt=500.0)
    height_cm: float = Field(default=170, gt=60.0, lt= 250.0)
    gender: str
    activity_level: ActivityLevel
    training_plan: TrainingPlan
    
    model_config = ConfigDict(from_attributes=True)

class UserInput(BaseModel, UserValidationMixin):
    """
    User model for database input.
    Use to create database entries.
    """
    id: int = Field(frozen=True)
    username: str = Field(default='Anon')
    age: int = Field(gt=0, lt=100)
    weight_kg: float = Field(default=70, gt=0.0, lt=500.0)
    height_cm: float = Field(default=170, gt=60.0, lt= 250.0)
    gender: str
    activity_level_id: int

class UserUpdate(BaseModel, UserValidationMixin):
    """
    User model for database update.
    Use to update database entries.
    """
    username: Optional[str] = Field(default=None)
    age: Optional[int] = Field(default=None, gt=0, lt=100)
    weight_kg: Optional[float] = Field(default=None, gt=0.0, lt=500.0)
    height_cm: Optional[float] = Field(default=None, gt=60.0, lt= 250.0)
    gender: Optional[str] = None
