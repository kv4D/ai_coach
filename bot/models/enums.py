from enum import Enum
from typing import Any


class EnumMixin(Enum):
    """Mixin for all defined `Enum` classes."""
    @classmethod
    def make_list(cls) -> list[Any]:
        """Turns `Enum` into list with values."""
        return list(map(lambda c: c.value, cls))


class GenderEnum(str, EnumMixin):
    """Available genders."""
    MALE = 'мужской'
    FEMALE = 'женский'


class ActivityLevelEnum(int, EnumMixin):
    """Available activity levels."""
    # TODO: make static, take from API OR delete this
    LOW_ACTIVITY = 1
    LITTLE_ACTIVITY = 2
    MODERATE_ACTIVITY = 3
    HIGH_ACTIVITY = 4
