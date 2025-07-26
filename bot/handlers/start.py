from aiogram import Router, F, Bot
from aiogram.methods import delete_my_commands
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from aiogram.utils.formatting import as_marked_list
from aiogram.utils.chat_action import ChatActionSender
from service.api import create_user, get_activity_levels, get_activity_levels_descriptions
from states.create_profile import CreateProfile
from states.main import Main
from validators.user import validate_activity_level, validate_age, \
    validate_gender, validate_height, validate_weight
from keyboards.start import get_gender_kb, get_activity_level_kb
from keyboards.menu_buttons import set_main_menu


router = Router()


@router.message(CommandStart())
async def handle_start_command(message: Message, state: FSMContext, bot: Bot):
    """Handle /start command.
    User starts the bot by sending the /start command.
    Start collecting user's data.

    Args:
        message (Message): Message object
        state (FSMContext): FSMContext object
        bot (Bot): Bot object
    """
    await state.clear()
    await bot.delete_my_commands()
    await message.answer('Привет, я буду помогать тебе. Напиши свое <b>имя</b>',
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(CreateProfile.sending_name)


@router.message(F.text, CreateProfile.sending_name)
async def process_name(message: Message, state: FSMContext):
    """Process user's name.

    Args:
        message (Message): Message object
        state (FSMContext): FSMContext object
    """
    await state.update_data(username=message.text)
    await message.answer('Теперь введи свой <b>возраст</b>',
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(CreateProfile.sending_age)


@router.message(F.text, CreateProfile.sending_age)
async def process_age(message: Message, state: FSMContext):
    """Process user's age.

    Args:
        message (Message): Message object
        state (FSMContext): FSMContext object
    """
    try:
        age = validate_age(message.text)
        # some other checks
        await message.answer('Укажи свой <b>пол</b>', 
                            reply_markup=get_gender_kb())
        await state.update_data(age=age)
        await state.set_state(CreateProfile.sending_gender)
    except ValueError as e:
        await message.answer(str(e))


@router.message(F.text, CreateProfile.sending_gender)
async def process_gender(message: Message, state: FSMContext):
    """Process user's gender.

    Args:
        message (Message): Message object
        state (FSMContext): FSMContext object
    """
    try:
        gender = validate_gender(message.text)
        await state.update_data(gender=gender)
        await message.answer('А теперь введи свой <b>рост в сантиметрах</b>',
                            reply_markup=ReplyKeyboardRemove())
        await state.set_state(CreateProfile.sending_height)
    except ValueError as e:
        await message.answer(str(e))


@router.message(F.text, CreateProfile.sending_height)
async def process_height(message: Message, state: FSMContext):
    """Process user's height.

    Args:
        message (Message): Message object
        state (FSMContext): FSMContext object
    """
    try:
        height = validate_height(message.text)
        # some checks
        await message.answer('Укажи свой <b>вес в килограммах</b>',
                            reply_markup=ReplyKeyboardRemove())
        await state.update_data(height_cm=height)
        await state.set_state(CreateProfile.sending_weight)
    except ValueError as e:
        await message.answer(str(e))


@router.message(F.text, CreateProfile.sending_weight)
async def process_weight(message: Message, state: FSMContext, bot: Bot):
    """Process user's weight.

    Args:
        message (Message): Message object
        state (FSMContext): FSMContext object
        bot (Bot): Bot object
    """
    try:
        weight = validate_weight(message.text)
        async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
            levels = await get_activity_levels()
            descriptions = await get_activity_levels_descriptions()
            levels_descriptions = [
                f"Уровень {level}:\n{descriptions[level]}\n\n" for level in levels
                ]

            await state.update_data(weight_kg=weight)
            
            content = as_marked_list(*levels_descriptions, marker="🏆 ") 
            await message.answer('Выбери свой <b>уровень активности</b>',
                                reply_markup=ReplyKeyboardRemove())
            await message.answer(**content.as_kwargs(), 
                                reply_markup=await get_activity_level_kb())
            await state.set_state(CreateProfile.sending_activity_level)
    except ValueError as e:
        await message.answer(str(e))


@router.message(F.text, CreateProfile.sending_activity_level)
async def process_activity_level(message: Message, state: FSMContext, bot: Bot):
    """Process user's activity level.

    Args:
        message (Message): Message object
        state (FSMContext): FSMContext object
        bot (Bot): Bot object
    """
    try:
        activity_level = await validate_activity_level(message.text)
        await message.answer('Отлично, теперь расскажи о своей <b>цели</b>: для чего ты занимаешься,'
                            'чего хочешь добиться и прочее. Это сделает мою помощь более полезной.\n\n'
                            'Если у тебя нет цели, то можешь так и написать', 
                            reply_markup=ReplyKeyboardRemove())
        await state.update_data(activity_level=activity_level)
        await state.set_state(CreateProfile.sending_goal)
    except ValueError as e:
        await message.answer(str(e))
    

@router.message(F.text, CreateProfile.sending_goal)
async def process_goal(message: Message, state: FSMContext, bot: Bot):
    """Process user's goal.
    User has finished collecting all the data.
    Create user in the API's database OR update existing user.
    Clear the state, set 'Main' state.

    Args:
        message (Message): Message object
        state (FSMContext): FSMContext object
        bot (Bot): Bot object
    """
    await state.update_data(goal=message.text)
    await message.answer('Начало положено!\nМы собрали всю информацию и готовы к работе.'
                         '\n\nВоспользуйтесь меню\nСоветую для начала создать план тренировок',
                         reply_markup=ReplyKeyboardRemove())
    user_data = await state.get_data()
    user_data['id'] = message.from_user.id

    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await create_user(user_data)
    await state.clear()
    await set_main_menu(bot)
    await state.set_state(Main.main_menu)
