from pydantic import BaseModel, Field, field_validator
from .activity_level import ActivityLevel
from .enums import GenderEnum


class User(BaseModel):
    id: int
    age: int = Field(description="Возраст (полных лет)",
                     title="Возраст")
    gender: str = Field(description="Пол из доступных в системе",
                        title="Пол")
    weight_kg: float = Field(description="Вес в килограммах",
                             title="Вес (кг)")
    height_cm: float = Field(description="Рост в сантиметрах",
                             title="Рост (см)")
    activity_level: int
    goal: str = Field(description="Цель тренировок",
                      title="Цель тренировок")

    @field_validator('age', mode='before')
    @classmethod
    def validate_age(cls, age: str | int | None) -> int:
        try:
            if age is None:
                raise ValueError
            if isinstance(age, str):
                age = int(age)
            if age >= 100 or age <= 16:
                raise ValueError
            return age
        except ValueError as exc:
            raise ValueError("Возраст должен быть числом от 16 до 100") from exc

    @field_validator('gender', mode='before')
    @classmethod
    def validate_gender(cls, gender: str | None) -> str:
        try:
            if gender is None:
                raise ValueError
            gender = gender.lower()
            for gender_type in GenderEnum:
                # use stated gender type anyway
                if gender == gender_type.value or gender_type.name.lower() == gender:
                    return gender_type.name.lower()
            raise ValueError   
        except ValueError as exc:
            raise ValueError("Такого пола нет") from exc

    @field_validator('weight_kg', mode='before')
    @classmethod
    def validate_weight(cls, weight: str | float | None) -> float:
        try:
            if weight is None:
                raise ValueError
            if isinstance(weight, str):
                weight = float(weight.replace(',','.'))
            if weight < 30 or weight > 300:
                raise ValueError
            return weight
        except ValueError as exc:
            raise ValueError("Вес должен быть числом от 30 до 300") from exc

    @field_validator('height_cm', mode='before')
    @classmethod
    def validate_height(cls, height: str | float | None) -> float:
        try:
            if height is None:
                raise ValueError
            if isinstance(height, str):
                height = float(height.replace(',','.'))
            if height < 100 or height > 250:
                raise ValueError
            return height
        except ValueError as exc:
            raise ValueError("Рост должен быть числом от 100 до 250") from exc

    @classmethod
    def get_display_name(cls, field_name: str) -> str:
        """
        Get field's display name.\n
        Extracts 'title' parameter of a field.
        """
        field_info = cls.model_fields.get(field_name)
        if field_info and hasattr(field_info, 'title') and field_info.title:
            return field_info.title
        return field_name
