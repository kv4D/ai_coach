"""Custom bot filters on users."""
from aiogram.filters.callback_data import CallbackData
from aiogram.filters import BaseFilter
from aiogram.types import Message
from api.client import APIClient
from service.service import is_user_exist

class UserExistsFilter(BaseFilter):
    """Filter to check if user is present in the database."""
    async def __call__(self, message: Message, api_client: APIClient) -> bool:
        return await is_user_exist(message.from_user.id, api_client)

class UserDataCallbackFactory(CallbackData, prefix="update"):
    """Callback factory for updating User fields."""
    field: str
