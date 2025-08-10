from aiogram.fsm.state import StatesGroup, State


class UseAI(StatesGroup):
    sending_request = State()
    generating_answer = State()