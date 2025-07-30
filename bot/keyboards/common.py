from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types.keyboard_button import KeyboardButton
from models.enums import GenderEnum

from api.client import APIClient


def get_gender_kb():
    builder = ReplyKeyboardBuilder()
    for gender in GenderEnum:
        builder.button(text=f"{gender.value.capitalize()}")
    builder.adjust(len(GenderEnum))
    keyboard = builder.as_markup(resize_keyboard=True, 
                                 one_time_keyboard=True,
                                 input_field_placeholder="Нажмите на кнопку для выбора")
    return keyboard

async def get_activity_level_kb(api_client: APIClient):
    builder = ReplyKeyboardBuilder()
    levels = await api_client.get_activity_levels()
    for level in levels:
        builder.button(text=str(level.level))
    builder.adjust(len(levels))
    keyboard = builder.as_markup(resize_keyboard=True, 
                                 one_time_keyboard=True,
                                 input_field_placeholder="Нажмите на кнопку для выбора")
    return keyboard
    