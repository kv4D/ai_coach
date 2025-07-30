from aiogram.fsm.state import StatesGroup, State


class Profile(StatesGroup):
    changing_field = State()