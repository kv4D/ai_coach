"""Command menu buttons setters."""
from aiogram import Bot
from aiogram.types import BotCommand


async def set_menu(bot: Bot):
    """Set up menu with bot commands.

    You should use this when user is **authorized**.

    Args:
        bot (`Bot`): your bot object    
    """    
    menu_commands = [
        BotCommand(command='/my_plan',
                   description='Просмотреть план тренировок'),
        BotCommand(command='/generate_plan',
                   description='Сгенерировать план тренировок'),
        BotCommand(command='/profile',
                   description='Профиль'),
        BotCommand(command='/help',
                   description='О работе с ботом'),
        BotCommand(command='/start',
                   description='Создать профиль с нуля'),
    ]
    await bot.set_my_commands(menu_commands)
