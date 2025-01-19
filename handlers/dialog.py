from aiogram.types import CallbackQuery

from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button, Next
from sqlalchemy.ext.asyncio import AsyncSession

from database import UserBase
from handlers.states import LangSG, RegistrationSG
from keyboards import create_language_buttons
from lexicon import LocalizedTextFormat, LANGUAGES


async def get_languages(dialog_manager: DialogManager, **kwargs):
    return {
        "languages": LANGUAGES
    }

async def start_language_selection(callback: CallbackQuery, button: Button,
                          manager: DialogManager):
    await manager.start(LangSG.select_lang)

language_dialog = Dialog(
    Window(
        LocalizedTextFormat("get_lang"),
        create_language_buttons(),
        state=LangSG.select_lang,
        getter=get_languages
    )
)

registration_dialog = Dialog(
    Window(
        LocalizedTextFormat("start"),
        Button(LocalizedTextFormat("start_registration"), id="start_reg", on_click=Next()),
        Button(LocalizedTextFormat("select_language"), id="select_lang", on_click=start_language_selection),
        state=RegistrationSG.start
    ),
    Window(
        LocalizedTextFormat("get_name"),
        TextInput(id="name", on_success=Next()),
        state=RegistrationSG.get_name
    )
)
