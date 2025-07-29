from enum import Enum


class EnumMixin(Enum):
    @classmethod
    def make_list(cls):
        return list(map(lambda c: c.value, cls))


class GenderEnum(str, EnumMixin):
    MALE = 'мужской'
    FEMALE = 'женский'


class ActivityLevelEnum(int, EnumMixin):
    LOW_ACTIVITY = 1
    LITTLE_ACTIVITY = 2
    MODERATE_ACTIVITY = 3
    HIGH_ACTIVITY = 4
