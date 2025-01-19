from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import UserBase
from filters import IsRegistered
from handlers.states import RegistrationSG
from lexicon import lexicon

commands_router: Router = Router(name='commands-router')


@commands_router.message(CommandStart(), ~IsRegistered())
async def start_unregistered(message: Message, session: AsyncSession, dialog_manager: DialogManager, lang: str):
    """
    :param message: Telegram message
    :param session: DB connection session
    :param dialog_manager: DialogManager for starting dialogs
    :param lang: language code
    """
    user = UserBase(
        user_id=message.from_user.id,
        username=message.from_user.username,
        lang=message.from_user.language_code
    )
    await session.merge(user)
    await session.commit()
    await dialog_manager.start(RegistrationSG.start, mode=StartMode.RESET_STACK)


@commands_router.message(CommandStart(), IsRegistered())
async def start_registered(message: Message, session: AsyncSession, lang: str):
    """
    :param message: Telegram message
    :param session: DB connection session
    :param lang: language code
    """
    query = select(UserBase.first_name).where(UserBase.user_id == message.from_user.id)
    name = await session.scalar(query)
    await message.answer(text=lexicon(lang, 'start-registered').format(name=name))
