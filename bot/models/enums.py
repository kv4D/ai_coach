from enum import Enum


class Gender(str, Enum):
    MALE = ['мужской',
            'муж',
            'мужчина']
    FEMALE = ['женский',
              'жен',
              'женщина']