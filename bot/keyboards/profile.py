"""Keyboards for the profile."""
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from models.user import User
from filters.user import UserDataCallbackFactory


def get_profile_kb() -> InlineKeyboardMarkup:
    """Creates inline keyboard, contains options
    for updating a profile.

    Uses User model fields and callback factory for
    automatization.
    """
    builder = InlineKeyboardBuilder()
    fields = list(User.model_fields.keys())
    # can't change ID
    fields.remove('id')
    for field in fields:
        builder.button(
            text=f"Изменить {User.get_display_name(field).lower()}",
            callback_data=UserDataCallbackFactory(field=field)
        )
    builder.adjust(2, repeat=True)
    keyboard = builder.as_markup(resize_keyboard=True,
                                 one_time_keyboard=True,
                                 input_field_placeholder="Нажми на кнопку для выбора")
    return keyboard
