"""User validation functions."""
from service.api import get_activity_levels


def validate_age(age_input: str | None) -> int:
    try:
        if age_input is None:
            raise ValueError
        age = int(age_input)
        if age >= 100 or age <= 16:
            raise ValueError
        return age
    except ValueError as exc:
        raise ValueError("Возраст должен быть числом от 16 до 100") from exc

def validate_gender(gender_input: str | None) -> str:
    genders = {
        "муж": "male",
        "жен": "female"
    }
    try:
        if gender_input is None:
            raise ValueError
        gender = gender_input.lower()[:3]
        if gender not in genders.keys():
            raise ValueError
        return genders[gender]
    except ValueError as exc:
        raise ValueError("Такого пола нет\nВыберите ваш пол c помощью кнопок, пожалуйста") from exc

def validate_height(height_input: str | None) -> float:
    try:
        if height_input is None:
            raise ValueError
        height = float(height_input.replace(',','.'))
        if height <= 100 or height >= 250:
            raise ValueError
        return height
    except ValueError as exc:
        raise ValueError("Рост должен быть числом от 100 до 250") from exc

def validate_weight(weight_input: str | None) -> float:
    try:
        if weight_input is None:
            raise ValueError
        weight = float(weight_input.replace(',','.'))
        if weight <= 20 and weight >= 300:
            raise ValueError
        return weight
    except ValueError as exc:
        raise ValueError("Вес должен быть числом от 20 до 300") from exc

def validate_activity_level(activity_level_input: str | None) -> int:
    try:
        activity_levels = get_activity_levels()
        if activity_level_input is None:
            raise ValueError
        activity_level = int(activity_level_input)
        if activity_level not in activity_levels:
            raise ValueError
        return activity_level
    except ValueError as exc:
        raise ValueError("Такого уровня активности нет\n"
                         "Выберите ваш уровень активности c помощью кнопок, пожалуйста") from exc