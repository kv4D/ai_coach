"""Handlers for the main state."""
from aiogram import Router, Bot, F
from aiogram.types import Message, ErrorEvent
from aiogram.filters import Command, ExceptionTypeFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.chat_action import ChatActionSender
from keyboards.profile import get_profile_kb
from api.client import APIClient
from states.use_ai import UseAI
from states.main import Main
from utils import get_command_descriptions


router = Router()

@router.error(ExceptionTypeFilter(ValueError), F.update.message.as_("message"))
async def handle_value_error(event: ErrorEvent, message: Message):
    """Process value error.
    
    Value error is raised when a user inputs
    wrong data during filling profile fields.
    
    Catches errors and sends messages to user.
    
    Value error message should be user-friendly for sending in
    chat.
    """
    await message.answer(f"Неверно введены данные ❌\n\n❗ {str(event.exception)} ❗")

@router.message(UseAI.generating_answer)
async def handle_message_during_generation(message: Message):
    """Handle message during generating AI answer.
    
    When bot is trying to get answer from the API,
    user still can send messages, but it can ruin
    the requests.
    
    So the bot will tell user to wait a little.
    """
    await message.answer("Пожалуйста, ожидайте ⌛")

@router.message(Command('help'), Main.main)
async def handle_help_command(message: Message, bot: Bot):
    """Handle /help command.

    Send help message about bot to a user.
    Including advices, commands description,
    menu navigation, etc.
    """
    help_message = "Этот бот поможет вам с вашими тренировками и предоставит советы по здоровому образу жизни 🏋️\n"
    help_message += "❗ Важно: бот не является специалистом ❗\n\n"
    help_message += f"🤖 Набор команд:\n{await get_command_descriptions(bot)}"
    help_message += """
Вот несколько советов при общении с ботом:
    <strong>📋 Заполните свой профиль</strong> - Бот будет брать информацию оттуда
    <strong>🎯 Будьте точны в своих запросах</strong> - Тогда и ответ будет точным
    <strong>❔ Добавляйте детали, уточнения и пожелания</strong> - Бот может чего-то не знать о вас
    <strong>🏃 Используйте бота по назначению</strong> - Бот работает только в пределах своей области
    """
    await message.answer(help_message)

@router.message(Command('my_plan'), Main.main)
async def handle_my_plan_command(message: Message, bot: Bot, api_client: APIClient):
    """Handle /my_plan command.

    Send user's training plan from API's database.
    If there is none, tell about it to the user.
    """
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        training_plan = await api_client.get_user_training_plan(message.from_user.id)

    if training_plan is None:
        await message.answer('Вы еще не создавали план 🤔\n\nИспользуйте команду /generate_plan')
    else:
        await message.answer('Вот ваш план 💪')
        await message.answer(training_plan)

@router.message(Command('generate_plan'), Main.main)
async def handle_generate_plan_command(message: Message, state: FSMContext):
    """Handle /generate_plan command.

    Set new state and ask the user to send message with extra data
    for plan generation.
    """
    await message.answer('Отлично, я буду использовать вашу информацию, указанную в профиле 👍\n\n'
                         'Дополнительно вы можете рассказать больше для желаемого плана ✍️')
    await state.set_state(UseAI.sending_request)

@router.message(Command('profile'), Main.main)
async def handle_profile_command(message: Message, 
                                 bot: Bot,
                                 api_client: APIClient):
    """Handle /profile command.

    Get user's info from API's database.
    Sends message with this data.
    Sets state to Profile, so user could manage his profile.
    """
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        user = await api_client.get_user(message.from_user.id)
        user_activity_level = await api_client.get_activity_level(user.activity_level)

    await message.answer('Ваш профиль 📋')
    await message.answer(user.get_formatted_string() + user_activity_level.get_formatted_string(),
                         reply_markup=get_profile_kb())

@router.message(F.text, Main.main)
async def handle_user_request(message: Message,
                              bot: Bot,
                              api_client: APIClient,
                              state: FSMContext):
    """Handle user request in the main state.

    When user sends some message to bot (not a command/button),
    it means, they want to chat with AI.
    
    Get user's message and send it to the API with their ID.    
    """
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        user_id = message.from_user.id
        request = message.text
        await state.set_state(UseAI.generating_answer)
        ai_response = await api_client.get_user_request_response(user_id, request)
    await message.answer(ai_response)
    await state.set_state(Main.main)

@router.message(~F.text)
async def handle_wrong_data_type(message: Message):
    """Handle not text message.
    
    They are not supported by this bot, so we 
    need to tell about that to users.
    """
    await message.answer("Я могу работать только с текстом 📜")
