from aiogram.fsm.state import StatesGroup, State


class CreateProfile(StatesGroup):
    sending_gender = State()
    sending_age = State()
    sending_height = State()
    sending_weight = State()
    sending_goal = State()
    sending_activity_level = State()
    