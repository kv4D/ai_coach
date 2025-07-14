from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from states.create_profile import CreateProfile

router = Router()

@router.message(CommandStart())
async def handle_start_command(message: Message):
    await message.answer('I am useless right *now*', 
                   parse_mode=ParseMode.MARKDOWN_V2)
