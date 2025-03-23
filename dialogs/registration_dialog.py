from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram_dialog import Dialog, Window, DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button, Row, Cancel, Group, SwitchTo, Back
from aiogram_dialog.widgets.text import Const, Format, Case
from aiogram_dialog.widgets.input import TextInput
from magic_filter import F
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.models import User  # Import the *correct* User model
from dialogs.main_menu_dialog import MainMenuSG
from lexicon import lexicon, LocalizedTextFormat
from loguru import logger

class RegistrationSG(StatesGroup):
    """States for the registration dialog."""
    get_name = State()
    get_room = State()  # Get room number
    get_grade = State() # Add get_grade
    get_year = State()
    confirm = State()
    cancelled = State()

async def on_cancel(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    """Handles cancellation of the registration process."""
    logger.info(f"User {callback.from_user.id} canceled registration.")

async def restart_registration(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    """Handles register button (after cancellation) of the registration process."""
    await dialog_manager.start(RegistrationSG.get_name, mode=StartMode.RESET_STACK)
    logger.info(f"User {callback.from_user.id} restarted registration.")

async def get_name_handler(message: Message, widget: TextInput, dialog_manager: DialogManager, text: str):
    """Handles name input."""
    # Basic validation (you can add more)
    if not all(part.isalpha() or part.isspace() for part in text):
      await message.answer(lexicon(dialog_manager.middleware_data.get("lang"), "name_invalid"))
      return

    parts = text.split()
    if len(parts) < 2 or len(parts) > 3:
        await message.answer(lexicon(dialog_manager.middleware_data.get("lang"), "name_invalid"))
        return

    dialog_manager.dialog_data["first_name"] = parts[0]
    dialog_manager.dialog_data["last_name"] = parts[-1] # always the last
    if len(parts) == 3:
        dialog_manager.dialog_data["middle_name"] = parts[1]
    else:
        dialog_manager.dialog_data["middle_name"] = None # explicitly store None.

    await dialog_manager.switch_to(RegistrationSG.get_grade) # switch to grade selection
    logger.debug(f"User entered name: {text}")

async def get_room_handler(message: Message, widget: TextInput, dialog_manager: DialogManager, text: str):
    """Handles room number input."""

    # Basic validation: should be a string, possibly with letters.  Don't over-restrict.
    if not text:
        await message.answer(lexicon(dialog_manager.middleware_data.get("lang"), "room_invalid"))
        return
    dialog_manager.dialog_data["room_number"] = text
    await dialog_manager.next()
    logger.debug(f"User entered room: {text}")

# async def get_year_handler(message: Message, widget: TextInput, dialog_manager: DialogManager, text: str):
#     """Handles year of study input."""
#     if not text.isdigit() or not 1 <= int(text) <= 6: # check for valid range (adjust the 6 for your needs)
#       await message.answer(lexicon(dialog_manager.middleware_data.get("lang"), "year_invalid"))
#       return
#
#     dialog_manager.dialog_data["year"] = int(text)
#     await dialog_manager.next()

async def get_confirmation_data(dialog_manager: DialogManager, **kwargs) -> dict:
    """Prepares data for the confirmation window."""
    lang = dialog_manager.middleware_data.get("lang")
    data = {
      "first_name": dialog_manager.dialog_data.get("first_name"),
      "last_name": dialog_manager.dialog_data.get("last_name"),
      "room_number": dialog_manager.dialog_data.get("room_number"),
      "year": dialog_manager.dialog_data.get("year"),
      "grade": dialog_manager.dialog_data.get("grade"), # added
      "grade_loc": lexicon(lang, dialog_manager.dialog_data.get("grade"))
    }
    # Add middle name if it is given
    if dialog_manager.dialog_data.get("middle_name"):
        data["middle_name"] = dialog_manager.dialog_data.get("middle_name")
    else:
        data["middle_name"] = lexicon(lang, "not_specified")

    return data

async def on_confirm(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    """Handles confirmation of registration data."""
    session: AsyncSession = dialog_manager.middleware_data.get("session")
    lang = dialog_manager.middleware_data.get("lang")
    first_name = dialog_manager.dialog_data.get("first_name")
    last_name = dialog_manager.dialog_data.get("last_name")
    middle_name = dialog_manager.dialog_data.get("middle_name")
    room_number = dialog_manager.dialog_data.get("room_number")
    year = dialog_manager.dialog_data.get("year")
    grade = dialog_manager.dialog_data.get("grade")


    user = User(
        telegram_id=callback.from_user.id,
        first_name=first_name,
        last_name=last_name,
        middle_name=middle_name,
        room_number=room_number,
        year = year,
        grade = grade,
        lang=lang,
    )
    session.add(user)

    await session.commit()
    await callback.message.edit_text(lexicon(lang, 'registration_successful'))
    await dialog_manager.done()
    logger.info(f"Created new user: {user}")
    await dialog_manager.start(MainMenuSG.main, mode=StartMode.RESET_STACK)


get_name_window = Window(
    LocalizedTextFormat("registration_get_name"),
    TextInput(id="name_input", on_success=get_name_handler),
    SwitchTo(LocalizedTextFormat("cancel_button"), on_click=on_cancel, state=RegistrationSG.cancelled, id="cancel_registration"),
    state=RegistrationSG.get_name,
)

# Get grade window (reverted to button-based selection)
async def save_grade(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    """Handles grade selection."""
    dialog_manager.dialog_data["grade"] = button.widget_id  # Store the selected grade (e.g., "bachelor")
    await dialog_manager.next()
    logger.debug(f"User selected grade: {button.widget_id}")

get_grade_window = Window(
    LocalizedTextFormat("registration_get_grade"),  # Add this key to your lexicon
    Group(
        Button(LocalizedTextFormat("bachelor"), id="bachelor", on_click=save_grade),
        Button(LocalizedTextFormat("master"), id="master", on_click=save_grade),
        Button(LocalizedTextFormat("specialist"), id="specialist", on_click=save_grade),
        width=2
    ),
    Back(LocalizedTextFormat("back_button")),
    state=RegistrationSG.get_grade
)

# Get year window (reverted to button-based selection)
async def save_year(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
        dialog_manager.dialog_data["year"] = int(button.widget_id)
        await dialog_manager.switch_to(RegistrationSG.get_room)


get_year_window = Window(
    LocalizedTextFormat("registration_get_year"),  # Add this key to your lexicon
    Group(
        Button(Const("1"), id="1", on_click=save_year, when=F["dialog_data"]["grade"].in_(["bachelor", "master", "specialist"])),
        Button(Const("2"), id="2", on_click=save_year, when=F["dialog_data"]["grade"].in_(["bachelor", "master", "specialist"])),
        Button(Const("3"), id="3", on_click=save_year, when=F["dialog_data"]["grade"].in_(["bachelor", "specialist"])),
        Button(Const("4"), id="4", on_click=save_year, when=F["dialog_data"]["grade"].in_(["bachelor", "specialist"])),
        Button(Const("5"), id="5", on_click=save_year, when=F["dialog_data"]["grade"].in_(["specialist"])),
        Button(Const("6"), id="6", on_click=save_year, when=F["dialog_data"]["grade"].in_(["specialist"])),
        width=2
    ),
     Back(LocalizedTextFormat("back_button")),
    state=RegistrationSG.get_year
)

get_room_window = Window(
    LocalizedTextFormat("registration_get_room"),
    TextInput(id="room_input", on_success=get_room_handler),
    Back(LocalizedTextFormat("back_button")),
    state=RegistrationSG.get_room
)

confirm_window = Window(
    LocalizedTextFormat("registration_confirmation"),
    Row(
        Button(LocalizedTextFormat("confirm_button"), id="confirm_reg", on_click=on_confirm),
        SwitchTo(LocalizedTextFormat("back_button"), state=RegistrationSG.get_name, id="back_registration"),
    ),
    state=RegistrationSG.confirm,
    getter=get_confirmation_data
)

cancelled_window = Window(
    LocalizedTextFormat("registration_canceled"),
    Button(LocalizedTextFormat('register'), id='register_button', on_click=restart_registration),
    state=RegistrationSG.cancelled,
)

registration_dialog = Dialog(
    get_name_window,
    get_grade_window, # Added
    get_year_window,  # Added
    get_room_window,
    confirm_window,
    cancelled_window
)
