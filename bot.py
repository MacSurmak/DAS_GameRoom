import asyncio
import urllib

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config_data import config
from handlers import commands_router, admin_router, messages_router
from keyboards import set_commands_menu
from middlewares import MessageThrottlingMiddleware, DbSessionMiddleware, GetLangMiddleware
from database import Base
from services import setup_logger


async def main() -> None:

    bot: Bot = Bot(token=config.bot.token,
                   default=DefaultBotProperties(parse_mode='HTML'))

    bot_storage: RedisStorage = RedisStorage.from_url(
        f'redis://{config.redis.user}:{urllib.parse.quote_plus(config.redis.password)}@{config.redis.host}:{config.redis.port}/0'
    )
    middleware_storage: RedisStorage = RedisStorage.from_url(
        f'redis://{config.redis.user}:{urllib.parse.quote_plus(config.redis.password)}@{config.redis.host}:{config.redis.port}/1'
    )

    dp: Dispatcher = Dispatcher(storage=bot_storage)

    engine = create_async_engine(url=config.db.url, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    session_maker = async_sessionmaker(engine, expire_on_commit=False)

    dp.message.middleware(MessageThrottlingMiddleware(storage=middleware_storage))
    dp.update.middleware(DbSessionMiddleware(session_pool=session_maker))
    dp.callback_query.middleware(CallbackAnswerMiddleware())
    dp.update.middleware(GetLangMiddleware(session_pool=session_maker))

    dp.include_router(admin_router)
    dp.include_router(commands_router)
    dp.include_router(messages_router)

    await set_commands_menu(bot)
    await bot.delete_webhook(drop_pending_updates=True)

    polling_task = asyncio.create_task(dp.start_polling(bot))

    await polling_task


if __name__ == '__main__':
    setup_logger("DEBUG")
    asyncio.run(main())
