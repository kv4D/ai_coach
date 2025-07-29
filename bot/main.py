"""Entry point for bot"""
import asyncio
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis
from config import config
from api.client import APIClient
from handlers.start import router as start_router
from handlers.main import router as main_router
from handlers.profile import router as profile_router


def create_storage() -> RedisStorage:
    redis = Redis(host=config.DB_HOST,
                  port=config.TG_BOT_STORAGE_PORT)
    storage = RedisStorage(redis=redis)
    return storage


async def main():
    """
    Start the bot
    """
    bot = Bot(token=config.TG_BOT_TOKEN,
              session=AiohttpSession(),
              default=DefaultBotProperties(
                  parse_mode=ParseMode.HTML
              ))
    
    dispatcher = Dispatcher(storage=create_storage())
    
    client = APIClient()
    # close client session with api on bot's shutdown
    dispatcher.shutdown.register(client.close_session)
    
    # include routers here
    dispatcher.include_routers(start_router, 
                               main_router,
                               profile_router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot, api_client=client)


if __name__ == '__main__':
    asyncio.run(main())