from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from models.user import User
from filters.user import UserDataCallbackFactory


def get_profile_kb():
    builder = InlineKeyboardBuilder()
    fields = list(User.model_fields.keys())
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
