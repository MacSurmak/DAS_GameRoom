from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from sqlalchemy.ext.asyncio import AsyncSession

from database import UserBase
from filters import IsRegistered
from handlers.dialog import MySG
from lexicon.lexicon import lexicon

commands_router: Router = Router(name='commands-router')


@commands_router.message(CommandStart())
async def start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MySG.main, mode=StartMode.RESET_STACK)


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
