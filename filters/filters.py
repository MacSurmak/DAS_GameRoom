from aiogram.filters import BaseFilter
from aiogram.types import Message
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import *


class IsRegistered(BaseFilter):
    async def __call__(self, event, session: AsyncSession) -> bool:

        if type(event) is Message:
            user_id = event.chat.id
        else:
            user_id = event.message.chat.id

        state = False
        query = select(UserBase).where(UserBase.user_id == user_id)
        if await session.scalar(query):
            state = True
        return state


class IsAdmin(BaseFilter):
    async def __call__(self, event, session: AsyncSession) -> bool:

        if type(event) is Message:
            user_id = event.chat.id
        else:
            user_id = event.message.chat.id

        state = False
        query = select(UserBase.admin).where(UserBase.user_id == user_id)
        if await session.scalar(query):
            state = True
        return state
