from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.text import Format

LEXICON: dict[str, dict[str, str]] = {
    'ru': {
        # Commands messages
        'start': 'Привет! Для начала давай познакомимся.',
        'start-registered': 'Снова привет, {name}!',
        'help': '* Здесь должна быть справка *',

        # Registration
        'get_lang': 'Выбери свой язык:',
        'get_name': 'Пожалуйста, введи свои ФИО (например, Иванов Иван Иванович):',
        'get_year': 'На каком курсе ты учишься?',
        'get_room': 'Введи номер своей комнаты:',
        'name_confirmation': '{dialog_data[last_name]} {dialog_data[first_name]} {dialog_data[middle_name]}, верно?',

        # Buttons
        'start_registration': 'Познакомиться',
        'select_language': 'Выбрать язык',

        # Service
        'throttling-warning': 'Обнаружена подозрительная активность! '
                              'Подожди 10 секунд прежде, чем писать снова.'
    },

    'en': {

    },

    'de': {

    },

    'es': {

    },

}


LEXICON_COMMANDS: dict[str, str] = {
    '/start': 'Старт',
    '/help': 'Помощь'
}

LANGUAGES = [
    {"code": "ru", "name": "Русский 🇷🇺"},
    {"code": "en", "name": "English 🇺🇸"},
    {"code": "de", "name": "Deutsch 🇩🇪"},
    {"code": "es", "name": "Español 🇪🇸"}
]

def lexicon(lang: str, key: str) -> str:
    # return LEXICON[f'{lang}'][key]
    return LEXICON['ru'][key]


class LocalizedTextFormat(Format):
    def __init__(self, key: str, default_lang="ru", **kwargs):
        super().__init__(text="", **kwargs)
        self.key = key
        self.default_lang = default_lang

    async def _render_text(
        self, data: dict, manager: DialogManager
    ) -> str:
        lang = manager.middleware_data.get("lang", self.default_lang)
        text = lexicon(lang, self.key)
        return text.format_map(data)
