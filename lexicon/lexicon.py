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
        'len_error0': 'Кажется, здесь чего-то не хватает. Пожалуйста, введи свои ФИО через пробел.',
        'len_error1': 'Кажется, здесь больше слов, чем нужно. Пожалуйста, введи свои ФИО через пробел.',
        'alpha_error': 'Кажется, здесь есть посторонние символы. Пожалуйста, введи свои ФИО через пробел.',
        'name_type_error': 'Это не похоже на имя. Пожалуйста, введи свои ФИО через пробел.',
        'name_confirmation': 'Фамилия: {dialog_data[last_name]}\n'
                             'Имя: {dialog_data[first_name]}\n'
                             'Отчество: {dialog_data[middle_name]}\n\nВерно?',

        'get_year': 'Выбери свою ступень обучения и курс.',

        'get_room': 'Введи номер своей комнаты:',
        'nan_error': 'Номер должен состоять только из цифр! Пожалуйста, повтори ввод:',
        'room_type_error': 'Это не похоже на номер. Пожалуйста, повтори ввод:',
        'room_invalid': 'Неверный номер комнаты! Пожалуйста, повтори ввод:',

        'confirm_data': '{dialog_data[last_name]} {dialog_data[first_name]} {dialog_data[middle_name]}\n'
                        '{dialog_data[grade_localized]}, {dialog_data[year]} курс\n'
                        'Комната {dialog_data[room]}\n\nВсё верно?',
        'complete': 'Теперь ты зарегистрирован(-а) в системе!',

        # Buttons
        'start_registration': 'Познакомиться',
        'select_language': 'Сменить язык',
        'bachelor': 'Бакалавриат',
        'specialist': 'Специалитет',
        'master': 'Магистратура',

        # Service buttons
        'yes': 'Да',
        'no': 'Нет',
        'back': '<<< Назад',
        'next': 'Далее >>>',
        'cancel': 'Отмена',

        # Service
        'throttling-warning': 'Обнаружена подозрительная активность! '
                              'Подожди 10 секунд прежде, чем писать снова.'
    },

    'en': {
        # Commands messages
        'start': 'Hello! Let\'s get acquainted to start.',
        'start-registered': 'Hello again, {name}!',
        'help': '* Help should be here *',

        # Registration
        'get_lang': 'Choose your language:',

        'get_name': 'Please enter your full name (e.g., John Doe Smith):',
        'len_error0': 'It seems something is missing. Please enter your full name separated by spaces.',
        'len_error1': 'It seems there are more words than needed. Please enter your full name separated by spaces.',
        'alpha_error': 'It seems there are extraneous characters. Please enter your full name separated by spaces.',
        'name_type_error': 'This doesn\'t look like a name. Please enter your full name separated by spaces.',
        'name_confirmation': 'Last Name: {dialog_data[last_name]}\n'
                             'First Name: {dialog_data[first_name]}\n'
                             'Middle Name: {dialog_data[middle_name]}\n\nCorrect?',

        'get_year': 'Select your study level and year.',

        'get_room': 'Enter your room number:',
        'nan_error': 'The number must consist of digits only! Please enter again:',
        'room_type_error': 'This doesn\'t look like a number. Please enter again:',
        'room_invalid': 'Invalid room number! Please enter again:',

        'confirm_data': '{dialog_data[last_name]} {dialog_data[first_name]} {dialog_data[middle_name]}\n'
                        '{dialog_data[grade_localized]}, Year {dialog_data[year]}\n'
                        'Room {dialog_data[room]}\n\nIs everything correct?',
        'complete': 'You are now registered in the system!',

        # Buttons
        'start_registration': 'Get acquainted',
        'select_language': 'Change language',
        'bachelor': 'Bachelor\'s',
        'specialist': 'Specialist',
        'master': 'Master\'s',

        # Service buttons
        'yes': 'Yes',
        'no': 'No',
        'back': '<<< Back',
        'next': 'Next >>>',
        'cancel': 'Cancel',

        # Service
        'throttling-warning': 'Suspicious activity detected! '
                              'Wait 10 seconds before writing again.'
    },

    'de': {
        # Commands messages
        'start': 'Hallo! Lass uns zum Start kennenlernen.',
        'start-registered': 'Hallo wieder, {name}!',
        'help': '* Hier sollte Hilfe stehen *',

        # Registration
        'get_lang': 'Wähle deine Sprache:',

        'get_name': 'Bitte gib deinen vollständigen Namen ein (z.B. Max Mustermann):',
        'len_error0': 'Es scheint, als würde etwas fehlen. Bitte gib deinen vollständigen Namen mit Leerzeichen getrennt ein.',
        'len_error1': 'Es scheint, als wären es mehr Wörter als nötig. Bitte gib deinen vollständigen Namen mit Leerzeichen getrennt ein.',
        'alpha_error': 'Es scheint, als wären fremde Zeichen vorhanden. Bitte gib deinen vollständigen Namen mit Leerzeichen getrennt ein.',
        'name_type_error': 'Das sieht nicht wie ein Name aus. Bitte gib deinen vollständigen Namen mit Leerzeichen getrennt ein.',
        'name_confirmation': 'Nachname: {dialog_data[last_name]}\n'
                             'Vorname: {dialog_data[first_name]}\n'
                             'Mittelname: {dialog_data[middle_name]}\n\nKorrekt?',

        'get_year': 'Wähle dein Studienniveau und dein Studienjahr.',

        'get_room': 'Gib deine Zimmernummer ein:',
        'nan_error': 'Die Nummer darf nur aus Ziffern bestehen! Bitte gib sie erneut ein:',
        'room_type_error': 'Das sieht nicht wie eine Nummer aus. Bitte gib sie erneut ein:',
        'room_invalid': 'Ungültige Zimmernummer! Bitte gib sie erneut ein:',

        'confirm_data': '{dialog_data[last_name]} {dialog_data[first_name]} {dialog_data[middle_name]}\n'
                        '{dialog_data[grade_localized]}, {dialog_data[year]}. Studienjahr\n'
                        'Zimmer {dialog_data[room]}\n\nIst alles korrekt?',
        'complete': 'Du bist jetzt im System registriert!',

        # Buttons
        'start_registration': 'Kennenlernen',
        'select_language': 'Sprache ändern',
        'bachelor': 'Bachelor',
        'specialist': 'Diplom',
        'master': 'Master',

        # Service buttons
        'yes': 'Ja',
        'no': 'Nein',
        'back': '<<< Zurück',
        'next': 'Weiter >>>',
        'cancel': 'Abbrechen',

        # Service
        'throttling-warning': 'Verdächtige Aktivität erkannt! '
                              'Warte 10 Sekunden, bevor du wieder schreibst.'
    },

    'es': {
        # Commands messages
        'start': '¡Hola! Para empezar, vamos a conocernos.',
        'start-registered': '¡Hola de nuevo, {name}!',
        'help': '* Aquí debería haber ayuda *',

        # Registration
        'get_lang': 'Elige tu idioma:',

        'get_name': 'Por favor, introduce tu nombre completo (ej. Juan Pérez García):',
        'len_error0': 'Parece que falta algo. Por favor, introduce tu nombre completo separado por espacios.',
        'len_error1': 'Parece que hay más palabras de las necesarias. Por favor, introduce tu nombre completo separado por espacios.',
        'alpha_error': 'Parece que hay caracteres extraños. Por favor, introduce tu nombre completo separado por espacios.',
        'name_type_error': 'Esto no parece un nombre. Por favor, introduce tu nombre completo separado por espacios.',
        'name_confirmation': 'Apellido: {dialog_data[last_name]}\n'
                             'Nombre: {dialog_data[first_name]}\n'
                             'Segundo nombre: {dialog_data[middle_name]}\n\n¿Correcto?',

        'get_year': 'Selecciona tu nivel de estudios y curso.',

        'get_room': 'Introduce tu número de habitación:',
        'nan_error': '¡El número debe contener solo dígitos! Por favor, inténtalo de nuevo:',
        'room_type_error': 'Esto no parece un número. Por favor, inténtalo de nuevo:',
        'room_invalid': '¡Número de habitación no válido! Por favor, inténtalo de nuevo:',

        'confirm_data': '{dialog_data[last_name]} {dialog_data[first_name]} {dialog_data[middle_name]}\n'
                        '{dialog_data[grade_localized]}, Curso {dialog_data[year]}\n'
                        'Habitación {dialog_data[room]}\n\n¿Todo correcto?',
        'complete': '¡Ahora estás registrado(-a) en el sistema!',

        # Buttons
        'start_registration': 'Conocer',
        'select_language': 'Cambiar idioma',
        'bachelor': 'Grado',
        'specialist': 'Especialidad',
        'master': 'Máster',

        # Service buttons
        'yes': 'Sí',
        'no': 'No',
        'back': '<<< Atrás',
        'next': 'Siguiente >>>',
        'cancel': 'Cancelar',

        # Service
        'throttling-warning': '¡Se ha detectado actividad sospechosa! '
                              'Espera 10 segundos antes de volver a escribir.'
    },

    'fr': {
        # Commands messages
        'start': 'Bonjour ! Pour commencer, faisons connaissance.',
        'start-registered': 'Bonjour encore, {name} !',
        'help': '* L\'aide devrait être ici *',

        # Registration
        'get_lang': 'Choisissez votre langue :',

        'get_name': 'Veuillez entrer votre nom complet (par exemple, Jean Dupont Martin) :',
        'len_error0': 'Il semble que quelque chose manque. Veuillez entrer votre nom complet séparé par des espaces.',
        'len_error1': 'Il semble qu\'il y ait plus de mots que nécessaire. Veuillez entrer votre nom complet séparé par des espaces.',
        'alpha_error': 'Il semble qu\'il y ait des caractères étrangers. Veuillez entrer votre nom complet séparé par des espaces.',
        'name_type_error': 'Cela ne ressemble pas à un nom. Veuillez entrer votre nom complet séparé par des espaces.',
        'name_confirmation': 'Nom de famille : {dialog_data[last_name]}\n'
                             'Prénom : {dialog_data[first_name]}\n'
                             'Deuxième prénom : {dialog_data[middle_name]}\n\nCorrect ?',

        'get_year': 'Sélectionnez votre niveau d\'études et votre année.',

        'get_room': 'Entrez votre numéro de chambre :',
        'nan_error': 'Le numéro doit être composé uniquement de chiffres ! Veuillez réessayer :',
        'room_type_error': 'Cela ne ressemble pas à un numéro. Veuillez réessayer :',
        'room_invalid': 'Numéro de chambre invalide ! Veuillez réessayer :',

        'confirm_data': '{dialog_data[last_name]} {dialog_data[first_name]} {dialog_data[middle_name]}\n'
                        '{dialog_data[grade_localized]}, {dialog_data[year]} année\n'
                        'Chambre {dialog_data[room]}\n\nEst-ce correct ?',
        'complete': 'Vous êtes maintenant enregistré(e) dans le système !',

        # Buttons
        'start_registration': 'Faire connaissance',
        'select_language': 'Changer de langue',
        'bachelor': 'Licence',
        'specialist': 'Spécialiste',
        'master': 'Master',

        # Service buttons
        'yes': 'Oui',
        'no': 'Non',
        'back': '<<< Retour',
        'next': 'Suivant >>>',
        'cancel': 'Annuler',

        # Service
        'throttling-warning': 'Activité suspecte détectée ! '
                              'Veuillez attendre 10 secondes avant d\'écrire à nouveau.'
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
    {"code": "es", "name": "Español 🇪🇸"},
    {"code": "fr", "name": "Français 🇫🇷"}
]

def lexicon(lang: str, key: str) -> str:
    return LEXICON[f'{lang}'][key]
    # return LEXICON["ru"][key]


class LocalizedTextFormat(Format):
    def __init__(self, key: str, **kwargs):
        super().__init__(text="", **kwargs)
        self.key = key

    async def _render_text(self, data: dict, manager: DialogManager) -> str:
        lang = manager.middleware_data.get("lang")
        text = lexicon(lang, self.key)
        return text.format_map(data)
