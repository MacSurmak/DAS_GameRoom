from aiogram.fsm.state import StatesGroup, State


class LangSG(StatesGroup):
    select_lang = State()

class RegistrationSG(StatesGroup):
    start = State()
    get_name = State()
    confirm_data  = State()
    complete = State()
