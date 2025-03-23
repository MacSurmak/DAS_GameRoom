import datetime

from aiogram.types import CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram_dialog import (
    Dialog, Window, DialogManager, StartMode
)
from aiogram_dialog.widgets.kbd import Button, Select, Group, Calendar, Back, SwitchTo, Row, ListGroup
from aiogram_dialog.widgets.text import Const, Format
from magic_filter import F
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Resource, Booking, User # Import Booking
from services.schedule_service import get_available_slots, get_resource_name_by_id, is_slot_available
from lexicon import LocalizedTextFormat, lexicon
from loguru import logger

class ScheduleDialogSG(StatesGroup):
    resource_select = State()
    date_select = State()
    slot_select = State()
    duration_select = State()
    booking_confirm = State()

# --- Data Getters ---
async def get_resources_data(dialog_manager: DialogManager, **kwargs) -> dict:
    session: AsyncSession = dialog_manager.middleware_data.get("session")
    resources = await session.execute(select(Resource))
    resources = resources.scalars().all()
    return {
        "resources": [(r.resource_name, r.resource_id) for r in resources],
    }

async def get_selected_resource_name(dialog_manager: DialogManager, **kwargs) -> dict:
  session: AsyncSession = dialog_manager.middleware_data.get("session")
  resource_id = dialog_manager.dialog_data.get("selected_resource_id")
  resource_name = await get_resource_name_by_id(session, resource_id)
  return {"resource_name": resource_name}


async def get_slots_data(dialog_manager: DialogManager, **kwargs) -> dict:
    session: AsyncSession = dialog_manager.middleware_data.get("session")
    resource_id = dialog_manager.dialog_data.get("selected_resource_id")
    selected_date_str: str = dialog_manager.dialog_data.get("selected_date") # Get as string
    selected_date = datetime.date.fromisoformat(selected_date_str) # Convert to date
    available_slots = await get_available_slots(session, resource_id, selected_date)
    # Format slots for display (list of tuples (text, data))
    formatted_slots = [
        {"time_str": start.strftime('%H:%M'), "start_time": start.isoformat()}
        for start in available_slots
    ]

    return {
        "resource_name": await get_resource_name_by_id(session, resource_id),
        "selected_date": selected_date.strftime("%Y-%m-%d"),
        "available_slots": formatted_slots,
        "has_slots": bool(available_slots)  # Check if there are any slots
    }

async def get_booking_confirm_data(dialog_manager: DialogManager, **kwargs) -> dict:
    session: AsyncSession = dialog_manager.middleware_data.get("session")
    resource_id = dialog_manager.dialog_data.get("selected_resource_id")
    resource_name = await get_resource_name_by_id(session, resource_id)
    selected_date_str: str = dialog_manager.dialog_data.get("selected_date") # Get as string
    selected_date = datetime.date.fromisoformat(selected_date_str)       # Convert to date
    start_time_str: str = dialog_manager.dialog_data.get("selected_start_time")  # Get as string
    start_time = datetime.time.fromisoformat(start_time_str) # Convert to time
    duration: int = dialog_manager.dialog_data.get("selected_duration")

    # Calculate end time
    end_time = (datetime.datetime.combine(datetime.date.min, start_time) + datetime.timedelta(hours=duration)).time()

    return {
        "resource_name": resource_name,
        "selected_date": selected_date.strftime("%Y-%m-%d"),
        "start_time": start_time.strftime("%H:%M"),
        "end_time": end_time.strftime("%H:%M"),
    }

async def get_duration_data(dialog_manager: DialogManager, **kwargs) -> dict:
  lang = dialog_manager.middleware_data.get("lang")
  return {
    "one_hour": lexicon(lang, "one_hour"),
    "two_hours": lexicon(lang, "two_hours"),
    "three_hours": lexicon(lang, "three_hours")
}

# --- Callback Handlers ---

async def on_resource_selected(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager,
                               selected_item_id: str):
    dialog_manager.dialog_data["selected_resource_id"] = int(selected_item_id)
    await dialog_manager.switch_to(ScheduleDialogSG.date_select)

async def on_date_selected(callback: CallbackQuery, widget, dialog_manager: DialogManager,
                           selected_date: datetime.date):
    dialog_manager.dialog_data["selected_date"] = selected_date.isoformat() # Store as ISO string
    await dialog_manager.switch_to(ScheduleDialogSG.slot_select)

async def on_slot_selected(callback: CallbackQuery, button: Button, dialog_manager: DialogManager,
                                *args):
    # Store selected start time (already a string).  The button's ID *is* the start time.
    start_time_str = button.widget_id
    logger.debug(f"on_slot_selected: User {callback.from_user.id} clicked. button_id (start_time): {start_time_str}")  # Add logging
    dialog_manager.dialog_data["selected_start_time"] = start_time_str # Store as string
    logger.debug(f"on_slot_selected: dialog_data after storing start_time: {dialog_manager.dialog_data}") # Add logging
    try:
        await dialog_manager.switch_to(ScheduleDialogSG.duration_select) # Go to duration select
        logger.debug("on_slot_selected: switch_to successful")
    except Exception as e:
        logger.exception(f"on_slot_selected: switch_to failed: {e}")


async def on_duration_selected(callback: CallbackQuery, widget: Select, dialog_manager: DialogManager,
                               selected_item_id: str):
    dialog_manager.dialog_data["selected_duration"] = int(selected_item_id)
    await dialog_manager.switch_to(ScheduleDialogSG.booking_confirm)


async def on_booking_confirmed(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    session: AsyncSession = dialog_manager.middleware_data.get("session")
    user_id = callback.from_user.id
    resource_id = dialog_manager.dialog_data.get("selected_resource_id")
    booking_date_str: str = dialog_manager.dialog_data.get("selected_date")
    booking_date = datetime.date.fromisoformat(booking_date_str) # convert to date
    start_time_str: str = dialog_manager.dialog_data.get("selected_start_time")
    start_time = datetime.time.fromisoformat(start_time_str) # convert to time

    duration: int = dialog_manager.dialog_data.get("selected_duration")
    end_time = (datetime.datetime.combine(datetime.date.min, start_time) + datetime.timedelta(hours=duration)).time()

    # **CRITICAL: Check availability BEFORE creating the booking**
    if await is_slot_available(session, resource_id, booking_date, start_time, end_time):
        # Create the booking
        new_booking = Booking(
            user_id=user_id,
            resource_id=resource_id,
            booking_date=booking_date,
            start_time=start_time,
            end_time=end_time,
            status='pending'
        )
        session.add(new_booking)
        await session.commit()
        await callback.message.answer(lexicon(dialog_manager.middleware_data.get("lang"), "booking_created"))
        logger.info(f"Booking created: user {user_id}, resource {resource_id}, date {booking_date}, time {start_time}-{end_time}")

        # Clear dialog data and close
        dialog_manager.dialog_data.pop("selected_resource_id", None)
        dialog_manager.dialog_data.pop("selected_date", None)
        dialog_manager.dialog_data.pop("selected_start_time", None)
        dialog_manager.dialog_data.pop("selected_duration", None)
        await dialog_manager.done()

        # TODO: Send notification to admins (implementation in next step)

    else:
        # Slot is no longer available
        await callback.message.answer(lexicon(dialog_manager.middleware_data.get("lang"), "booking_failed"))
        logger.info(f"Booking failed (slot unavailable): user {user_id}, resource {resource_id}, date {booking_date}, time {start_time}-{end_time}")
        await dialog_manager.switch_to(ScheduleDialogSG.slot_select)  # Return to slot selection


# --- Dialog Windows ---

resource_select_window = Window(
    LocalizedTextFormat("select_resource"),
    Select(
        Format("{item[0]}"),  # Display resource name
        id="resource_select",
        item_id_getter=lambda item: item[1],  # Use resource ID as the data
        items="resources",
        on_click=on_resource_selected,
    ),
    state=ScheduleDialogSG.resource_select,
    getter=get_resources_data,
)

date_select_window = Window(
    LocalizedTextFormat("select_date"),
    Calendar(id="calendar", on_click=on_date_selected),
      SwitchTo(
      LocalizedTextFormat("back_button"),
      id="back_to_resource",
      state=ScheduleDialogSG.resource_select
    ),
    state=ScheduleDialogSG.date_select,
    getter=get_selected_resource_name
)

slot_select_window = Window(
    LocalizedTextFormat("available_slots"),
    Group(
        ListGroup(
            Button(
                Format("{item[time_str]}"),
                id="slot_select",
                on_click=on_slot_selected,
            ),
            id="slot_list_group",
            item_id_getter=lambda item: item["start_time"],
            items="available_slots"
        ),
        width=3,
    ),
    SwitchTo(
        LocalizedTextFormat("back_button"),
        id="back_to_date",
        state=ScheduleDialogSG.date_select
    ),
    Const("Нет доступных слотов", when=~F["has_slots"]),
    state=ScheduleDialogSG.slot_select,
    getter=get_slots_data,
)

duration_select_window = Window(
    LocalizedTextFormat("select_duration"),
    Select(
        Format("{item[0]}"),
        id="duration_select",
        item_id_getter=lambda item: item[1],
        items=[
            ("one_hour", "1"), # added to lexicon
            ("two_hours", "2"),
            ("three_hours", "3")
        ],
        on_click=on_duration_selected,
    ),
    Back(LocalizedTextFormat("back_button")),
    state=ScheduleDialogSG.duration_select,
    getter=get_duration_data  # Add the getter here
)


booking_confirm_window = Window(
    LocalizedTextFormat("booking_confirm"),
    Group(
      Button(LocalizedTextFormat("confirm_button"), id="confirm_booking", on_click=on_booking_confirmed),
      Back(LocalizedTextFormat("back_button"))
    ),
    state=ScheduleDialogSG.booking_confirm,
    getter=get_booking_confirm_data
)

schedule_dialog = Dialog(
    resource_select_window,
    date_select_window,
    slot_select_window,
    duration_select_window,
    booking_confirm_window,
)
