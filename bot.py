from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
from typing import List, Union, Dict, Optional
from typing_extensions import TypeAlias
import outlook as otl



TOKEN = open('token.txt').read().strip()
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

vpt_unread_bookings_eng : TypeAlias = list
vpt_unread_quotes_eng : TypeAlias = list
vpt_unread_bookings_de : TypeAlias = list
vpt_unread_quotes_de : TypeAlias = list

VPT_booking : TypeAlias = otl.VPT_booking
VPT_quote : TypeAlias = otl.VPT_quote

vpt_bookings : TypeAlias = list[VPT_booking]
vpt_quotes : TypeAlias = list[VPT_quote]

# --------------------------------------------------------------------------- #
#                                  COMMANDS                                   #
# --------------------------------------------------------------------------- #
def start(update, context):
    name: str = update.effective_chat.first_name

    message: str = "Hola %s, \nAquests són es missatges pendents per contestar. Per qualsevol dubte fés servir sa comanda /help" % (name)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    get()

def get_bookings(update, context):
    otl.vpt_summarize_bookings_eng()
    otl.vpt_summarize_bookings_de()

    message : str = "Reserves: \n"

    for booking in vpt_bookings:
        message = message + 

def get_quotes(update, context):
    otl.vpt_summarize_quotes_eng()
    otl.vpt_summarize_quotes_de()


def get(update, context):
    try:
        otl.vpt_get_unread_messages()

        if len(vpt_unread_bookings_eng) + len(vpt_unread_quotes_eng) + len(vpt_unread_bookings_de) + len(vpt_unread_quotes_de) == 0:
            context.bot.send_message(chat_id=update.effective_chat.id, text = "Sembla que no hi ha cap missatge pendent ")
        else:

            get_bookings()
            get_quotes()


    except Exception as e:
        print(e)

        context.bot.send_message(chat_id=update.effective_chat.id, text = "Sembla que hi ha hagut algún problema, torna-ho a intentar o contacta amb s'informàtic")


# --------------------------------------------------------------------------- #
#                              COMMAND HANDLERS                               #
# --------------------------------------------------------------------------- #

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('get', get))

updater.start_polling()
updater.idle()
