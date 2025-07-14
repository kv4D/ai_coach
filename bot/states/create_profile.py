from aiogram.fsm.state import StatesGroup, State


class CreateProfile(StatesGroup):
    sending_name = State()
    sending_age = State()
    sending_height = State()
    sending_weight = State()
    choosing_gender = State()
    choosing_activity_level = State()
    