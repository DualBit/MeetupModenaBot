import requests
from json import JSONDecodeError
from telegram import ParseMode
from telegram.ext import Updater, MessageHandler, Filters

from constants import TG_API_KEY, LUIS_START_KEY, LUIS_START_URL, LUIS_APP_ID, PRETTY_OUTPUT

# region parametri request LUIS
headers = {
    'Ocp-Apim-Subscription-Key': LUIS_START_KEY,
}

base_params = {
    'q': '',
    'timezoneOffset': '0',
    'verbose': 'true',
    'spellCheck': 'false',
    'staging': 'true',
}
# endregion


def get_luis_data(message):
    try:
        req_params = dict(base_params, **{'q': message})
        r = requests.get(
            url='{0}/{1}'.format(LUIS_START_URL, LUIS_APP_ID),
            headers=headers,
            params=req_params
        )
        ret = r.json()
    except requests.exceptions.RequestException as e:
        ret = "Errno {0}: {1}".format(e.errno, e.strerror)
    except JSONDecodeError as e:
        ret = "JSON error: {0}".format(e.msg)
    except TypeError:
        ret = "JSON TypeError"
    return ret


def format_luis_data(luis_data):

    if luis_data.get('query') is None:
        ret = luis_data.get('Message')

    else:
        # Top score intent
        ret = '*❗ Top Score Intent:*'
        ret += '\n'
        ret += '{0} - {1}'.format(
            luis_data.get('topScoringIntent', {}).get('score', ''),
            luis_data.get('topScoringIntent', {}).get('intent', '')
        )

        ret += '\n\n'

        # Tutti gli intent
        ret += '*🦄 Tutti gli Intent:*'
        for intent in luis_data.get('intents', []):
            ret += '\n'
            ret += '{0} - {1}'.format(
                intent.get('score', ''),
                intent.get('intent', '')
            )

        ret += '\n\n'

        # Tutte le entities
        ret += '*📚 Tutte le entities:*'
        for entity in luis_data.get('entities', []):
            ret += '\n'
            ret += '{0} - {1}'.format(
                entity.get('score', ''),
                entity.get('intent', '')
            )

        ret += '\n\n'

        # Sentiment
        ret += '*🤬 Sentiment:*'
        ret += '\n'
        ret += '{0}'.format(luis_data.get('sentimentAnalysis', {}).get('score', ''))

    return ret


# Handler dei messaggi
def echo(update, context):
    luis_data = get_luis_data(update.message.text)

    try:
        context.bot.send_message(
            chat_id=update.message.chat_id,
            text=format_luis_data(luis_data) if PRETTY_OUTPUT else luis_data,
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception as e:
        print(e)


# Inizializzo l'updater che resta in ascolto dei messaggi
updater = Updater(token=TG_API_KEY, use_context=True)
dispatcher = updater.dispatcher

# Aggiungo l'handler per tutti i messaggi di testo
echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

# Inizio l'ascolto
updater.start_polling()
