from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from aiogram.utils.chat_action import ChatActionSender
from api.client import APIClient
from keyboards.profile import get_profile_kb
from states.main import Main
from states.profile import Profile


router = Router()


@router.message(Command('profile'), Main.main_menu)
async def handle_profile_command(message: Message, 
                                 bot: Bot, 
                                 state: FSMContext,
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