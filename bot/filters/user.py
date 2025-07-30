from aiogram.filters.callback_data import CallbackData


class UserDataCallbackFactory(CallbackData, prefix="update"):
    field: str