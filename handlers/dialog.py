from aiogram import Router
from aiogram.filters.state import State, StatesGroup

from aiogram_dialog import Window, Dialog, DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const


class MySG(StatesGroup):
    main = State()

dialog_router: Router = Router(name='dialog-router')

main_window = Window(
    Const("Hello, unknown person"),  # just a constant text
    Button(Const("Useless button"), id="nothing"),  # button with text and id
    state=MySG.main,  # state is used to identify window between dialogs
)
dialog = Dialog(main_window)
