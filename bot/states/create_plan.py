from aiogram.fsm.state import StatesGroup, State


class CreatePlan(StatesGroup):
    sending_request = State()