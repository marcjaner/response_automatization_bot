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
    get(update, context)

def get_bookings(update, context):
    try:
        otl.vpt_summarize_bookings_eng()
        otl.vpt_summarize_bookings_de()

        message : str = "Reserves: \n"

        for i in range(0, len(vpt_bookings)):
            booking = vpt_bookings[i]

            message = message + "**%d**. %s -> %s \n%s %d pax \n %s %s\n" % (i, booking.pick_up_arrival, booking.destination_arrival, booking.arrival_date, booking.pax, booking.arrival_time, booking.flight_n_arrival)

            if booking.pick_up_departure is not None:
                message = message + "%s -> %s \n %s %s %s\n" % (booking.pick_up_departure, booking.destination_departure, booking.departure_date, booking.departure_time, booking.flight_n_departure)
            message = message + "\n"

        context.user_data['index'] = len(vpt_bookings - 1)

        context.bot.send_message(chat_id=update.effective_chat.id, text = message)
    except Exception as e:
        print(e)

        context.bot.send_message(chat_id=update.effective_chat.id, text="Hi ha hagut algun error")


def get_quotes(update, context):
    try:
        otl.vpt_summarize_quotes_eng()
        otl.vpt_summarize_quotes_de()

        message : str = "Pressuposts: /n"

        for i in range(context.user_data['index'], context.user_data['index'] + len(vpt_quotes)):
            quote = vpt_quotes[i]

            message = message + "%d. %s %d pax \n\n" % (i, quote.destination, quote.pax)

        context.bot.send_message(chat_id=update.effective_chat.id, text = message)
    except Exception as e:
        print(e)

        context.bot.send_message(chat_id=update.effective_chat.id, text="Hi ha hagut algun problema")


def get(update, context):
    try:
        otl.vpt_get_unread_messages()

        if len(vpt_unread_bookings_eng) + len(vpt_unread_quotes_eng) + len(vpt_unread_bookings_de) + len(vpt_unread_quotes_de) == 0:
            context.bot.send_message(chat_id=update.effective_chat.id, text = "Sembla que no hi ha cap missatge pendent ")
        else:

            get_bookings(update, context)
            get_quotes(uptadte, context)


    except Exception as e:
        print(e)

        context.bot.send_message(chat_id=update.effective_chat.id, text = "Sembla que hi ha hagut algún problema, torna-ho a intentar o contacta amb s'informàtic")

def help(update, context):
    message = "Hola, això és una guia per utilitzar aquest contestador automàtic. Aquí tens una llista amb totes ses comandes que pots utilitzar:\n\n/start: inicialitza aquest bot, s'ha de fer servir cada vegada que l'obris. Per defecte també retorna totes ses reserves i es pressupostos en negrita.\n\n/help: permet accedir a aquesta guia.\n\n/get: retorna totes ses reserves i es pressupostos (ennumerats) pendents de contestar.\n\n/getb: retorna una llista ennumerada amb totes ses reserves pendents de contestar.\n\n/getq: retorna una llista ennumerada amb tots es pressupostos pendents de contestar.\n\n/yes: Confirma una reserva. Sa comanda ha d'anar acompanyada de sa següent informació: \n\n [index] [nº reserva] [preu] [desti(ciutat)]\n\nOpcionalment s'hi poden afegir, en aquest ordre i separats per espais: \n\n[origen(si es diferent a s'aeroport)] [comentaris adicionals]\n\n/no: Contesta a una reserva amb un missatge predefinit per dir que no tenim disponibilitat. Ha d'anar acompanyada de sa següent informació:\n\n [index] [comentaris adicionals(opcional)]\n\n/reply: Contesta a un pressupost amb es preu per trajecte. Ha de tenir es següent format:\n\n[index] [preu] [destí(opcional)]\n\nAquestes són totes ses comandes que inclou es contestador. Per qualsevol sugerència contacta amb s'informàtic"

    context.bot.send_message(chat_id=update.effective_chat.id, text =message)


# --------------------------------------------------------------------------- #
#                              COMMAND HANDLERS                               #
# --------------------------------------------------------------------------- #

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('get', get))
dispatcher.add_handler(CommandHandler('getb', get_bookings))
dispatcher.add_handler(CommandHandler('getq', get_quotes))

updater.start_polling()
updater.idle()
