from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from aiogram.utils.chat_action import ChatActionSender
from service.api import get_user, get_activity_level
from states.main import Main
from states.profile import Profile


router = Router()


@router.message(Command('profile'), Main.main_menu)
async def handle_profile_command(message: Message, bot: Bot, state: FSMContext):
    """
    Handle /profile command.

    Get user's info from API's database.
    Sends message with this data.
    Sets state to Profile, so user could manage his profile.
    """
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        user = await get_user(message.from_user.id)
        user_activity_level = await get_activity_level(user.activity_level)
        

    await message.answer('Ваш <b>профиль</b>')
    await message.answer(user.get_formatted_string() + '\n' + user_activity_level.get_formatted_string())
    await state.set_state(Profile.viewing_profile)