from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from database import UserBase
from filters import IsRegistered
from lexicon.lexicon import lexicon

commands_router: Router = Router(name='commands-router')


@commands_router.message(CommandStart(), IsRegistered())
async def process_start_command(message: Message, session: AsyncSession, lang: str):
    """
    :param lang: language code
    :param message: Telegram message
    :param session: DB connection session
    """
    user = UserBase(
        user_id=message.from_user.id,
        username=message.from_user.username
    )
    await session.merge(user)
    await session.commit()

    await message.answer(text=f"Hello-reg, {lang}")


@commands_router.message(CommandStart(), ~IsRegistered())
async def process_start_command(message: Message, session: AsyncSession, lang: str):
    """
    :param lang: language code
    :param message: Telegram message
    :param session: DB connection session
    """
    user = UserBase(
        user_id=message.from_user.id,
        username=message.from_user.username,
        lang=message.from_user.language_code
    )
    await session.merge(user)
    await session.commit()

    await message.answer(text=f"Hello-no-reg, {lang}")
