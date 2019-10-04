from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from constants import TG_API_KEY


# Handler del comando
def meme(update, context):
    keyboard = [
        [
            InlineKeyboardButton('Opzione 😏', callback_data='1'),
            InlineKeyboardButton('Opzione 😯', callback_data='2'),
            InlineKeyboardButton('Opzione 😮', callback_data='3'),
            InlineKeyboardButton('Opzione 😵', callback_data='4')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        # Invio il meme
        context.bot.send_photo(
            chat_id=update.message.chat_id,
            photo=open('vince/full.png', 'rb')
        )

        # Imposto la tastiera
        update.message.reply_text('Scegli la tua opzione:', reply_markup=reply_markup)

    except Exception as e:
        print(e)


# Handler delle opzioni
def button(update, context):
    query = update.callback_query

    try:
        # Rimpiazzo i bottoni con la scelta effettuata
        query.edit_message_text(text='Selezionata l\'opzione: {0}'.format(query.data))

        # Invio il meme corrispondente
        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=open('vince/{0}.png'.format(query.data), 'rb')
        )

    except Exception as e:
        print(e)


# Inizializzo l'updater che resta in ascolto dei messaggi
updater = Updater(token=TG_API_KEY, use_context=True)
dispatcher = updater.dispatcher

# Aggiungo gli handler per il comando start e le opzioni
updater.dispatcher.add_handler(CommandHandler('meme', meme))
updater.dispatcher.add_handler(CallbackQueryHandler(button))

# Inizio l'ascolto
updater.start_polling()

# Rimango in attesa per l'uscita
updater.idle()
