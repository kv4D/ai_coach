from aiogram import Bot


async def get_command_descriptions(bot: Bot):
    """Returns string with command list for user."""
    commands = await bot.get_my_commands()
    command_descriptions = ""
    for command in commands:
        command_descriptions += f"<b>/{command.command}</b>: {command.description}\n"
    return command_descriptions