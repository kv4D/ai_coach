from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils.i18n import gettext as _
from aiogram.utils.chat_action import ChatActionSender
from api.client import get_user_training_plan
from states.main import Main


router = Router()


@router.message(Command('help'), Main.main_menu)
async def handle_help_command(message: Message):
    """Handle /help command.

    Send help message about bot to a user.
    Including advices, commands description,
    menu navigation, etc.
    """
    await message.answer('Какое-то сообщение о помощи')

@router.message(Command('my_plan'), Main.main_menu)
async def handle_my_plan_command(message: Message, bot: Bot):
    """
    Handle /my_plan command.

    Send user's training plan from API's database.
    If there is none, tell about it to the user.
    """
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        training_plan = await get_user_training_plan(message.from_user.id)

    if training_plan is None:
        await message.answer('Вы еще не создавали план.\nИспользуйте команду /generate_plan!')
    else:
        await message.answer('Вот <b>ваш план</b>')
        await message.answer(training_plan)

@router.message(Command('generate_plan'), Main.main_menu)
async def handle_generate_plan_command(message: Message, bot: Bot):
    """
    Handle /generate_plan command.

    Uses API to create user's plan with his data.
    Gives feedback upon creation.
    """
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await message.answer('Генерирую план, ожидайте')
        # create user plan here
        training_plan = 'some training plan'
    await message.answer('Вот ваш план')
    await message.answer(training_plan)
