from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional
from .base_model import BaseModel


class UserModel(BaseModel):
    __tablename__ = 'users'
    
    username: Mapped[str]
    age: Mapped[int]
    weight: Mapped[float]
    height: Mapped[float]
    gender: Mapped[str] # TODO: maybe be more strict?
    goal: Mapped[Optional[str]]
    
    # connect to activity levels
    activity_level_id: Mapped[int] = mapped_column(ForeignKey('activity_levels.id'))
    activity_level: Mapped['ActivityLevelModel'] = relationship("ActivityLevelModel",
                                                                back_populates="users")
    
    # connect to training plan


class ActivityLevelModel(BaseModel):
    __tablename__ = 'activity_levels'
    
    description: Mapped[str]
    name: Mapped[str]
    level: Mapped[int]
    
    # connect to user
    users: Mapped[list['UserModel']] = relationship("UserModel",
                                                   back_populates="activity_level")


class TrainingPlanModel(BaseModel):
    __tablename__ = 'training_plans'
    
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    # by days or in one string?