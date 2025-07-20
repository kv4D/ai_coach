from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional
from db.models.base_model import BaseModel


class UserModel(BaseModel):
    __tablename__ = 'users'
    
    username: Mapped[Optional[str]]
    age: Mapped[int]
    weight_kg: Mapped[float]
    height_cm: Mapped[float]
    gender: Mapped[str]
    goal: Mapped[Optional[str]]
    
    # connect to activity levels
    # one activity level per user
    activity_level_id: Mapped[int] = mapped_column(ForeignKey('activity_levels.id'))
    activity_level: Mapped['ActivityLevelModel'] = relationship("ActivityLevelModel",
                                                                back_populates="users",
                                                                lazy='joined')
    
    # connect to training plan
    # one plan per user
    training_plan: Mapped[Optional['TrainingPlanModel']] = relationship("TrainingPlanModel",
                                                              back_populates="user",
                                                              # one-to-one
                                                              uselist=False,
                                                              # load with user
                                                              lazy="joined") 


class ActivityLevelModel(BaseModel):
    __tablename__ = 'activity_levels'
    
    description: Mapped[str]
    name: Mapped[str]
    level: Mapped[int]
    
    # connect to user
    # multiple users for a level
    users: Mapped[list['UserModel']] = relationship("UserModel",
                                                   back_populates="activity_level")


class TrainingPlanModel(BaseModel):
    __tablename__ = 'training_plans'
    
    plan_description: Mapped[str]
    
    # connect to user
    # one user per plan
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["UserModel"] = relationship("UserModel",
                                             back_populates="training_plan",
                                             # one-to-one
                                             uselist=False,
                                             cascade="all, delete-orphan",
                                             single_parent=True)
