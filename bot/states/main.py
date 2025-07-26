from aiogram.fsm.state import StatesGroup, State


class Main(StatesGroup):
    main_menu = State()
    profile_menu = State()
    training_plan = State()