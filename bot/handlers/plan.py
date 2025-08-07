"""Handlers for main state."""
from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.chat_action import ChatActionSender
from aiogram.enums.parse_mode import ParseMode
from api.client import APIClient
from service.service import create_user_training_plan
from states.main import Main
from states.create_plan import CreatePlan


router = Router()


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

@router.message(F.text, CreatePlan.sending_request)
async def handle_plan_request(message: Message, 
                              state: FSMContext, 
                              bot: Bot,
                              api_client: APIClient):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        request = message.text
        await message.answer('Генерирую план, ожидайте')
        # create user plan here
        user_id = message.from_user.id
        await create_user_training_plan(user_id,
                                        request,
                                        api_client=api_client)
        training_plan = await api_client.get_user_training_plan(user_id)
    await message.answer('Ваш план готов!')
    await message.answer(training_plan)
    await state.set_state(Main.main)
