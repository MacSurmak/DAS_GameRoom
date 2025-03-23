from aiogram.types import CallbackQuery
from aiogram_dialog.widgets.kbd import Button, ManagedListGroup
from sqlalchemy.ext.asyncio import AsyncSession

from database import User


async def save_lang(callback: CallbackQuery, button: Button, manager: ManagedListGroup, session: AsyncSession):
    user_id: int = callback.message.chat.id
    item_id: str = manager.item_id
    user = User(
        telegram_id=user_id,
        lang=item_id
    )
    await session.merge(user)
    await session.commit()

    manager.middleware_data["lang"] = item_id

    await manager.done()
