"""Entry point for bot"""
import asyncio
import logging
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis
from bot.config import config
from bot.api.client import APIClient
from bot.middlewares.throttling import ThrottlingMiddleware
from bot.handlers.start import router as start_router
from bot.handlers.main import router as main_router
from bot.handlers.profile import router as profile_router
from bot.handlers.plan import router as plan_router


def create_storage() -> RedisStorage:
    """Create FSM storage for bot."""
    redis = Redis(host=config.HOST,
                  port=config.BOT_STORAGE_PORT)
    storage = RedisStorage(redis=redis)
    return storage


def configure_logging():
    logging.basicConfig(filename="bot_logs.log",
                        level=logging.INFO,
                        format='[%(asctime)s] %(levelname)s \n%(filename)s:%(lineno)d - %(name)s - %(message)s\n')


async def main():
    """Start the bot."""
    configure_logging()
    bot = Bot(token=config.BOT_TOKEN,
              session=AiohttpSession(),
              default=DefaultBotProperties(
                  parse_mode=ParseMode.HTML
              ))

    storage = create_storage()
    dispatcher = Dispatcher(storage=storage)

    client = APIClient()
    # close client session with api on bot's shutdown
    dispatcher.shutdown.register(client.close_session)

    # include routers here
    dispatcher.include_routers(start_router,
                               main_router,
                               profile_router,
                               plan_router)

    # include middlewares here
    dispatcher.update.middleware(ThrottlingMiddleware(storage=storage))

    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot, api_client=client)


if __name__ == '__main__':
    asyncio.run(main())
