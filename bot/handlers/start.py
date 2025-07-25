from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from aiogram.utils.formatting import as_marked_list
from service.api import create_user, get_activity_levels, get_activity_levels_descriptions
from states.create_profile import CreateProfile
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
    age = message.text
    # some other checks
    await message.answer(f'Укажи свой <b>пол</b>', 
                         reply_markup=get_gender_kb())
    await state.update_data(age=int(age))
    await state.set_state(CreateProfile.sending_gender)


@router.message(F.text, CreateProfile.sending_gender)
async def process_gender(message: Message, state: FSMContext):
    gender = message.text
    # some checks
    if gender.lower()[:3] == 'муж':
        await state.update_data(gender='male')
    elif gender.lower()[:3] == 'жен':
        await state.update_data(gender='female')
    await message.answer('А теперь введи свой <b>рост в сантиметрах</b>',
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(CreateProfile.sending_height)


@router.message(F.text, CreateProfile.sending_height)
async def process_height(message: Message, state: FSMContext):
    height = message.text
    # some checks
    await message.answer('Укажи свой <b>вес в килограммах</b>',
                         reply_markup=ReplyKeyboardRemove())
    await state.update_data(height_cm=float(height.replace(',','.')))
    await state.set_state(CreateProfile.sending_weight)


@router.message(F.text, CreateProfile.sending_weight)
async def process_weight(message: Message, state: FSMContext):
    weight = message.text
    # some checks
    levels = get_activity_levels()
    descriptions = get_activity_levels_descriptions()
    
    levels_descriptions = [
        f"Уровень {level}:\n{descriptions[level]}\n\n" for level in levels
        ]

    await state.update_data(weight_kg=float(weight.replace(',','.')))
    
    content = as_marked_list(*levels_descriptions, marker="🏆 ") 
    await message.answer('Выбери свой <b>уровень активности</b>',
                         reply_markup=ReplyKeyboardRemove())
    await message.answer(**content.as_kwargs(), 
                         reply_markup=get_activity_level_kb())
    await state.set_state(CreateProfile.sending_activity_level)


@router.message(F.text, CreateProfile.sending_activity_level)
async def process_activity_level(message: Message, state: FSMContext):
    activity_level = message.text
    # some checks
    await message.answer(f'Отлично, теперь расскажи о своей <b>цели</b>: для чего ты занимаешься,'
                         f'чего хочешь добиться и прочее. Это сделает мою помощью более полезной.\n\n'
                         f'Если у тебя нет цели, то можешь так и написать', 
                         reply_markup=ReplyKeyboardRemove())
    await state.update_data(activity_level=activity_level)
    await state.set_state(CreateProfile.sending_goal)


@router.message(F.text, CreateProfile.sending_goal)
async def process_goal(message: Message, state: FSMContext):
    await state.update_data(goal=message.text)
    await message.answer(f'Начало положено!\nМы собрали всю информацию и готовы к работе.'
                         f'\n\nВоспользуйтесь меню\nСоветую для начала создать план тренировок',
                         reply_markup=ReplyKeyboardRemove())
    # it is worth to check if user already in DB
    # probably we can delete them and create again
    user_data = await state.get_data()
    user_data['id'] = message.from_user.id
    create_user(user_data)
    await state.clear()
