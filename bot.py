from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
from typing import List, Union, Dict, Optional
from typing_extensions import TypeAlias
import outlook as otl



vpt_unread_bookings_eng : TypeAlias = list
vpt_unread_quotes_eng : TypeAlias = list
vpt_unread_bookings_de : TypeAlias = list
vpt_unread_quotes_de : TypeAlias = list

vpt_bookings : TypeAlias = list[otl.VPT_booking]
vpt_quotes : TypeAlias = list[otl.VPT_quote]

# --------------------------------------------------------------------------- #
#                                  COMMANDS                                   #
# --------------------------------------------------------------------------- #
def start(update, context):
    name: str = update.effective_chat.first_name

    message: str = "Hola %s, \nAquests són es missatges pendents per contestar. Per qualsevol dubte fés servir sa comanda /help" % (name)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    get(update, context)

def get(update, context):
    try:
        global vpt_bookings
        vpt_bookings = otl.manage_bookings()
        global vpt_quotes
        vpt_quotes = otl.manage_quotes()

        message : str = "Reserves: \n"

        for i in range(0, len(vpt_bookings)):
            booking = vpt_bookings[i]

            message = message + "%d. %s -> %s \n    %s pax %s %s %s\n" % (i, booking.pick_up_arrival, booking.destination_arrival, booking.pax, booking.arrival_date, booking.arrival_time, booking.flight_n_arrival.upper())

            if booking.type_transf != ' One way':
                message = message + "    %s -> %s \n    %s %s %s\n" % (booking.pick_up_departure, booking.destination_departure, booking.departure_date, booking.departure_time, booking.flight_n_departure)


            message = message + "\n"
        message = message + "\n" + "Pressuposts: \n"


        for i in range(0, len(vpt_quotes)):
            quote = vpt_quotes[i]

            message = message + "%s. %s %s pax \n\n" % (i + len(vpt_bookings), quote.destination, quote.pax)

        context.bot.send_message(chat_id=update.effective_chat.id, text = message)

    except Exception as e:
        print(e)

        context.bot.send_message(chat_id=update.effective_chat.id, text="Hi ha hagut algun problema")



    except Exception as e:
        print(e)

        context.bot.send_message(chat_id=update.effective_chat.id, text = "Sembla que hi ha hagut algún problema, torna-ho a intentar o contacta amb s'informàtic")

def help(update, context):
    message = "Hola, això és una guia per utilitzar aquest contestador automàtic. Aquí tens una llista amb totes ses comandes que pots utilitzar:\n\n/start: inicialitza aquest bot, s'ha de fer servir cada vegada que l'obris. Per defecte també retorna totes ses reserves i es pressupostos en negrita.\n\n/help: permet accedir a aquesta guia.\n\n/get: retorna totes ses reserves i es pressupostos (ennumerats) pendents de contestar.\n\n/getb: retorna una llista ennumerada amb totes ses reserves pendents de contestar.\n\n/getq: retorna una llista ennumerada amb tots es pressupostos pendents de contestar.\n\n/yes: Confirma una reserva. Sa comanda ha d'anar acompanyada de sa següent informació: \n\n [index] [nº reserva] [preu] [desti(ciutat)]\n\nOpcionalment s'hi poden afegir, en aquest ordre i separats per espais: \n\n[origen(si es diferent a s'aeroport)] [comentaris adicionals]\n\n/no: Contesta a una reserva amb un missatge predefinit per dir que no tenim disponibilitat. Ha d'anar acompanyada de sa següent informació:\n\n [index] [comentaris adicionals(opcional)]\n\n/reply: Contesta a un pressupost amb es preu per trajecte. Ha de tenir es següent format:\n\n[index] [preu] [destí(opcional)]\n\nAquestes són totes ses comandes que inclou es contestador. Per qualsevol sugerència contacta amb s'informàtic"

    context.bot.send_message(chat_id=update.effective_chat.id, text =message)

def yes(update, context):
    try:
        booking : otl.VPT_booking = vpt_bookings[int(context.args[0])]
        parameters = context.args[1].replace('.', ' ').split(',')
        booking.booking_number = parameters[0]

        booking.subtotal_first = int(parameters[1])
        booking.total = booking.subtotal_first * 2
        booking.subtotal_second = 10 * round(int(booking.subtotal_first) * 0.4 / 10)
        booking.subtotal_third = int(booking.subtotal_first - booking.subtotal_second)

        booking.city = parameters[2]

        for arg in context.args:
            if arg.startswith("correct"):
                change = str(arg[8:int(len(str(arg)))]).replace(".", " ").split(',')

                for attribute, value in booking.__dict__.items():
                    if str(value) == str(change[0]):
                        for at, val in zip([attribute], [change[1]]):
                            setattr(booking, at, val)

        if booking.language == "ENG":
            otl.vpt_send_booking_confirmation_eng(booking)
        else:
            otl.vpt_send_booking_confirmation_de(booking)
        # elif booking.language == "ES":
        #     otl.vpt_send_booking_confirmation_es(booking)




    except Exception as e:
        print(e)

def no(update, context):
    index = context.args[0]
    assert index < len(vpt_bookings)

    booking = vpt_bookings[index]
    if booking.language == "ENG":
        otl.vpt_reject_booking_eng(booking)
    elif booking.language == "DE":
        otl.vpt_reject_booking_de(booking)
    elif booking.language == "ES":
        otl.vpt_reject_booking_es(booking)

def reply(update, context):
    index = context.args[0]
    assert index >= len(vpt_bookings)

    price = int(context.args[1])
    quote.subtotal = price
    quote.total = price * 2

    quote = vpt_quotes[index]
    if quote.language == "ENG":
        otl.vpt_send_quote_eng(quote)
    elif quote.language == "DE":
        otl.vpt_send_quote_de(quote)
    elif quote.language == "ES":
        otl.vpt_send_quote_es(quote)


# --------------------------------------------------------------------------- #
#                              COMMAND HANDLERS                               #
# --------------------------------------------------------------------------- #
TOKEN = open('token.txt').read().strip()
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('get', get))
dispatcher.add_handler(CommandHandler('yes', yes))
dispatcher.add_handler(CommandHandler('no', no))
dispatcher.add_handler(CommandHandler('reply', reply))

updater.start_polling()
updater.idle()
