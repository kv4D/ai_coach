"""Handlers for main state."""
from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.chat_action import ChatActionSender
from bot.api.client import APIClient
from bot.states.main import Main
from bot.states.use_ai import UseAI


router = Router()


@router.message(F.text, UseAI.sending_request)
async def handle_plan_request(message: Message,
                              state: FSMContext,
                              bot: Bot,
                              api_client: APIClient):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        request = message.text
        user_id = message.from_user.id
        await state.set_state(UseAI.generating_answer)
        await api_client.create_user_training_plan(user_id,
                                                   request)
        training_plan = await api_client.get_user_training_plan(user_id)
    await message.answer('Ваш план готов ✅')
    await message.answer(training_plan)
    await state.set_state(Main.main)
