from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.text import Format

LEXICON: dict[str, dict[str, str]] = {
    'ru': {
        # Commands messages
        'start': 'Привет!',
        'start-registered': 'Снова привет, {name}!',
        'help': 'Помощь',

        # Registration
        'get_lang': 'Выбери свой язык:',
        'get_name': 'Пожалуйста, введи своё имя:',

        # Buttons
        'start_registration': 'Зарегистрироваться',
        'select_language': 'Выбрать язык',


        # Service
        'throttling-warning': 'Обнаружена подозрительная активность! '
                              'Подожди 10 секунд прежде, чем писать снова.'
    },

    'en': {
        # Commands messages
        'start': 'Hello!',
        'start-registered': 'Hello again, {name}!',
        'help': 'Help',

        # Registration
        'get_lang': 'Select your language:',
        'get_name': 'Please, enter your name:',

        # Buttons
        'start_registration': 'Register',
        'select_language': 'Select language',

        # Service
        'throttling-warning': 'Suspicious activity detected! '
                              'Wait 10 seconds before writing again.'
    },

    'de': {
        # Commands messages
        'start': 'Hallo!',
        'start-registered': 'Hallo wieder, {name}!',
        'help': 'Hilfe',

        # Registration
        'get_lang': 'Wähle deine Sprache:',
        'get_name': 'Bitte gib deinen Namen ein:',

        # Buttons
        'start_registration': 'Registrieren',
        'select_language': 'Sprache auswählen',

        # Service
        'throttling-warning': 'Verdächtige Aktivität erkannt! '
                              'Warte 10 Sekunden, bevor du wieder schreibst.'
    },

    'es': {
        # Commands messages
        'start': '¡Hola!',
        'start-registered': '¡Hola de nuevo, {name}!',
        'help': 'Ayuda',

        # Registration
        'get_lang': 'Selecciona tu idioma:',
        'get_name': 'Por favor, introduce tu nombre:',

        # Buttons
        'start_registration': 'Registrarse',
        'select_language': 'Seleccionar idioma',

        # Service
        'throttling-warning': '¡Actividad sospechosa detectada! '
                              'Espera 10 segundos antes de volver a escribir.'
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
    return LEXICON[f'{lang}'][key]


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
