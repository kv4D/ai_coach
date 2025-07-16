from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from . base_model import BaseModel


class ActivityLevel(BaseModel):
    __tablename__ = 'activity_labels'
    
    description: Mapped[str]
    name: Mapped[str]


class User(BaseModel):
    __tablename__ = 'users'
    
    username: Mapped[str]
    age: Mapped[int]
    weight: Mapped[float]
    height: Mapped[float]
    gender: Mapped[str] # maybe be more strict?
    goal: Mapped[str | None]
    # later on create table with activity levels
    # or maybe enums?
    activity_level: Mapped[int]


class TrainingPlan(BaseModel):
    __tablename__ = 'training_plans'
    
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    # by days or in one string?