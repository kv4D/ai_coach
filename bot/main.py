"""Entry point for bot"""
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis
from config import config
from handlers.start import router as start_router


async def main():
    """
    Start the bot
    """
    bot = Bot(token=config.TG_BOT_TOKEN)
    # redis = Redis(host=config.DB_HOST)
    # storage = RedisStorage(redis=redis)
    dispatcher = Dispatcher(storage=None)
    
    # include routers here
    dispatcher.include_routers(start_router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())