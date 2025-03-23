from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.text import Format
from loguru import logger

LEXICON: dict[str, dict[str, str]] = {
    'ru': {
        # General Messages (Общие сообщения)
        'start_command_response': '👋 Привет! Я бот для бронирования помещений в общежитии.', # Changed
        'help_command_response': 'ℹ️ Вот что я умею:\n\n'
                                 '/start – Начать.\n'
                                 '/help – Помощь.\n'
                                 '/menu – Открыть главное меню.\n',
        'user_not_found_response': '🤔 Кажется, Вы ещё не зарегистрированы. Для начала работы нужно пройти регистрацию.',
        'random-message-response': '🤖 Не понимаю это сообщение. Пожалуйста, выберите команду из меню.',

        # Registration (dialogs/registration_dialog.py) - Регистрация
        'registration_get_name': "📝 Введите ваше ФИО (Фамилию Имя Отчество):",
        'registration_get_room': "🚪 Введите номер вашей комнаты:",
        'registration_get_year': "📅 Выберите вашу ступень обучения и курс:", # Changed
        'registration_successful': '✅ Отлично, регистрация завершена!',
        'registration_canceled': '↩️ Регистрация отменена.',
        'registration_confirmation': "👀 Проверяем:\nФамилия: {last_name}\nИмя: {first_name}\n"
                                     "Отчество: {middle_name}\nКомната: {room_number}\n"
                                     "Ступень: {grade_loc}\nКурс: {year}\n\nВсё верно?", # Changed
        'name_invalid': "❌ Некорректное ФИО. Пожалуйста, введите Фамилию, Имя и Отчество (если есть) через пробел.",
        'room_invalid': "❌ Некорректный номер комнаты. Пожалуйста, введите номер комнаты.",
        'year_invalid': "❌ Некорректный курс. Пожалуйста, введите число от 1 до 6.",
        'not_specified': "Не указано",

        # --- Grades ---
        'bachelor': 'Бакалавриат',
        'master': 'Магистратура',
        'specialist': 'Специалитет',

        # --- Common Buttons ---
        'back_button': '⬅️ Назад',
        'cancel_button': '❌ Отмена',
        'confirm_button': '✅ Да',
        'register': 'Регистрация',

        # --- Main Menu ---
        'main_menu_header': '🏠 Главное меню',
        'view_schedule_button': '📅 Посмотреть расписание',

        # --- Schedule Dialog ---
        "select_date": "📅 Выберите дату:",
        "select_time": "📅 Выберите время:",
        "select_duration": "⏱️ Выберите длительность бронирования:", # New
        'booking_confirm': "Подтвердите бронирование:\nПомещение: {resource_name}\nДата: {selected_date}\nВремя: {start_time} - {end_time}",
        "one_hour" : "1 час",
        "two_hours" : "2 часа",
        "three_hours" : "3 часа",
        "booking_created": "✅ Бронирование создано! Ожидайте подтверждения администратора.",
        "booking_failed" : "❌ Не удалось создать бронирование.  Слот уже занят.",
        'available_slots': "Доступные слоты ({resource_name}, {selected_date}):", # Key for slots
        'no_slots_available': "Нет доступных слотов",

        # --- Throttling ---
        'throttling-warning': '🛑 Слишком много сообщений! Пожалуйста, подождите немного.',
    }
}


LEXICON_COMMANDS: dict[str, str] = {
    '/start': 'Старт',
    '/help': 'Помощь',
    '/menu': 'Главное меню'
}

LANGUAGES = [
    {"code": "ru", "name": "Русский 🇷🇺"},
]

DEFAULT_LANG = "ru"

def lexicon(lang: str, key: str) -> str:
    """
    Retrieves a localized string from the lexicon.

    Args:
        lang: The language code (e.g., "ru" or "en").
        key: The key for the desired string.

    Returns:
        The localized string.  If the language or key is not found,
        it logs an error and returns the key itself as a fallback.

    Raises:
        KeyError:  If the key is not found, *after* logging the error.  This
                   is a change from the original, making it more robust.
    """
    try:
        return LEXICON[lang][key]
    except KeyError:
        logger.warning(f"Missing lexicon key for language '{lang}': {key}. Trying default language '{DEFAULT_LANG}'.")
        try:
            return LEXICON[DEFAULT_LANG][key]
        except KeyError:
            logger.error(f"Missing lexicon key in default language '{DEFAULT_LANG}': {key}. Returning key as fallback.")
            return key  # Return the key as a fallback
    except Exception as ex:
        logger.exception(f"An unexpected error occurred in lexicon function: {ex}")
        raise


class LocalizedTextFormat(Format):
    """
    Custom text formatting class for localized strings.  This class
    fetches strings from the lexicon based on the user's language.
    """
    def __init__(self, key: str, **kwargs):
        super().__init__(text="", **kwargs)  # Initialize with empty text
        self.key = key

    async def _render_text(self, data: dict, manager: DialogManager) -> str:
        lang = manager.middleware_data.get("lang")
        text = lexicon(lang, self.key)
        return text.format_map(data)
