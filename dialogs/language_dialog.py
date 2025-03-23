from typing import Any

from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from aiogram_dialog import Window, Dialog, DialogManager, Data
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button, Next, Row, SwitchTo, Group
from aiogram_dialog.widgets.text import Case, Const
from loguru import logger
from magic_filter import F
from sqlalchemy.ext.asyncio import AsyncSession

from database import User
from keyboards import create_language_buttons
from lexicon import LocalizedTextFormat, LANGUAGES, lexicon # Changed import


class LangSG(StatesGroup):
    """States for the language selection dialog."""
    select_lang = State()

async def get_languages(dialog_manager: DialogManager, **kwargs) -> dict:
    """
    Provides data for the language selection window.

    Args:
        dialog_manager: The dialog manager.
        **kwargs: Additional keyword arguments.

    Returns:
         A dictionary containing available languages. Key 'languages'.
    """
    return {"languages": LANGUAGES}

select_language = Window(
    LocalizedTextFormat("get_lang"), #  LocalizedTextFormat
    create_language_buttons(),
    state=LangSG.select_lang,
    getter=get_languages
)

language_dialog = Dialog(
    select_language
)

async def start_language_selection(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    """Starts the language selection dialog."""
    await dialog_manager.start(LangSG.select_lang)
    logger.debug(f"User {callback.from_user.id} started language selection.")
