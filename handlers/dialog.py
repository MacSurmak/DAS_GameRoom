from typing import Any

from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from aiogram_dialog import Window, Dialog, DialogManager, Data
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button, Next, Row, SwitchTo, Group
from aiogram_dialog.widgets.text import Case, Const
from magic_filter import F
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
    get_grade = State()
    get_year = State()
    year_incorrect = State()
    get_room = State()
    room_incorrect = State()
    confirm_data  = State()
    complete = State()


async def get_languages(dialog_manager: DialogManager, **kwargs):
    return {"languages": LANGUAGES}

language_dialog = Dialog(
    Window(
        LocalizedTextFormat("get_lang"),
        create_language_buttons(),
        state=LangSG.select_lang,
        getter=get_languages
    )
)

async def start_language_selection(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.start(LangSG.select_lang)

async def process_name(message: Message, widget: MessageInput, dialog_manager: DialogManager):
    if not message.text:
        dialog_manager.dialog_data["name_error"] = "type_error"
        await dialog_manager.switch_to(RegistrationSG.name_incorrect)
        return
    if not message.text.replace(' ', '').isalpha():
        dialog_manager.dialog_data["name_error"] = "alpha_error"
        await dialog_manager.switch_to(RegistrationSG.name_incorrect)
        return
    text = message.text.split()
    if len(text) < 2:
        dialog_manager.dialog_data["name_error"] = "len_error0"
        await dialog_manager.switch_to(RegistrationSG.name_incorrect)
        return
    if len(text) > 3:
        dialog_manager.dialog_data["name_error"] = "len_error1"
        await dialog_manager.switch_to(RegistrationSG.name_incorrect)
        return
    dialog_manager.dialog_data["last_name"] = text[0]
    dialog_manager.dialog_data["first_name"] = text[1]
    dialog_manager.dialog_data["middle_name"] = text[2] if len(text) == 3 else None
    await dialog_manager.switch_to(RegistrationSG.name_confirmation)

async def save_year(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    if button.widget_id.isalpha():
        dialog_manager.dialog_data["grade"] = button.widget_id
        await dialog_manager.switch_to(RegistrationSG.get_year)
    else:
        dialog_manager.dialog_data["year"] = button.widget_id
        await dialog_manager.switch_to(RegistrationSG.get_room)

registration_dialog = Dialog(
    Window(
        LocalizedTextFormat("start"),
        Button(LocalizedTextFormat("start_registration"), id="start_reg", on_click=Next()),
        Button(LocalizedTextFormat("select_language"), id="select_lang", on_click=start_language_selection),
        state=RegistrationSG.start
    ),
    Window(
        LocalizedTextFormat("get_name"),
        MessageInput(process_name),
        SwitchTo(LocalizedTextFormat("cancel"), id="back", state=RegistrationSG.start),
        state=RegistrationSG.get_name
    ),
    Window(
        Case(
            {"len_error0": LocalizedTextFormat("len_error0"),
             "len_error1": LocalizedTextFormat("len_error1"),
             "alpha_error": LocalizedTextFormat("alpha_error"),
             "type_error": LocalizedTextFormat("type_error")},
            selector=F["dialog_data"]["name_error"]
        ),
        MessageInput(process_name),
        SwitchTo(LocalizedTextFormat("cancel"), id="back", state=RegistrationSG.start),
        state=RegistrationSG.name_incorrect
    ),
    Window(
        LocalizedTextFormat("name_confirmation"),
        Row(
            Button(LocalizedTextFormat("yes"), id="yes", on_click=Next()),
            SwitchTo(LocalizedTextFormat("no"), id="no", state=RegistrationSG.get_name)
        ),
        state=RegistrationSG.name_confirmation
    ),
    Window(
        LocalizedTextFormat("get_year"),
        Group(
            Button(LocalizedTextFormat("bachelor"), id="bachelor", on_click=save_year),
            Button(LocalizedTextFormat("master"), id="master", on_click=save_year),
            Button(LocalizedTextFormat("specialist"), id="specialist", on_click=save_year),
            width=2
        ),
        SwitchTo(LocalizedTextFormat("back"), id="back", state=RegistrationSG.name_confirmation),
        state=RegistrationSG.get_grade
    ),
    Window(
        LocalizedTextFormat("get_year"),
        Group(
            Button(Const("1"), id="1", on_click=save_year, when=F["dialog_data"]["grade"].in_(["bachelor", "master", "specialist"])),
            Button(Const("2"), id="2", on_click=save_year, when=F["dialog_data"]["grade"].in_(["bachelor", "master", "specialist"])),
            Button(Const("3"), id="3", on_click=save_year, when=F["dialog_data"]["grade"].in_(["bachelor", "specialist"])),
            Button(Const("4"), id="4", on_click=save_year, when=F["dialog_data"]["grade"].in_(["bachelor", "specialist"])),
            Button(Const("5"), id="5", on_click=save_year, when=F["dialog_data"]["grade"].in_(["specialist"])),
            Button(Const("6"), id="6", on_click=save_year, when=F["dialog_data"]["grade"].in_(["specialist"])),
            width=2
        ),
        SwitchTo(LocalizedTextFormat("back"), id="back", state=RegistrationSG.get_grade),
        state=RegistrationSG.get_year
    ),
    Window(
        LocalizedTextFormat("get_room"),
        TextInput(id="room", on_success=Next()),
        state=RegistrationSG.get_room
    )
)
