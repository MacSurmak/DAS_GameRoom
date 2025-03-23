from aiogram.types import CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram_dialog import (
    Dialog, Window, DialogManager
)
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Group
from aiogram_dialog.widgets.text import Const
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.models import User
from dialogs.schedule_dialog import ScheduleDialogSG
from lexicon import lexicon, LocalizedTextFormat
from loguru import logger

class MainMenuSG(StatesGroup):
    main = State()

async def get_main_menu_data(dialog_manager: DialogManager, **kwargs) -> dict:
    """Retrieves data for the main menu."""
    lang = dialog_manager.middleware_data.get("lang")
    return {"lang": lang}

async def go_to_schedule(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    """Placeholder for going to the schedule view (to be implemented later)."""
    await dialog_manager.start(ScheduleDialogSG.resource_select)
    logger.info(f"User {callback.from_user.id} tried to access schedule (placeholder).")

main_menu_window = Window(
    LocalizedTextFormat("main_menu_header"),
    Group(
        Button(LocalizedTextFormat("view_schedule_button"), id="view_schedule_btn", on_click=go_to_schedule),
        # Add other buttons here later (e.g., "My Bookings")
        width=2
    ),
    state=MainMenuSG.main,
    getter=get_main_menu_data  # Make sure you have a getter
)

main_menu_dialog = Dialog(
    main_menu_window,
    # Add other windows later (e.g., schedule view, booking confirmation)
)
