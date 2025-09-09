from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.utils.chat_action import ChatActionSender
from aiogram.fsm.context import FSMContext
from bot.api.client import APIClient
from bot.models.activity_level import ActivityLevel
from bot.models.user import User
from bot.filters.user import UserDataCallbackFactory
from bot.service.service import get_activity_levels_description
from bot.keyboards.common import get_activity_level_kb, get_gender_kb
from bot.keyboards.profile import get_profile_kb
from bot.keyboards.commands import set_cancel, set_menu
from bot.states.main import Main
from bot.states.profile import Profile


router = Router()


@router.message(Command('cancel'), Profile.changing_field)
async def cancel_changing_field(message: Message,
                                bot: Bot,
                                api_client: APIClient,
                                state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        user = await api_client.get_user(message.from_user.id)
        user_activity_level = await api_client.get_activity_level(user.activity_level)

    await message.answer('Ваш профиль 📋', reply_markup=ReplyKeyboardRemove())
    await message.answer(user.get_formatted_string() + user_activity_level.get_formatted_string(),
                         reply_markup=get_profile_kb())
    await set_menu(bot, chat_id=message.chat.id)
    await state.set_state(Main.main)


@router.callback_query(UserDataCallbackFactory.filter(F.field.contains("gender")), Main.main)
async def callback_user_gender_update(callback: CallbackQuery,
                                      callback_data: UserDataCallbackFactory,
                                      bot: Bot,
                                      state: FSMContext):
    """Handler on `gender` field of User.

    Provides gender keyboard.
    """
    field_to_update = callback_data.field

    await callback.message.answer('Выберите новое значение\nИспользуйте /cancel для отмены',
                                  reply_markup=get_gender_kb())
    await set_cancel(bot, callback.message.chat.id)
    await callback.answer()
    await state.set_state(Profile.changing_field)
    await state.update_data(field_to_update=field_to_update)


@router.callback_query(UserDataCallbackFactory.filter(F.field.contains("activity")), Main.main)
async def callback_user_activity_update(callback: CallbackQuery,
                                        callback_data: UserDataCallbackFactory,
                                        bot: Bot,
                                        state: FSMContext,
                                        api_client: APIClient):
    """Handler on `activity_level` field of User.

    Provides levels descriptions and keyboard to choose
    available options.
    """
    field_to_update = callback_data.field
    await callback.message.answer('Выберите новое значение\nИспользуйте /cancel для отмены')

    level_info = await get_activity_levels_description(api_client)
    await callback.message.answer(level_info,
                                  reply_markup=await get_activity_level_kb(api_client))
    await set_cancel(bot, callback.message.chat.id)
    await callback.answer()
    await state.set_state(Profile.changing_field)
    await state.update_data(field_to_update=field_to_update)


@router.callback_query(UserDataCallbackFactory.filter(), Main.main)
async def callback_user_update(callback: CallbackQuery,
                               callback_data: UserDataCallbackFactory,
                               bot: Bot,
                               state: FSMContext):
    """Handler on any other field of User."""
    field_to_update = callback_data.field
    await callback.answer()
    await callback.message.answer('Введите новое значение\nИспользуйте /cancel для отмены')
    await set_cancel(bot, callback.message.chat.id)
    await state.set_state(Profile.changing_field)
    await state.update_data(field_to_update=field_to_update)


@router.message(F.text, Profile.changing_field)
async def process_new_field_value(message: Message,
                                  state: FSMContext,
                                  bot: Bot,
                                  api_client: APIClient):
    """Handler on user input.

    Validates new value and updates user data.
    """
    field_to_update = await state.get_value('field_to_update')
    new_value = message.text

    if field_to_update == 'activity_level':
        validated_value = ActivityLevel.validate_level(new_value)
    else:
        validator = getattr(User, f"validate_{field_to_update}", None)
        validated_value = validator(new_value) if validator else new_value

    # updating value
    await api_client.update_user_field(message.from_user.id,
                                       field_to_update,
                                       validated_value)
    await message.answer("Изменения применены успешно")
    await set_menu(bot, chat_id=message.chat.id)
    await state.set_state(Main.main)
