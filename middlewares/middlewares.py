from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject, Update
from aiogram.fsm.storage.redis import RedisStorage
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from typing import Any, Awaitable, Callable, Dict

from database import UserBase
from lexicon import lexicon


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
    def __init__(self, session_pool: async_sessionmaker):
        super().__init__()
        self.session_pool = session_pool

    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: Update,
                       data: Dict[str, Any]) -> Any:
        async with self.session_pool() as session:
            query = select(UserBase.lang).where(UserBase.user_id == event.event.from_user.id)
            lang = await session.scalar(query)
            if lang is not None:
                data["lang"] = await session.scalar(query)
            else:
                data["lang"] = event.event.from_user.language_code
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
