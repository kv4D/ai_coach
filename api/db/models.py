from sqlalchemy.orm import Mapped, mapped_column
from base_model import BaseModel


class ActivityLevel(BaseModel):
    pass


class User(BaseModel):
    id: Mapped[int] = mapped_column(primary_key=True,
                                    autoincrement=True)
    username: Mapped[str] = mapped_column()
    age: Mapped[int]
    weight: Mapped[float]
    height: Mapped[float]
    gender: Mapped[str]
    goal: Mapped[str | None]
    # later on create table with activity levels
    # or maybe enums?
    activity_level: Mapped[int]