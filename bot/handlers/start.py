from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from aiogram.utils.formatting import as_marked_list
from service.api import create_user
from states.create_profile import CreateProfile
from keyboards.start import get_gender_kb, get_activity_level_kb

router = Router()


@router.message(CommandStart())
async def handle_start_command(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Привет, я буду помогать тебе. Напиши свое <b>имя</b>')
    await state.set_state(CreateProfile.sending_name)

@router.message(F.text, CreateProfile.sending_name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(f'Теперь введи свой <b>возраст</b>')
    await state.set_state(CreateProfile.sending_age)

@router.message(F.text, CreateProfile.sending_age)
async def process_age(message: Message, state: FSMContext):
    age = message.text
    if age is None or not age.isnumeric():
        await message.reply('Используй только цифры')
        return
    # some other checks
    await message.answer(f'Укажи свой <b>пол</b>', reply_markup=get_gender_kb())
    await state.update_data(age=int(age))
    await state.set_state(CreateProfile.sending_gender)

@router.message(F.text, CreateProfile.sending_gender)
async def process_gender(message: Message, state: FSMContext):
    gender = message.text
    print(gender)
    if gender is None:
        await message.answer('Пожалуйста, укажи свой пол')
        return
    if gender.lower()[:3] == 'муж':
        await state.update_data(gender='male')
    elif gender.lower()[:3] == 'жен':
        await state.update_data(gender='female')
    else: 
        await message.reply('Не могу распознать, используй кнопки')
        return
    await message.answer('А теперь введи свой <b>рост в сантиметрах</b>',
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(CreateProfile.sending_height)

@router.message(F.text, CreateProfile.sending_height)
async def process_height(message: Message, state: FSMContext):
    height = message.text
    if height is None or not height.isnumeric():
        await message.reply('Используй только цифры')
        return
    # some other checks
    await message.answer('Выбери свой уровень активности, согласно описаниям ниже')
    
    # simulation
    # TODO: change later with API
    level_descriptions = [
        ('1', 'Сидячий'),
        ('2', 'Малоподвижный'),
        ('3', 'Активный'),
        ('4', 'Спортивный'),
        ('5', 'Божественный')
    ]
    
    level_descriptions = [
        f"<b>Уровень {i[0]}</b>:\n{i[1]}\n\n" for i in level_descriptions
        ]

    content = as_marked_list(*level_descriptions, marker="🏆 ") 

    await message.answer(**content.as_kwargs(), reply_markup=get_activity_level_kb())
    await state.update_data(height_cm=float(height.replace(',','.')))
    await state.set_state(CreateProfile.sending_weight)


@router.message(F.text, CreateProfile.sending_activity_level)
async def process_activity_level(message: Message, state: FSMContext):
    activity_level = message.text
    if activity_level not in [1, 2, 3, 4, 5]:
        await message.reply('Такого варианта не было, используй кнопки')
        return
    await message.answer('Введи свой <b>вес (килограммы)</b>', reply_markup=ReplyKeyboardRemove())
    await state.update_data(activity_level=activity_level)
    await state.set_state(CreateProfile.sending_weight)

@router.message(F.text, CreateProfile.sending_weight)
async def process_weight(message: Message, state: FSMContext):
    weight = message.text
    if weight is None or not weight.isnumeric():
        await message.answer('Используй только цифры')
        return
    # some other checks
    await message.answer(f'Отлично, теперь расскажи о своей <b>цели</b>: для чего ты занимаешься,'
                         f'чего хочешь добиться и прочее. Это сделает мою помощью более полезной.\n\n'
                         f'Если у тебя нет цели, то можешь так и написать')
    await state.update_data(height_cm=float(weight.replace(',','.')))
    await state.set_state(CreateProfile.sending_goal)

@router.message(F.text, CreateProfile.sending_goal)
async def process_goal(message: Message, state: FSMContext):
    await state.update_data(goal=message.text)
    await message.answer(f'Начало положено!\nМы собрали всю информацию и готовы к работе.'
                         f'\n\nВоспользуйтесь меню\nСоветую для начала создать план тренировок')
    # it is worth to check if user already in DB
    # probably we can delete them and create again
    user_data = await state.get_data()
    print(create_user(user_data))
    await state.clear()
    