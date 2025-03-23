from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from dialogs.main_menu_dialog import MainMenuSG  # Import the new dialog
from lexicon import lexicon
from filters.filters import IsRegistered
from dialogs.registration_dialog import RegistrationSG
from database import User

commands_router: Router = Router(name='commands-router')

@commands_router.message(CommandStart(), ~IsRegistered())
async def start_new_user(message: Message, dialog_manager: DialogManager):
    """Handles /start for new users (not registered)."""
    await dialog_manager.start(RegistrationSG.get_name, mode=StartMode.RESET_STACK)
    logger.info("Starting registration for new user")

@commands_router.message(CommandStart(), IsRegistered())
async def start_registered_user(message: Message, dialog_manager: DialogManager, session: AsyncSession, lang: str):
    """Handles /start for registered users."""

    # Check if the user exists (should always be true because of the filter, but good practice)
    user: User | None = await session.execute(select(User).where(User.telegram_id == message.from_user.id))
    user = user.scalar_one_or_none()

    if user:
        await dialog_manager.start(MainMenuSG.main, mode=StartMode.RESET_STACK)
        logger.info(f"User {message.from_user.id} started main menu.")
    else:
        # This *shouldn't* happen, but handle it just in case
        await message.answer(lexicon(lang, "user_not_found_response"))  # You'll need this lexicon key
        logger.error(f"User {message.from_user.id} triggered start_registered but is not in the database!")
        # Consider restarting registration, or sending them to the main menu anyway.
        await dialog_manager.start(MainMenuSG.main, mode=StartMode.RESET_STACK)

@commands_router.message(Command("menu"), IsRegistered())
async def menu_command(message: Message, dialog_manager: DialogManager):
    """Handles the /menu command."""
    await dialog_manager.start(MainMenuSG.main, mode=StartMode.RESET_STACK)
    logger.info(f"User {message.from_user.id} activated main menu")


@commands_router.message(Command("help"))
async def help_command(message: Message, session: AsyncSession, lang: str):
    """Handles the /help command."""
    await message.answer(lexicon(lang, 'help_command_response'))
    logger.info(f"User {message.from_user.id} requested help")
