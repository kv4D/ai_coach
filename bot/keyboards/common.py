"""Keyboard that appear in several places in the bot."""
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from models.enums import GenderEnum
from api.client import APIClient


def get_gender_kb() -> ReplyKeyboardMarkup: 
    """Creates keyboard for choosing user gender.
    
    Gender options are stated in `GenderEnum`.
    """
    builder = ReplyKeyboardBuilder()
    for gender in GenderEnum:
        builder.button(text=f"{gender.value.capitalize()}")
    builder.adjust(len(GenderEnum))
    keyboard = builder.as_markup(resize_keyboard=True,
                                 input_field_placeholder="Нажмите на кнопку для выбора")
    return keyboard

async def get_activity_level_kb(api_client: APIClient) -> ReplyKeyboardMarkup:
    """Creates keyboard for choosing user activity level.

    The API provides level options.

    Args:
        api_client (`APIClient`): an API client to make request     
    """
    builder = ReplyKeyboardBuilder()
    levels = await api_client.get_activity_levels()
    for level in levels:
        builder.button(text=str(level.level))
    builder.adjust(len(levels))
    keyboard = builder.as_markup(resize_keyboard=True,
                                 input_field_placeholder="Нажмите на кнопку для выбора")
    return keyboard
