from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from states.create_profile import CreateProfile

router = Router()

@router.message(CommandStart())
async def handle_start_command(message: Message, state: FSMContext):
    await message.answer('I am useless right *now*', 
                   parse_mode=ParseMode.MARKDOWN_V2)
    
    await state.set_state(CreateProfile.sending_name)


@router.message(CreateProfile.sending_name, F.text)
async def handle_name_input(message: Message, state: FSMContext):
    await state.update_data