from aiogram.fsm.state import StatesGroup, State


class Profile(StatesGroup):
    viewing_profile = State()