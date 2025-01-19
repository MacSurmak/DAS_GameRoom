from aiogram import Router
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from database import UserBase
from filters import IsRegistered

messages_router: Router = Router(name='messages-router')


@messages_router.message(IsRegistered())
async def process_start_command(message: Message, session: AsyncSession):
    """
    :param message: Telegram message
    :param session: DB connection session
    """
    user = UserBase(
        user_id=message.from_user.id,
        username=message.from_user.username
    )
    await session.merge(user)
    await session.commit()

    await message.answer(text="Message-reg")
