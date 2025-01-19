LEXICON: dict[str, dict[str, str]] = {
    'ru': {
        # Commands messages
        '/start': 'Привет!',
        '/help': 'Помощь',

        'throttling-warning': 'Обнаружена подозрительная активность! '
                              'Подожди 10 секунд прежде, чем писать снова.'
    },

    'en': {
        # Commands messages
        '/start': 'Hello!',
        '/help': 'Help',

        'throttling-warning': 'Suspicious activity detected! '
                              'Wait 10 seconds before writing again.'
    },
}


LEXICON_COMMANDS: dict[str, str] = {
    '/start': 'Старт',
    '/help': 'Помощь'
}


def lexicon(lang: str, key: str) -> str:
    if lang == 'ru':
        return LEXICON['ru'][key]
    elif lang == 'en':
        return LEXICON['en'][key]
    else:
        return LEXICON['en'][key]
