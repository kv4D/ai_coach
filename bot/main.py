"""Entry point for bot"""
import asyncio
from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis
from config import config
from handlers.start import router as start_router
from handlers.main import router as main_router


async def main():
    """
    Start the bot
    """
    bot = Bot(token=config.TG_BOT_TOKEN,
              default=DefaultBotProperties(
                  parse_mode=ParseMode.HTML
              ))
    redis = Redis(host=config.DB_HOST,
                  port=config.TG_BOT_STORAGE_PORT)
    storage = RedisStorage(redis=redis)
    dispatcher = Dispatcher(storage=storage)
    
    # include routers here
    dispatcher.include_routers(start_router, main_router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())