from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from aiogram.utils.chat_action import ChatActionSender
from api.client import APIClient
from models.activity_level import ActivityLevel
from models.user import User
from filters.user import UserDataCallbackFactory
from service.activity_levels import get_activity_levels_description
from keyboards.profile import get_profile_kb
from keyboards.common import get_activity_level_kb, get_gender_kb
from states.main import Main
from states.profile import Profile


router = Router()


@router.message(Command('profile'), Main.main_menu)
async def handle_profile_command(message: Message, 
                                 bot: Bot,
                                 api_client: APIClient):
    """
    Handle /profile command.

    Get user's info from API's database.
    Sends message with this data.
    Sets state to Profile, so user could manage his profile.
    """
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        user = await api_client.get_user(message.from_user.id)
        user_activity_level = await api_client.get_activity_level(user.activity_level)

    await message.answer('Ваш <b>профиль</b>')
    await message.answer(user.get_formatted_string() + user_activity_level.get_formatted_string(),
                         reply_markup=get_profile_kb())


@router.callback_query(UserDataCallbackFactory.filter(F.field.contains("gender")), Main.main_menu)
async def callback_user_gender_update(callback: CallbackQuery,
                                      callback_data: UserDataCallbackFactory,
                                      state: FSMContext):
    field_to_update = callback_data.field

    await callback.message.answer('Выберите новое значение',
                                  reply_markup=get_gender_kb())

    await callback.answer()
    await state.set_state(Profile.changing_field)
    await state.update_data(field_to_update=field_to_update)


@router.callback_query(UserDataCallbackFactory.filter(F.field.contains("activity")), Main.main_menu)
async def callback_user_activity_update(callback: CallbackQuery,
                                        callback_data: UserDataCallbackFactory,
                                        state: FSMContext,
                                        api_client: APIClient):
    field_to_update = callback_data.field
    await callback.message.answer('Выберите новое значение')
    
    level_info = await get_activity_levels_description(api_client)
    await callback.message.answer(level_info,
                                  reply_markup=await get_activity_level_kb(api_client))

    await callback.answer()
    await state.set_state(Profile.changing_field)
    await state.update_data(field_to_update=field_to_update)


@router.callback_query(UserDataCallbackFactory.filter(), Main.main_menu)
async def callback_user_update(callback: CallbackQuery,
                               callback_data: UserDataCallbackFactory,
                               state: FSMContext):
    field_to_update = callback_data.field
    await callback.answer()
    await callback.message.answer('Введите новое значение')
    await state.set_state(Profile.changing_field)
    await state.update_data(field_to_update=field_to_update)


@router.message(F.text, Profile.changing_field)
async def process_new_field_value(message: Message,
                                  state: FSMContext,
                                  api_client: APIClient):
    try:
        field_to_update = await state.get_value('field_to_update')
        new_value = message.text
        if field_to_update == 'activity_level':
            validated_value = ActivityLevel.validate_level(new_value)
        else:
            validated_value = getattr(User, f"validate_{field_to_update}")(new_value)
        # updating value
        await message.answer(f"Изменения применены успешно")
        await state.set_state(Main.main_menu)
    except ValueError as e:
        await message.answer(str(e))
        return
