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
	fullname: str
	email: str
	phone: str
	pax: int
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
	type_transf: str
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
	outlook = win32com.client.Dispatch('outlook.application', pythoncom.CoInitialize())
	mapi = outlook.GetNamespace("MAPI")
	mail = outlook.CreateItem(0)
	mail.Subject = subject
	From = outlook.Session.Accounts[acc]
	mail.To = to
	mail.HTMLbody = body
	mail._oleobj_.Invoke(*(64209, 0, 8, 0, From))
	mail.Send()

def print_booking(body : str):
	with Printer(printer_name = "Kyocera ECOSYS P2040dn") as printer:
		printer.text(body)



# --------------------------------------------------------------------------- #
#                                VPT MODULES                                  #
# --------------------------------------------------------------------------- #

def vpt_get_unread_messages(vpt_unread_bookings, vpt_unread_quotes) -> None:
	vpt_messages = mapi.Folders("contact@vptmallorca.com").Folders(1).Items
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
		if ":" in string and string.count(":") == 1:
			booking_info.append(string.split(":")[1])
		elif ":" in string and string.count(":")>1:
			index = index_two_points(string)
			word = string[index+1:len(string)]
			booking_info.append(word)
	return booking_info

def get_booking_class(booking_info: list)-> VPT_booking:
	""" creates an instance of the booking class from the info found in the auxiliary list created previously """
	aux_class = VPT_booking(None, booking_info[0].split()[0].title(),booking_info[0].title(),booking_info[1].lower(),booking_info[2],booking_info[3],booking_info[5].title(),booking_info[6].title(),booking_info[7],booking_info[8],booking_info[9],booking_info[10],booking_info[11],booking_info[12],booking_info[13],booking_info[14],booking_info[15],booking_info[16],None, None,None,None,None,None,None,booking_info[4], None)
	return aux_class

def treat_quote(msg_body : list)-> None:
    """ removes empty index """
    for string in msg_body:
        if string == '':
            msg_body.remove('')



def index_two_points(word: str)-> int:
	""" given a string, returns the index of the string in which we find the first ':' character """
	for i in range(0, len(word)):
		if word[i] == ':':
			return i


def get_quote(msg_body: list)-> list:
	""" returns a list with the info needed to create an instance of VPT_quote """
	quote_info = []
	for string in msg_body:
		if ":" in string and string.count(":") == 1:
			quote_info.append(string.split(":")[1])
		elif ":" in string and string.count(":")>1:
			index = index_two_points(string)
			word = string[index+1:-1]
			quote_info.append(word)

	return quote_info

def get_quote_class(quote_info: list)-> VPT_quote:
    """ from the info list, creates an instance of the quote class """
    quote = VPT_quote(quote_info[0],quote_info[1],quote_info[3],quote_info[2], None, None, None, None)
    return quote




def manage_bookings()-> list:
	""" updates and manages bookings, returns a list with all the new bookings """
	vpt_unread_bookings = []
	vpt_unread_quotes = []
	print(1)
	# updates global variables with new unread messages
	vpt_get_unread_messages(vpt_unread_bookings, vpt_unread_quotes)
	print(2)
	vpt_bookings = []
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

def vpt_send_booking_confirmation_eng(booking : VPT_booking):
	message = tmplt.vpt_eng_booking_confirmation(booking)

	send_message(booking.email, "contact@vptmallorca.com", "Transfer confirmation VPT" + booking.booking_number, message)


def vpt_send_quote_eng(quote_id : int):
	quote = VPT_quote = vpt_quotes[quote_id]
	assert quote.language == "ENG"
	message = tmplt.vpt_eng_quote(quote)

	send_message(quote.email, "contact@vptamllorca.com", "VPTMallorca Quote", message)

#-------------------------------------DE--------------------------------------#
def vpt_send_booking_confirmation_de(booking : VPT_booking):
	assert booking.language == "DE"

	message = tmplt.vpt_de_booking_confirmation(booking)
	send_message(booking.email, "contact@vptmallorca.com", "Buchungsbestätigung VPT" + booking.booking_number, message)

def vpt_send_quote_de(quote_id : int):
	quote = VPT_quote = vpt_quotes[quote_id]
	assert quote.language == "DE"


# --------------------------------------------------------------------------- #
#                              JANERBUS MODULES                               #
# --------------------------------------------------------------------------- #
# booking = VPT_booking("VPT123-1609", "Marc", "Marc Janer", "marcjanerferrer@gmail.com", "636990408", "6", "Palma Airport", "Alcudia", "06/07/2022", "10:35 pm", "VLG5678", "Alcudia", "Palma Airport", "14/07/2022", "9:00 am", "UX6730", None, None, "Palma Airport", "Alcudia", 144, 72, 30, 42, "DE", "Round", None)
#
# def main():
#     vpt_send_booking_confirmation_eng(booking)
#
# main()
