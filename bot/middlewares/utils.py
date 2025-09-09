from typing import Any
from aiogram import Bot
from aiogram.types import Chat


async def send_message_from_middleware(message: str, data: dict[str, Any]):
    """Send message from middleware using Bot object. 

    Args:
        data (dict[str, Any]): data dict argument that you receive in
        a middleware __call__() method

    Returns:
        _type_: _description_
    """
    bot: Bot = data.get("bot")  # type: ignore
    chat: Chat = data.get("event_chat")  # type: ignore
    await bot.send_message(text=message, chat_id=chat.id)
