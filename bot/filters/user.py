"""Custom bot filters."""
from aiogram.filters.callback_data import CallbackData


class UserDataCallbackFactory(CallbackData, prefix="update"):
    """Callback factory for updating User fields."""
    field: str