from pydantic import BaseModel, field_validator, Field
from .enums import ActivityLevelEnum


class ActivityLevel(BaseModel):
    level: int = Field(description="Относительный уровень активности",
                       title="Уровень активности")
    description: str = Field(description="Описание уровня активности с подробностями",
                             title="Описание")
    name: str = Field(description="Название",
                      title="Название")

    @field_validator("level", mode="before")
    @classmethod
    def validate_level(cls, level: str | int | None) -> int:
        try:
            possible_levels = ActivityLevelEnum.make_list()
            if level is None:
                raise ValueError
            level = int(level)
            if level not in possible_levels:
                raise ValueError
            return level
        except ValueError as exc:
            raise ValueError(f"Такого уровня активности нет: {level}") from exc

    def get_formatted_string(self) -> str:
        """
        Get user-friendly string with all data from
        ActivityLevel instance.
        """
        output = ''
        output += f"<b>Уровень активности {self.level}</b>:\n<b>{self.name}</b>\n{self.description}\n"
        return output
