from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.chat_action import ChatActionSender
from bot.service.service import get_activity_levels_description, create_user
from bot.api.client import APIClient
from bot.states.create_profile import CreateProfile
from bot.states.main import Main
from bot.keyboards.common import get_gender_kb, get_activity_level_kb
from bot.keyboards.commands import set_menu, set_cancel
from bot.filters.user import UserExistsFilter
from bot.models.user import User
from bot.models.activity_level import ActivityLevel
from bot.utils import get_command_descriptions


router = Router()


@router.message(Command('cancel'), StateFilter(CreateProfile), UserExistsFilter())
async def handle_cancel_command(message: Message,
                                state: FSMContext,
                                bot: Bot):
    """
    Handle /cancel command of an old user.

    Cancel updating their profile.
    """
    await state.clear()
    await message.answer('Изменения отменены ❌',
                         reply_markup=ReplyKeyboardRemove())
    await set_menu(bot, message.chat.id)
    await state.set_state(Main.main)


@router.message(CommandStart(), StateFilter(Main.main), UserExistsFilter())
async def handle_old_user_start_command(message: Message,
                                        state: FSMContext,
                                        bot: Bot):
    """
    Handle /start command, but from a user that is
    already in the database.

    Set state flag and give a chance to
    revert changes.
    Start collecting user's data.
    Begin with user's age.
    """
    await state.clear()
    await message.answer('Вы начинаете заполнять профиль с нуля 📋\nЕсли вы передумаете, используйте команду <b>/cancel</b> 🔙',
                         reply_markup=ReplyKeyboardRemove())
    await message.answer('Введите ваш <b>возраст</b> 🌱')
    await bot.delete_my_commands()
    await set_cancel(bot, message.chat.id)
    await state.set_state(CreateProfile.sending_age)


@router.message(CommandStart(), StateFilter(None, Main.main), ~UserExistsFilter())
async def handle_new_user_start_command(message: Message,
                                        state: FSMContext,
                                        bot: Bot):
    """
    Handle /start command from a new user.

    User starts the bot by sending the /start command.
    Start collecting user's data.
    Begin with user's age.
    """
    await state.clear()
    await bot.delete_my_commands()
    await message.answer('Привет, я буду помогать вам 👋\nДавайте заполним информацию о вас 📋',
                         reply_markup=ReplyKeyboardRemove())
    await message.answer('Введите ваш <b>возраст</b> 🌱')
    await state.set_state(CreateProfile.sending_age)


@router.message(F.text, CreateProfile.sending_age)
async def process_age(message: Message, state: FSMContext):
    """
    Process user's age.
    If everything is OK: try to get gender.
    """
    age = User.validate_age(message.text)
    keyboard = get_gender_kb()
    await message.answer('Укажите ваш <b>пол</b> ♀️♂️',
                         reply_markup=keyboard)
    await state.update_data(age=age)
    await state.set_state(CreateProfile.sending_gender)


@router.message(F.text, CreateProfile.sending_gender)
async def process_gender(message: Message, state: FSMContext):
    """
    Process user's gender.
    If everything is OK: try to get height.
    """
    gender = User.validate_gender(message.text)
    await state.update_data(gender=gender)
    await message.answer('А теперь введите ваш <b>рост в сантиметрах</b> 📏',
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(CreateProfile.sending_height)


@router.message(F.text, CreateProfile.sending_height)
async def process_height(message: Message, state: FSMContext):
    """
    Process user's height.
    If everything is OK: try to get weight.
    """
    height = User.validate_height_cm(message.text)
    await message.answer('Укажите ваш <b>вес в килограммах</b> ⚖️',
                         reply_markup=ReplyKeyboardRemove())
    await state.update_data(height_cm=height)
    await state.set_state(CreateProfile.sending_weight)


@router.message(F.text, CreateProfile.sending_weight)
async def process_weight(message: Message,
                         state: FSMContext,
                         bot: Bot,
                         api_client: APIClient):
    """
    Process user's weight.
    If everything is OK: try to get activity level.
    """
    weight = User.validate_weight_kg(message.text)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        levels_info = await get_activity_levels_description(api_client)

        await message.answer('Выберите ваш <b>уровень активности</b> 🔋',
                             reply_markup=ReplyKeyboardRemove())

        keyboard = await get_activity_level_kb(api_client)

        await message.answer(levels_info,
                             reply_markup=keyboard)
        await state.update_data(weight_kg=weight)
        await state.set_state(CreateProfile.sending_activity_level)


@router.message(F.text, CreateProfile.sending_activity_level)
async def process_activity_level(message: Message,
                                 state: FSMContext):
    """
    Process user's activity level.
    If everything is OK: try to get user's goal.
    """
    activity_level = ActivityLevel.validate_level(message.text)
    await message.answer('Отлично, теперь расскажите о вашей <b>цели</b> 🎯: для чего вы занимаетесь,'
                         'чего хотите добиться и прочее. Это сделает мою помощь более полезной.\n\n'
                         'Если у вас нет цели, то можете так и написать',
                         reply_markup=ReplyKeyboardRemove())
    await state.update_data(activity_level=activity_level)
    await state.set_state(CreateProfile.sending_goal)


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

    await message.answer('Начало положено!\nМы собрали всю информацию и готовы к работе 💯'
                         '\n\nВоспользуйтесь меню\nСоветую для начала создать план тренировок'
                         f'Список команд:\n{await get_command_descriptions(bot)}',
                         reply_markup=ReplyKeyboardRemove())
    await state.clear()
    await set_menu(bot, chat_id=message.chat.id)
    await state.set_state(Main.main)
