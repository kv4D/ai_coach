from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from aiogram.utils.formatting import as_marked_list
from service.api import create_user, get_activity_levels, get_activity_levels_descriptions
from states.create_profile import CreateProfile
from validators.user import validate_activity_level, validate_age, \
    validate_gender, validate_height, validate_weight
from keyboards.start import get_gender_kb, get_activity_level_kb

router = Router()


@router.message(CommandStart())
async def handle_start_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Привет, я буду помогать тебе. Напиши свое <b>имя</b>',
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(CreateProfile.sending_name)


@router.message(F.text, CreateProfile.sending_name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer(f'Теперь введи свой <b>возраст</b>',
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(CreateProfile.sending_age)


@router.message(F.text, CreateProfile.sending_age)
async def process_age(message: Message, state: FSMContext):
    try:
        age = validate_age(message.text)
        # some other checks
        await message.answer(f'Укажи свой <b>пол</b>', 
                            reply_markup=get_gender_kb())
        await state.update_data(age=age)
        await state.set_state(CreateProfile.sending_gender)
    except ValueError as e:
        await message.answer(str(e))


@router.message(F.text, CreateProfile.sending_gender)
async def process_gender(message: Message, state: FSMContext):
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
async def process_weight(message: Message, state: FSMContext):
    try:
        weight = validate_weight(message.text)

        levels = get_activity_levels()
        descriptions = get_activity_levels_descriptions()
        levels_descriptions = [
            f"Уровень {level}:\n{descriptions[level]}\n\n" for level in levels
            ]

        await state.update_data(weight_kg=weight)
        
        content = as_marked_list(*levels_descriptions, marker="🏆 ") 
        await message.answer('Выбери свой <b>уровень активности</b>',
                            reply_markup=ReplyKeyboardRemove())
        await message.answer(**content.as_kwargs(), 
                            reply_markup=get_activity_level_kb())
        await state.set_state(CreateProfile.sending_activity_level)
    except ValueError as e:
        await message.answer(str(e))


@router.message(F.text, CreateProfile.sending_activity_level)
async def process_activity_level(message: Message, state: FSMContext):
    try:
        activity_level = validate_activity_level(message.text)
        await message.answer('Отлично, теперь расскажи о своей <b>цели</b>: для чего ты занимаешься,'
                            'чего хочешь добиться и прочее. Это сделает мою помощь более полезной.\n\n'
                            'Если у тебя нет цели, то можешь так и написать', 
                            reply_markup=ReplyKeyboardRemove())
        await state.update_data(activity_level=activity_level)
        await state.set_state(CreateProfile.sending_goal)
    except ValueError as e:
        await message.answer(str(e))
    

@router.message(F.text, CreateProfile.sending_goal)
async def process_goal(message: Message, state: FSMContext):
    await state.update_data(goal=message.text)
    await message.answer('Начало положено!\nМы собрали всю информацию и готовы к работе.'
                         '\n\nВоспользуйтесь меню\nСоветую для начала создать план тренировок',
                         reply_markup=ReplyKeyboardRemove())
    # it is worth to check if user already in DB
    # probably we can delete them and create again
    user_data = await state.get_data()
    user_data['id'] = message.from_user.id
    create_user(user_data)
    await state.clear()
