"""Handlers for the main state."""
from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.chat_action import ChatActionSender
from keyboards.profile import get_profile_kb
from api.client import APIClient
from bot.states.create_plan import CreatePlan
from states.main import Main


router = Router()


@router.message(Command('help'), Main.main)
async def handle_help_command(message: Message):
    """Handle /help command.

    Send help message about bot to a user.
    Including advices, commands description,
    menu navigation, etc.
    """
    await message.answer('Какое-то сообщение о помощи')

@router.message(Command('my_plan'), Main.main)
async def handle_my_plan_command(message: Message, bot: Bot, api_client: APIClient):
    """
    Handle /my_plan command.

    Send user's training plan from API's database.
    If there is none, tell about it to the user.
    """
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        training_plan = await api_client.get_user_training_plan(message.from_user.id)

    if training_plan is None:
        await message.answer('Вы еще не создавали план.\nИспользуйте команду /generate_plan!')
    else:
        await message.answer('Вот <b>ваш план</b>')
        await message.answer(training_plan)

@router.message(Command('generate_plan'), Main.main)
async def handle_generate_plan_command(message: Message, state: FSMContext):
    """
    Handle /generate_plan command.

    Set new state and ask the user to send message with extra data
    for plan generation.
    """
    await message.answer('Отлично, я буду использовать вашу информацию, указанную в профиле\n'
                         'Дополнительно вы можете рассказать больше для желаемого плана')
    await state.set_state(CreatePlan.sending_request)

@router.message(Command('profile'), Main.main)
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

@router.message(F.text, Main.main)
async def handle_user_request(message: Message,
                              bot: Bot,
                              api_client: APIClient):
    """
    Handle user request in the main state.

    When user sends some message to bot (not a command/button),
    it means, they want to chat with AI.
    
    Get user's message and send it to the API with their ID.    
    """
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        user_id = message.from_user.id
        request = message.text
        ai_response = await api_client.get_user_request_response(user_id, request)
    await message.answer(ai_response)