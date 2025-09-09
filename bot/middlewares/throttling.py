from typing import Any, Awaitable, Callable
import logging
from aiogram import BaseMiddleware
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import TelegramObject
from .utils import send_message_from_middleware

logger = logging.getLogger(__name__)


class ThrottlingMiddleware(BaseMiddleware):
    """
    Provides anti-spam measures.

    - storage - RedisStorage object to use Redis for cache
    - expire_time_seconds - time for user's updates cooldown
    """

    def __init__(self, storage: RedisStorage, cooldown_time_seconds: int = 2):
        self.storage = storage
        self.cooldown_time = cooldown_time_seconds

    async def __call__(self,
                       handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: dict[str, Any]
                       ) -> Any:
        user_id: int = data.get("event_from_user").id  # type: ignore
        # use this as a key to get/set
        user_throttling_key: str = f"throttling:{user_id}:throttling_status"

        on_cooldown = await self.storage.redis.get(user_throttling_key)

        if on_cooldown:
            await send_message_from_middleware("Пожалуйста, подождите, "
                                               "вы отправляете слишком много сообщений ⏱️",
                                               data=data)
            logger.info("User (id=%i) sending too many messages", user_id)
            return

        # message is processed successfully, set cooldown timer on message
        await self.storage.redis.set(name=user_throttling_key, value=user_id, ex=self.cooldown_time)
        result = await handler(event, data)
        return result
