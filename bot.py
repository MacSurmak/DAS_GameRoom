import asyncio
import urllib

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from aiogram_dialog import setup_dialogs
from loguru import logger

from config_data import config
from dialogs import registration_dialog, language_dialog, main_menu_dialog, schedule_dialog  # Import dialogs
from keyboards import set_commands_menu
from middlewares import DbSessionMiddleware, GetLangMiddleware, MessageThrottlingMiddleware
from database import Base
from services import setup_logger, populate_initial_data
from handlers import commands_router, messages_router # import routers


async def initialize_storage(config) -> tuple[RedisStorage, RedisStorage]:
    """
    Initializes and returns Redis storages for the bot and middleware.

    Args:
        config: The configuration object containing Redis settings.

    Returns:
        A tuple containing two RedisStorage instances: one for the bot and one for middleware.
    """
    bot_storage = RedisStorage.from_url(
        f'redis://{config.redis.user}:{urllib.parse.quote_plus(config.redis.password)}@{config.redis.host}:{config.redis.port}/{config.redis.bot_database}',
        key_builder=DefaultKeyBuilder(with_destiny=True)
    )
    middleware_storage = RedisStorage.from_url(
        f'redis://{config.redis.user}:{urllib.parse.quote_plus(config.redis.password)}@{config.redis.host}:{config.redis.port}/{config.redis.middleware_database}',
        key_builder=DefaultKeyBuilder(with_destiny=True)
    )
    return bot_storage, middleware_storage


async def initialize_db(config):
    """
    Initializes and returns the database engine and session maker.

    Args:
        config: The configuration object containing database settings.

    Returns:
        A tuple containing the database engine and session maker.
    """
    engine = create_async_engine(url=config.db.url, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)
    return engine, session_maker


def setup_middlewares(dp: Dispatcher, session_maker: async_sessionmaker, middleware_storage: RedisStorage):
    """
    Sets up middlewares for the dispatcher.

    Args:
        dp: The aiogram Dispatcher instance.
        session_maker: The database session maker.
        middleware_storage: The Redis storage for middleware.
    """
    dp.update.middleware(DbSessionMiddleware(session_pool=session_maker))
    dp.update.middleware(GetLangMiddleware(session_pool=session_maker, storage=middleware_storage))
    dp.message.middleware(MessageThrottlingMiddleware(storage=middleware_storage)) # Added throttling middleware
    dp.callback_query.middleware(CallbackAnswerMiddleware())


def setup_routers(dp: Dispatcher):
    """
    Sets up routers for the dispatcher.

    Args:
        dp: The aiogram Dispatcher instance.
    """
    dp.include_router(registration_dialog)
    dp.include_router(language_dialog)
    dp.include_router(commands_router)
    dp.include_router(main_menu_dialog) # added
    dp.include_router(schedule_dialog)
    dp.include_router(messages_router)

    setup_dialogs(dp)


def setup_logging():
    """Configures the logger."""
    setup_logger("DEBUG")


async def start_polling(bot: Bot, dp: Dispatcher):
    """
    Starts polling for updates.

    Args:
        bot: The aiogram Bot instance.
        dp: The aiogram Dispatcher instance.
    """
    await set_commands_menu(bot)  # Set bot commands
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


async def main() -> None:
    """Main function to start the bot."""
    setup_logging()

    bot = Bot(token=config.bot.token, default=DefaultBotProperties(parse_mode='HTML'))
    bot_storage, middleware_storage = await initialize_storage(config)
    dp = Dispatcher(storage=bot_storage)
    engine, session_maker = await initialize_db(config)

    # --- Call populate_initial_data here ---
    async with session_maker() as session:
      try:
        await populate_initial_data(session)
      except Exception as e:
        logger.error(f"Initial data population failed, bot will exit: {e}")
        return # Exit if population fails

    setup_middlewares(dp, session_maker, middleware_storage)
    setup_routers(dp)
    try:
        await start_polling(bot, dp)  # Start polling
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())
