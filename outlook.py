from typing_extensions import TypeAlias
from dataclasses import dataclass
import templates as tmplt
import win32com.client
from win32printing import Printer

# --------------------------------------------------------------------------- #
#                              GLOBAL VARIABLES                               #
# --------------------------------------------------------------------------- #
outlook = win32com.client.Dispatch('outlook.application')
mapi = outlook.GetNamespace("MAPI")

# --------------------------------------------------------------------------- #
#                               VPT VARIABLES                                 #
# --------------------------------------------------------------------------- #
vpt = mapi.Folders("contact@vptmallorca.com")
vpt_inbox = vpt.Folders(1)
#------------------------------------ENG--------------------------------------#
vpt_unread_bookings_eng = list
vpt_unread_quotes_eng = list
#-------------------------------------DE--------------------------------------#
vpt_unread_bookings_de = list
vpt_unread_quotes_de = list

@dataclass
class VPT_booking:
	booking_number: str
	name: str
	email: str
	phone: str
	pax: int
	type_transf: str
	pick_up_arrival: str
	destination_arrival: str
	arrival_date: str
	arrival_time: str
	flight_n_arrival: str
	pick_up_departure: str
	destination_departure: str
	departure_date: str
	departure_time: str
	fligh_n_departure: str
	baby_seat: str
	child_seat: str
	origin: str
	city: str
	total: int
	subtotal_first: int
	subtotal_second: int
	subtotal_third: int
	language : str
	status: str


class VPT_quote:
	name:str
	email:str
	pax: int
	destination: str
	subtotal: int
	total: int
	language : str
	status:str


vpt_bookings : TypeAlias = list[VPT_booking]
vpt_quotes : TypeAlias = list[VPT_quote]



# --------------------------------------------------------------------------- #
#                             JANERBUS VARIABLES                              #
# --------------------------------------------------------------------------- #
jb = mapi.Folders("bus@janer-bus.com")
jb_inbox = jb.Folders(1)
jb_messages = jb_inbox.Items


# --------------------------------------------------------------------------- #
#                               GLOBAL MODULES                                #
# --------------------------------------------------------------------------- #

def send_message(to : str, acc : str, subject : str, body : str):
	mail = outlook.CreateItem(0)
	mail.Subject = subject
	mail.To = to
	mail.From = acc
	mail.HTMLbody = body
	mail.send()

def print_booking(body : str):
	with Printer(printer_name = "Kyocera ECOSYS P2040dn") as printer:
		printer.text(body)



# --------------------------------------------------------------------------- #
#                                VPT MODULES                                  #
# --------------------------------------------------------------------------- #

def vpt_get_unread_messages() -> list:
	vpt_messages = vpt_inbox.Items
      #------------------------------ENG--------------------------------#
	global vpt_unread_bookings_eng
	vpt_unread_bookings_eng = []
	global vpt_unread_quotes_eng
	vpt_unread_quotes_eng = []

      #-------------------------------DE--------------------------------#
	global vpt_unread_bookings_de
	vpt_unread_bookings_de = []
	global vpt_unread_quotes_de
	vpt_unread_quotes_de = []

	global vpt_unread
	for msg in list(vpt_messages):
		if msg.UnRead == True:
       #------------------------------ENG--------------------------------#
			if msg.Subject.startswith('Transfer de') or msg.Subject.startswith('Re: VPTMallorca Quote'):
				vpt_unread_bookings_eng.append(msg)
			elif msg.Subject.startswith('Presupuesto de'):
				vpt_unread_quotes_eng.append(msg)

       #-------------------------------DE--------------------------------#
			elif msg.Subject.startswith('Reserva de'):
				vpt_unread_bookings_de.append(msg)
			elif msg.Subject.startswith('Transferpreise vom'):
				vpt_unread_quotes_de.append(msg)


# def vpt_summarize_bookings_eng() -> list[VPT_booking]:
def vpt_summarize_quotes_eng() -> list[VPT_quote]:
	global vpt_quotes
	for message in vpt_unread_quotes_eng:
		previous_word = None

		for word in message.body:
			if previous_word is "Name:":
				name = word
				for word in message.body:
					if word is not "Email:":
						name = name + " " + word


			elif previous_word is "Email:":
				email = word.lower()
			elif previous_word is "Destination:":
				destination = word
			elif previous_word is "Pax:":
				pax = word
			previous_word = word

		quote = VPT_quote(name, email, int(pax), destination, None, None, "ENG", "pending")
		vpt_quotes.append(quote)

# def vpt_summarize_bookings_eng() -> list[VPT_booking]:
# def vpt_summarize_quotes_eng() -> list[VPT_quote]:

#------------------------------------ENG--------------------------------------#

def vpt_send_booking_confirmation_eng(booking_id : int):
	booking : VPT_booking = vpt_bookings[booking_id]
	assert booking.language == "ENG"
	message = tmplt.vpt_eng_booking_confirmation(booking)

	send_message(booking.email, "contact@vptmallorca.com", "Transfer confirmation VPT" + booking.booking_number, message)

	print_booking(booking.body)

def vpt_send_quote_eng(quote_id : int):
	quote = VPT_quote = vpt_quotes[quote_id]
	assert quote.language == "ENG"
	message = tmplt.vpt_eng_quote(quote)

	send_message(quote.email, "contact@vptamllorca.com", "VPTMallorca Quote", message)

#-------------------------------------DE--------------------------------------#
def vpt_send_booking_confirmation_de(booking_id : int):
	booking : VPT_booking = vpt_bookings[booking_id]
	assert booking.language == "DE"

	message = tmplt.vpt_de_booking_confirmation(booking)
	send_message(booking.email, "contact@vptmallorca.com", "Buchungsbestätigung VPT" + booking.booking_number, message)

def vpt_send_quote_de(quote_id : int):
	quote = VPT_quote = vpt_quotes[quote_id]
	assert quote.language == "DE"





def main():
	vpt_get_unread_messages()
	vpt_summarize_bookings(vpt_unread_bookings_eng)
	vpt_summarize_quotes(vpt_unread_quotes_eng)


main()

# --------------------------------------------------------------------------- #
#                              JANERBUS MODULES                               #
# --------------------------------------------------------------------------- #
