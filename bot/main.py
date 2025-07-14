"""Entry point for bot"""
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis
from config import Config
from handlers.start import router as start_router


async def main():
    """
    Start the bot
    """
    config = Config() # type: ignore
    
    bot = Bot(token=config.bot_token)
    redis = Redis(host=config.db_host)
    storage = RedisStorage(redis=redis)
    dispatcher = Dispatcher(storage=storage)
    
    # include routers here
    dispatcher.include_routers(start_router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())