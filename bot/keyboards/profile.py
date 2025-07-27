from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.inline_keyboard_button import InlineKeyboardButton

from service.api import get_activity_levels


def get_profile_kb():
    builder = InlineKeyboardBuilder()
    keyboard = builder.as_markup(resize_keyboard=True,
                                 one_time_keyboard=True,
                                 input_field_placeholder="Нажми на кнопку для выбора")
    return keyboard
