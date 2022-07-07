from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
from typing import List, Union, Dict, Optional
from typing_extensions import TypeAlias
from outlook import*


vpt_unread_bookings_eng : TypeAlias = list
vpt_unread_quotes_eng : TypeAlias = list
vpt_unread_bookings_de : TypeAlias = list
vpt_unread_quotes_de : TypeAlias = list

vpt_bookings : TypeAlias = list[VPT_booking]
vpt_quotes : TypeAlias = list[VPT_quote]


vpt_bookings = manage_bookings()
vpt_quotes = manage_quotes()

def start(update, context):
    name: str = update.effective_chat.first_name
    message: str = "Hola %s, \nAquests són es missatges pendents per contestar. Per qualsevol dubte fés servir sa comanda /help" % (name)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def get_bookings(update, context):
    try:

        message : str = "Reserves: \n"

        for i in range(0, len(vpt_bookings)):
            booking = vpt_bookings[i]

            message = message + "%s. %s -> %s \n%s %s pax %s %s\n" % (i, booking.pick_up_arrival, booking.destination_arrival, booking.arrival_date, booking.pax, booking.arrival_time, booking.flight_n_arrival.upper())

            if booking.flight_n_departure != '':
                message = message + "%s -> %s \n%s %s %s\n" % (booking.pick_up_departure, booking.destination_departure, booking.departure_date, booking.departure_time, booking.flight_n_departure.upper())
            message = message + "\n"

        context.user_data['index'] = len(vpt_bookings )-1

        context.bot.send_message(chat_id=update.effective_chat.id, text = message)
    except Exception as e:
        print(e)

        context.bot.send_message(chat_id=update.effective_chat.id, text="Hi ha hagut algun error")

def get_quotes(update, context):
    try:


        message : str = "Pressuposts: \n"

        for i in range(0, len(vpt_quotes)):
            quote = vpt_quotes[i]

            message = message + "%s. %s %s pax \n\n" % (i, quote.destination, quote.pax)

        context.bot.send_message(chat_id=update.effective_chat.id, text = message)
    except Exception as e:
        print(e)

        context.bot.send_message(chat_id=update.effective_chat.id, text="Hi ha hagut algun problema")


def yes(update, context):
    """ accepts a certain booking """
    """ parameters to take: [index] [nº reserva] [preu] [desti(ciutat)]
    parameters to take optionally: [origen(si es diferent a s'aeroport)] [comentaris adicionals] """
    try:
        index = context.args[0]
        id = context.args[1]
        price = context.args[2]
        dst = context.args[3].split(',')
        orig = context.args[4].split(',')
        comments = context.args[5].split(',')

    except Exception as e:
        print(e)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Hi ha hagut algun problema")

def no(update, context):
    """ rejects a certain booking """
    """ parameters to take:  [index] [comentaris adicionals(opcional)] """





def help(update, context):
    message = "Hola, això és una guia per utilitzar aquest contestador automàtic. Aquí tens una llista amb totes ses comandes que pots utilitzar:\n\n/start: inicialitza aquest bot, s'ha de fer servir cada vegada que l'obris. Per defecte també retorna totes ses reserves i es pressupostos en negrita.\n\n/help: permet accedir a aquesta guia.\n\n/get: retorna totes ses reserves i es pressupostos (ennumerats) pendents de contestar.\n\n/getb: retorna una llista ennumerada amb totes ses reserves pendents de contestar.\n\n/getq: retorna una llista ennumerada amb tots es pressupostos pendents de contestar.\n\n/yes: Confirma una reserva. Sa comanda ha d'anar acompanyada de sa següent informació: \n\n [index] [nº reserva] [preu] [desti(ciutat)]\n\nOpcionalment s'hi poden afegir, en aquest ordre i separats per espais: \n\n[origen(si es diferent a s'aeroport)] [comentaris adicionals]\n\n/no: Contesta a una reserva amb un missatge predefinit per dir que no tenim disponibilitat. Ha d'anar acompanyada de sa següent informació:\n\n [index] [comentaris adicionals(opcional)]\n\n/reply: Contesta a un pressupost amb es preu per trajecte. Ha de tenir es següent format:\n\n[index] [preu] [destí(opcional)]\n\nAquestes són totes ses comandes que inclou es contestador. Per qualsevol sugerència contacta amb s'informàtic"

    context.bot.send_message(chat_id=update.effective_chat.id, text =message)



TOKEN = open('token.txt').read().strip()
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('yes', yes))
dispatcher.add_handler(CommandHandler('getb', get_bookings))
dispatcher.add_handler(CommandHandler('getq', get_quotes))

updater.start_polling()
updater.idle()
