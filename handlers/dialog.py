from typing import Any

from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from aiogram_dialog import Window, Dialog, DialogManager, Data
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import Button, Next
from sqlalchemy.ext.asyncio import AsyncSession

from database import UserBase
from keyboards import create_language_buttons
from lexicon import LocalizedTextFormat, LANGUAGES


class LangSG(StatesGroup):
    select_lang = State()

class RegistrationSG(StatesGroup):
    start = State()
    get_name = State()
    name_incorrect = State()
    name_confirmation = State()
    get_year = State()
    year_incorrect = State()
    get_room = State()
    room_incorrect = State()
    confirm_data  = State()
    complete = State()


async def get_languages(dialog_manager: DialogManager, **kwargs):
    return {
        "languages": LANGUAGES
    }

language_dialog = Dialog(
    Window(
        LocalizedTextFormat("get_lang"),
        create_language_buttons(),
        state=LangSG.select_lang,
        getter=get_languages
    )
)

async def start_language_selection(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.start(LangSG.select_lang)

async def process_name(message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, data: Data):
    text = data.split()
    dialog_manager.dialog_data["last_name"] = text[0]
    dialog_manager.dialog_data["first_name"] = text[1]
    dialog_manager.dialog_data["middle_name"] = text[2] if len(text) == 3 else None
    await dialog_manager.switch_to(RegistrationSG.name_confirmation)

registration_dialog = Dialog(
    Window(
        LocalizedTextFormat("start"),
        Button(LocalizedTextFormat("start_registration"), id="start_reg", on_click=Next()),
        Button(LocalizedTextFormat("select_language"), id="select_lang", on_click=start_language_selection),
        state=RegistrationSG.start
    ),
    Window(
        LocalizedTextFormat("get_name"),
        TextInput(id="name", on_success=process_name),
        state=RegistrationSG.get_name
    ),
    Window(
        LocalizedTextFormat("name_confirmation"),
        TextInput(id="name_confirmation", on_success=Next()),
        state=RegistrationSG.name_confirmation
    ),
    Window(
        LocalizedTextFormat("get_year"),
        TextInput(id="year", on_success=Next()),
        state=RegistrationSG.get_year
    ),
    Window(
        LocalizedTextFormat("get_room"),
        TextInput(id="room", on_success=Next()),
        state=RegistrationSG.get_room
    )
)
