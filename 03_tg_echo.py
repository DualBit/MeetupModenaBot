from telegram.ext import Updater, MessageHandler, Filters

from constants import TG_API_KEY


# Handler dei messaggi
def echo(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text=update.message.text
    )


# Inizializzo l'updater che resta in ascolto dei messaggi
updater = Updater(token=TG_API_KEY, use_context=True)
dispatcher = updater.dispatcher

# Aggiungo l'handler per tutti i messaggi di testo
echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

# Inizio l'ascolto
updater.start_polling()
