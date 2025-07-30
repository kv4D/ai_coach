from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from aiogram.utils.chat_action import ChatActionSender
from service.user import create_user
from service.activity_levels import get_activity_levels_description
from api.client import APIClient
from states.create_profile import CreateProfile
from states.main import Main
from keyboards.common import get_gender_kb, get_activity_level_kb
from keyboards.menu_buttons import set_main_menu
from models.user import User
from models.activity_level import ActivityLevel


router = Router()


@router.message(CommandStart(), StateFilter(None, Main.main_menu))
async def handle_start_command(message: Message, state: FSMContext, bot: Bot):
    """
    Handle /start command.
    User starts the bot by sending the /start command.
    Start collecting user's data.
    Begin with user's age.
    """
    await state.clear()
    await bot.delete_my_commands()
    await message.answer('Привет, я буду помогать вам!\nДавайте заполним информацию о вас',
                         reply_markup=ReplyKeyboardRemove())
    await message.answer('Введите ваш <b>возраст</b>')
    await state.set_state(CreateProfile.sending_age)


@router.message(F.text, CreateProfile.sending_age)
async def process_age(message: Message, state: FSMContext):
    """
    Process user's age.
    If everything is OK: try to get gender.
    """
    try:
        age = User.validate_age(message.text)
        await message.answer('Укажите ваш <b>пол</b>',
                             reply_markup=get_gender_kb())
        await state.update_data(age=age)
        await state.set_state(CreateProfile.sending_gender)
    except ValueError as e:
        await message.answer(str(e))


@router.message(F.text, CreateProfile.sending_gender)
async def process_gender(message: Message, state: FSMContext):
    """
    Process user's gender.
    If everything is OK: try to get height.
    """
    try:
        gender = User.validate_gender(message.text)
        await state.update_data(gender=gender)
        await message.answer('А теперь введите ваш <b>рост в сантиметрах</b>',
                            reply_markup=ReplyKeyboardRemove())
        await state.set_state(CreateProfile.sending_height)
    except ValueError as e:
        await message.answer(str(e))


@router.message(F.text, CreateProfile.sending_height)
async def process_height(message: Message, state: FSMContext):
    """
    Process user's height.
    If everything is OK: try to get weight.
    """
    try:
        height = User.validate_height(message.text)
        await message.answer('Укажите ваш <b>вес в килограммах</b>',
                            reply_markup=ReplyKeyboardRemove())
        await state.update_data(height_cm=height)
        await state.set_state(CreateProfile.sending_weight)
    except ValueError as e:
        await message.answer(str(e))


@router.message(F.text, CreateProfile.sending_weight)
async def process_weight(message: Message, 
                         state: FSMContext, 
                         bot: Bot, 
                         api_client: APIClient):
    """
    Process user's weight.
    If everything is OK: try to get activity level.
    """
    try:
        weight = User.validate_weight(message.text)
        async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
            levels_info = await get_activity_levels_description(api_client)

            await message.answer('Выберите ваш <b>уровень активности</b>',
                                reply_markup=ReplyKeyboardRemove())
            await message.answer(levels_info, 
                                reply_markup=await get_activity_level_kb(api_client))
            await state.update_data(weight_kg=weight)
            await state.set_state(CreateProfile.sending_activity_level)
    except ValueError as e:
        await message.answer(str(e))


@router.message(F.text, CreateProfile.sending_activity_level)
async def process_activity_level(message: Message, 
                                 state: FSMContext, 
                                 bot: Bot,
                                 api_client: APIClient):
    """
    Process user's activity level.
    If everything is OK: try to get user's goal.
    """
    try:
        activity_level = ActivityLevel.validate_level(message.text)
        await message.answer('Отлично, теперь расскажите о вашей <b>цели</b>: для чего вы занимаетесь,'
                            'чего хотите добиться и прочее. Это сделает мою помощь более полезной.\n\n'
                            'Если у вас нет цели, то можете так и написать', 
                            reply_markup=ReplyKeyboardRemove())
        await state.update_data(activity_level=activity_level)
        await state.set_state(CreateProfile.sending_goal)
    except ValueError as e:
        await message.answer(str(e),
                             reply_markup=await get_activity_level_kb(api_client))
    

@router.message(F.text, CreateProfile.sending_goal)
async def process_goal(message: Message, 
                       state: FSMContext, 
                       bot: Bot, 
                       api_client: APIClient):
    """
    Process user's goal.
    User has finished collecting all the data.
    Send this data to service.
    Clear the state, set 'main' state.
    """
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await state.update_data(goal=message.text)
        user_data = await state.get_data()
        user = User(**user_data, 
                    id=message.from_user.id)
        await create_user(user, api_client=api_client)
    
    await message.answer('Начало положено!\nМы собрали всю информацию и готовы к работе.'
                         '\n\nВоспользуйтесь меню\nСоветую для начала создать план тренировок',
                         reply_markup=ReplyKeyboardRemove())
    await state.clear()
    await set_main_menu(bot)
    await state.set_state(Main.main_menu)
