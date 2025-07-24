from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.types.keyboard_button import KeyboardButton


def get_gender_kb():
    builder = ReplyKeyboardBuilder()
    builder.button(text='Мужской')
    builder.button(text='Женский')
    builder.adjust(2)
    keyboard = builder.as_markup(resize_keyboard=True, 
                                 one_time_keyboard=True,
                                 input_field_placeholder="Нажми на кнопку для выбора")
    return keyboard

def get_activity_level_kb():
    builder = ReplyKeyboardBuilder()
    # extract service data here
    levels = [1, 2, 3, 4, 5]
    for level in levels:
        builder.button(text=str(level))
    builder.adjust(len(levels))
    keyboard = builder.as_markup(resize_keyboard=True, 
                                 one_time_keyboard=True,
                                 input_field_placeholder="Нажми на кнопку для выбора")
    return keyboard
    