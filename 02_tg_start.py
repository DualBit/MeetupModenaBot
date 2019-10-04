from telegram.ext import Updater, CommandHandler

from constants import TG_API_KEY


# Handler del messaggio start
def start(update, context):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="Ciao sono un 🤖! Parla con me!"
    )


# Inizializzo l'updater che resta in ascolto dei messaggi
updater = Updater(token=TG_API_KEY, use_context=True)
dispatcher = updater.dispatcher

# Aggiungo l'handler per il comando start
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# Inizio l'ascolto
updater.start_polling()
