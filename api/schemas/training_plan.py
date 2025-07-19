from pydantic import BaseModel, ConfigDict, Field, field_validator


class TrainingPlan(BaseModel):
    """
    Training plan model.
    Used to contain training plan for a user for
    every day of the week.
    """
    id: int = Field(frozen=True)
    user_id: int
    plan_description: str

    model_config = ConfigDict(from_attributes=True)
