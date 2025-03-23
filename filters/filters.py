from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import *


class IsRegistered(BaseFilter):
    """Checks if the user is registered in the database."""
    async def __call__(self, event: Message | CallbackQuery, session: AsyncSession) -> bool:
        """
        Checks user registration.

        Args:
            event: The incoming event (Message or CallbackQuery).
            session: The database session.

        Returns:
            True if the user is registered, False otherwise.
        """

        if isinstance(event, Message):
            user_id = event.from_user.id
        elif isinstance(event, CallbackQuery):
             user_id = event.from_user.id
        else:
            return False

        user = await session.execute(select(User).where(User.telegram_id == user_id))
        user = user.scalar_one_or_none()

        return bool(user)


class IsAdmin(BaseFilter):
    """Checks if the user is an administrator."""
    async def __call__(self, event: Message | CallbackQuery, session: AsyncSession) -> bool:
        """
        Checks user admin status.

        Args:
            event: The incoming event (Message or CallbackQuery).
            session: The database session.

        Returns:
            True if user is admin, False otherwise
        """

        if isinstance(event, Message):
            user_id = event.from_user.id
        elif isinstance(event, CallbackQuery):
            user_id = event.from_user.id
        else:
            return False

        user = await session.execute(select(User).where(User.telegram_id == user_id))
        user = user.scalar_one_or_none()
        # Check both user existence and admin flag
        return bool(user and user.is_admin)
