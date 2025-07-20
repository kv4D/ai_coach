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

class TrainingPlanInput(BaseModel):
    """
    Training plan model for database input.
    Use to create database entries.
    """
    plan_description: str
    user_id: int

    model_config = ConfigDict(from_attributes=True)
    @field_validator('plan_description')
    @classmethod
    def check_plan_description(cls, text: str) -> str:
        days = [
            'понедельник',
            'вторник',
            'среда',
            'четверг',
            'пятница',
            'суббота',
            'воскресенье'
        ]
        
        missing = [day for day in days if day not in text.lower()]
        if missing:
            raise ValueError(f"Some days are not in the plan: {', '.join(missing)}")
        return text
