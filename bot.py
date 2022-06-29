from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
from typing import List, Union, Dict, Optional



TOKEN = open('token.txt').read().strip()
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# --------------------------------------------------------------------------- #
#                                  COMMANDS                                   #
# --------------------------------------------------------------------------- #
def start(update, context):
    fullname: str = update.effective_chat.first_name + " " + update.effective_chat.last_name

    message: str = "Hola %s" % (fullname)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

# --------------------------------------------------------------------------- #
#                              COMMAND HANDLERS                               #
# --------------------------------------------------------------------------- #

dispatcher.add_handler(CommandHandler('start', start))

updater.start_polling()
updater.idle()
