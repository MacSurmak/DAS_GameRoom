from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from sqlalchemy.ext.asyncio import AsyncSession

from filters import IsAdmin
from database import UserBase

admin_router: Router = Router(name='admin-router')
admin_router.message.filter(IsAdmin())


@admin_router.message(CommandStart())
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

    await message.answer(text="Hello-adm")
