from aiogram import Router
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from filters import IsRegistered

messages_router: Router = Router(name='messages-router')


@messages_router.message(IsRegistered())
async def process(message: Message, session: AsyncSession):
    """
    :param message: Telegram message
    :param session: DB connection session
    """
    await message.answer(text="Message-reg")
