from typing_extensions import TypeAlias
from dataclasses import dataclass
import templates as tmplt
import win32com.client
from win32printing import Printer
import pythoncom

# --------------------------------------------------------------------------- #
#                              GLOBAL VARIABLES                               #
# --------------------------------------------------------------------------- #
outlook = win32com.client.Dispatch('outlook.application', pythoncom.CoInitialize())
mapi = outlook.GetNamespace("MAPI")

# --------------------------------------------------------------------------- #
#                               VPT VARIABLES                                 #
# --------------------------------------------------------------------------- #
vpt = mapi.Folders("contact@vptmallorca.com")
vpt_inbox = vpt.Folders(1)
#------------------------------------ENG--------------------------------------#



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
	flight_n_departure: str
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

@dataclass
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
# jb = mapi.Folders("bus@janer-bus.com")
# jb_inbox = jb.Folders(1)
# jb_messages = jb_inbox.Items


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

def vpt_get_unread_messages(vpt_unread_bookings, vpt_unread_quotes) -> None:
	vpt_messages = vpt_inbox.Items
      #------------------------------ENG--------------------------------#
	for msg in list(vpt_messages):
		if msg.UnRead == True:
			if msg.Subject.startswith('Transfer de') or msg.Subject.startswith('Re: VPTMallorca Quote') or 				msg.Subject.startswith('Reserva de'):
				vpt_unread_bookings.append(msg)
			elif msg.Subject.startswith('Presupuesto de') or msg.Subject.startswith('Transferpreise vom'):
				vpt_unread_quotes.append(msg)

def treat_booking(msg_body: list)-> None:
	""" removes empty index """
	for string in msg_body:
		if string == '':
			msg_body.remove('')

def get_booking(msg_body: list)-> list:
	""" returns a list with the info needed to create an instance of VPT_booking """
	booking_info = []
	for string in msg_body:
		if ":" in string:
			booking_info.append(string.split(":")[1])
	return booking_info

def get_booking_class(booking_info: list)-> VPT_booking:
	""" creates an instance of the booking class from the info found in the auxiliary list created previously """
	aux_class = VPT_booking(None, booking_info[0],booking_info[1],booking_info[2],booking_info[3],booking_info[4],booking_info[5],booking_info[6],booking_info[7],booking_info[8],booking_info[9],booking_info[10],booking_info[11],booking_info[12],booking_info[13],booking_info[14],booking_info[15],booking_info[16],None, None,None,None,None,None,None,None)
	return aux_class

def treat_quote(msg_body : list)-> None:
    """ removes empty index """
    for string in msg_body:
        if string == '':
            msg_body.remove('')

def get_quote(msg_body: list)-> list:
	""" returns a list with the info needed to create an instance of VPT_quote """
	quote_info = []
	for string in msg_body:
		if ":" in string:
			quote_info.append(string.split(":")[1])
	return quote_info

def get_quote_class(quote_info: list)-> VPT_quote:
    """ from the info list, creates an instance of the quote class """
    quote = VPT_quote(quote_info[0],quote_info[1],quote_info[2],quote_info[3], None, None, None, None)
    return quote




def manage_bookings()-> list:
	""" updates and manages bookings, returns a list with all the new bookings """
	vpt_unread_bookings = []
	vpt_unread_quotes = []
	# updates global variables with new unread messages
	vpt_get_unread_messages(vpt_unread_bookings, vpt_unread_quotes)

	vpt_bookings = []
	assert len(vpt_unread_bookings)>0
	for i in range(0, len(vpt_unread_bookings)):
		# pre-process the e-mail in order to treat it correctly
		msg_body = vpt_unread_bookings[i].Body.replace("\n","").split("\r")
		subject = vpt_unread_bookings[i].Subject

		treat_booking(msg_body)

		# get info in order to initialize the VPT_booking dataclass
		info_list = get_booking(msg_body)

		# get booking class
		booking = get_booking_class(info_list)

		# check the language of the e-mail and store the language.
		if subject.startswith('Transfer de') or subject.startswith('Re: VPTMallorca Quote'):
			booking.language = 'ENG'
		elif subject.startswith('Reserva de'):
			booking.language = 'DE'
		else:
			booking.language = 'ESP'
		vpt_bookings.append(booking)

	return vpt_bookings


def manage_quotes()-> list:
	""" updates and manages bookings, returns a list with all the new bookings """
	# updates global variables with new unread messages
	vpt_unread_bookings = []
	vpt_unread_quotes = []
	vpt_get_unread_messages(vpt_unread_bookings, vpt_unread_quotes)

	vpt_quotes = []
	assert len(vpt_unread_quotes) > 0
	for i in range(0, len(vpt_unread_quotes)):
		# pre-process the e-mail in order to treat it correctly
		msg_body = vpt_unread_quotes[i].Body.replace("\n","").split("\r")
		subject = vpt_unread_quotes[i].Subject

		treat_quote(msg_body)

		quote_info = get_quote(msg_body)

		quote = get_quote_class(quote_info)

		if subject.startswith('Presupuesto de'):
			quote.language = 'ENG'
		elif subject.startswith('Transferpreise vom'):
			quote.language = 'DE'
		else:
			quote.language = 'ESP'

		vpt_quotes.append(quote)
	return vpt_quotes

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
	manage_bookings()
	manage_quotes()

main()
# --------------------------------------------------------------------------- #
#                              JANERBUS MODULES                               #
# --------------------------------------------------------------------------- #
