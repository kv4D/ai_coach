from aiogram import Bot
from aiogram.types import BotCommand


async def set_main_menu(bot: Bot):
    """Set up menu with bot commands in main menu."""    
    main_menu_commands = [
        BotCommand(command='/start',
                   description='Создать профиль с нуля'),
        BotCommand(command='/my_plan',
                   description='Просмотреть план тренировок'),
        BotCommand(command='/generate_plan',
                   description='Сгенерировать план тренировок'),
        BotCommand(command='/profile',
                   description='Профиль'),
        BotCommand(command='/help',
                   description='О работе с ботом'),
    ]
    await bot.set_my_commands(main_menu_commands)
