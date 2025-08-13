"""Command menu buttons setters."""
from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat


async def set_menu(bot: Bot, chat_id: int | None = None):
    """Set up menu with bot commands.

    It is the main menu bot commands.
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
    if chat_id:
        await bot.set_my_commands(menu_commands, scope=BotCommandScopeChat(chat_id=chat_id))
    else:
        await bot.set_my_commands(menu_commands)

async def set_cancel(bot: Bot, chat_id: int):
    """Set up cancel option with bot commands.

    You should use this when a user have an option to
    go back.

    Args:
        bot (`Bot`): your bot object    
    """    
    menu_commands = [
        BotCommand(command='/cancel',
                   description='Отмена'),
    ]
    await bot.set_my_commands(menu_commands, scope=BotCommandScopeChat(chat_id=chat_id))
