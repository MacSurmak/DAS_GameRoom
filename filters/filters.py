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

        user = await session.get(UserBase, user_id)
        if user:
            if user.registered:
                return True
        return False


class IsAdmin(BaseFilter):
    async def __call__(self, event, session: AsyncSession) -> bool:

        if type(event) is Message:
            user_id = event.chat.id
        else:
            user_id = event.message.chat.id

        user = await session.get(UserBase, user_id)
        if user.admin:
            return True
        return False
