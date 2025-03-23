from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject, Update
from aiogram.fsm.storage.redis import RedisStorage
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from typing import Any, Awaitable, Callable, Dict

from database import User
from lexicon import lexicon, LANGUAGES
from lexicon.lexicon import DEFAULT_LANG


class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        super().__init__()
        self.session_pool = session_pool

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            data["session"] = session
            return await handler(event, data)


class GetLangMiddleware(BaseMiddleware):
    """Determines the user's language and provides it to handlers."""
    def __init__(self, session_pool: async_sessionmaker, storage: RedisStorage):
        super().__init__()
        self.session_pool = session_pool
        self.storage = storage

    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: Update,
                       data: Dict[str, Any]) -> Any:
        lang_code = DEFAULT_LANG # Default language

        if event.event.from_user:
            telegram_id = event.event.from_user.id

            async with self.session_pool() as session:
                user: User | None = await session.execute(select(User).where(User.telegram_id == telegram_id))
                user_row = user.scalar_one_or_none()

                if user_row:
                    lang_code = user_row.lang if user_row.lang else event.event.from_user.language_code
                    logger.debug(f"User language from DB: {lang_code}")
                else:
                    # User not in DB, use Telegram's language if available
                    telegram_lang = event.event.from_user.language_code
                    logger.debug(f"User language from Telegram: {telegram_lang}")
                    if telegram_lang in [lang['code'] for lang in LANGUAGES]:
                        lang_code = telegram_lang

        data["lang"] = lang_code
        data["storage"] = self.storage
        return await handler(event, data)


class MessageThrottlingMiddleware(BaseMiddleware):
    def __init__(self, storage: RedisStorage):
        self.storage = storage

    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]) -> Any:

        user = str(event.from_user.id)
        check_user = await self.storage.redis.get(name=user)

        if check_user:
            if int(check_user.decode()) == 1:
                await self.storage.redis.set(name=user, value=2, ex=3)
                return await handler(event, data)
            elif int(check_user.decode()) == 2:
                await self.storage.redis.set(name=user, value=3, ex=10)
                return await event.answer(lexicon(data['lang'], 'throttling-warning'))
            elif int(check_user.decode()) == 3:
                return

        await self.storage.redis.set(name=user, value=1, ex=3)
        return await handler(event, data)
