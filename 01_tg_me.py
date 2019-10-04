import telegram

from constants import TG_API_KEY

# Prendo il gestore del bot
bot = telegram.Bot(token=TG_API_KEY)
print(bot.get_me())
