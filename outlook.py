from typing_extensions import TypeAlias
from dataclasses import dataclass
import templates as tmplt
import win32com.client
from win32 import win32print
import win32api
import pythoncom
from fpdf import FPDF
import os

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
class Booking:
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
	pick_up_time: str
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
	body : str

@dataclass
class Quote:
	name:str
	email:str
	pax: int
	destination: str
	subtotal: int
	total: int
	language : str
	status:str
	body: str


vpt_bookings : TypeAlias = list[Booking]
vpt_quotes : TypeAlias = list[Quote]



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
	print(outlook.GetNamespace('MAPI').Accounts.Count)
	for account in outlook.GetNamespace('MAPI').Accounts:
		print(account.SmtpAddress)
		if str(account) == acc:
			From = account
			break
	mail.To = to
	mail.HTMLbody = body
	mail._oleobj_.Invoke(*(64209, 0, 8, 0, From))
	mail.Send()

def print_booking(body : str):
	pdf = FPDF()
	pdf.add_page()
	pdf.set_font('Arial', '', 10)
	for s in body:
		pdf.cell(200, 10, txt = body, align= 'L')
	pdf.output("booking_confirmation.pdf")

	win32api.ShellExecute(0,"print","booking_confirmation.pdf", "Kyocera ECOSYS P2040dn",".",0)


def mark_as_read(message) -> None:
	outlook = win32com.client.Dispatch('outlook.application', pythoncom.CoInitialize())
	mapi = outlook.GetNamespace("MAPI")
	vpt_messages = mapi.Folders("contact@vptmallorca.com").Folders(1).Items

	for msg in list(vpt_messages):
		if msg.UnRead == True:
			if msg.Body == message.body and message.status != "Pending":
				print(str(mapi.Folders("contact@vptmallorca.com").Folders(1).Folders))
				msg.Move(mapi.Folders("contact@vptmallorca.com").Folders(1).Folders("Contestador automatic"))
				msg.UnRead = False

# --------------------------------------------------------------------------- #
#                                VPT MODULES                                  #
# --------------------------------------------------------------------------- #

def vpt_get_unread_messages(vpt_unread_bookings, vpt_unread_quotes) -> None:
	outlook = win32com.client.Dispatch('outlook.application', pythoncom.CoInitialize())
	mapi = outlook.GetNamespace("MAPI")
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
	""" returns a list with the info needed to create an instance of Booking """
	booking_info = []
	for string in msg_body:
		if ":" in string and string.count(":") == 1:
			booking_info.append(string.split(": ")[1])
		elif ":" in string and string.count(":")>1:
			index = index_two_points(string)
			word = string[index+1:len(string)]
			booking_info.append(word)
	return booking_info

def get_booking_class(booking_info: list)-> Booking:
	""" creates an instance of the booking class from the info found in the auxiliary list created previously """
	aux_class = Booking(None, booking_info[0].split()[0].title(),booking_info[0].title(),booking_info[1].lower(),booking_info[2],booking_info[3],booking_info[5].title(),booking_info[6].title(),booking_info[7],booking_info[8],booking_info[9],booking_info[10],booking_info[11],booking_info[12],booking_info[13],None, booking_info[14],booking_info[15],booking_info[16],None, None,None,None,None,None,None,booking_info[4], "Pending", None)
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
	""" returns a list with the info needed to create an instance of Quote """
	quote_info = []
	for string in msg_body:
		if ":" in string and string.count(":") == 1:
			quote_info.append(string.split(":")[1])
		elif ":" in string and string.count(":")>1:
			index = index_two_points(string)
			word = string[index+1:-1]
			quote_info.append(word)

	return quote_info

def get_quote_class(quote_info: list)-> Quote:
    """ from the info list, creates an instance of the quote class """
    quote = Quote(quote_info[0], quote_info[1], quote_info[3], quote_info[2] , None, None, None, "Pending", None)
    return quote

def vpt_manage_bookings(vpt_bookings)-> list:
	""" updates and manages bookings, returns a list with all the new bookings """
	vpt_unread_bookings = []
	vpt_unread_quotes = []
	vpt_bookings = []
	# updates global variables with new unread messages
	vpt_get_unread_messages(vpt_unread_bookings, vpt_unread_quotes)
	for i in range(0, len(vpt_unread_bookings)):
		# pre-process the e-mail in order to treat it correctly
		msg_body = vpt_unread_bookings[i].Body.replace("\n","").split("\r")
		subject = vpt_unread_bookings[i].Subject

		treat_booking(msg_body)

		# get info in order to initialize the Booking dataclass
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
		booking.body = vpt_unread_bookings[i].Body

		#CONTROL
		if "marcjanerferrer@gmail.com" in booking.email:
			vpt_bookings.append(booking)

	return vpt_bookings

def vpt_manage_quotes() -> list:
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
		quote.body = vpt_unread_quotes[i].Body
		if "marcjanerferrer@gmail.com" in quote.email:
			vpt_quotes.append(quote)
	return vpt_quotes

#------------------------------------ENG--------------------------------------#

def vpt_send_booking_confirmation_eng(booking : Booking):
	message = tmplt.vpt_eng_booking_confirmation(booking)

	send_message(booking.email, "contact@vptmallorca.com", "Transfer confirmation " + booking.booking_number, message)

	# print_booking(booking.body)
	# os.remove("booking_confirmation.pdf")

def vpt_reject_booking_eng(booking : Booking):
	message = tmplt.vpt_eng_reject_booking(booking)

	send_message(booking.email, "contact@vptmallorca.com", "VPTMallorca transfer", message)

def vpt_send_quote_eng(quote : Quote):
	assert quote.language == "ENG"
	message = tmplt.vpt_eng_quote(quote)

	send_message(quote.email, "contact@vptmallorca.com", "VPTMallorca Quote", message)

#-------------------------------------DE--------------------------------------#
def vpt_send_booking_confirmation_de(booking : Booking):
	assert booking.language == "DE"

	message = tmplt.vpt_de_booking_confirmation(booking)
	send_message(booking.email, "contact@vptmallorca.com", "Buchungsbestätigung VPT" + booking.booking_number, message)

def vpt_reject_booking_de(booking : Booking):
	message = tmplt.vpt_de_reject_booking(booking)

	send_message(booking.email, "contact@vptmallorca.com", "VPTMallorca transfer", message)

def vpt_send_quote_de(quote : Quote):
	quote = Quote = vpt_quotes[quote_id]
	assert quote.language == "DE"


#-------------------------------------ES--------------------------------------#
def vpt_send_booking_confirmation_es(booking : Booking):
	assert booking.language == "ES"

	message = tmplt.vpt_es_booking_confirmation(booking)

	send_message(booking.email, "contact@vptmallorca.com", "Confirmación de reserva " + booking.booking_number, message)

def vpt_reject_booking_es(booking : Booking):
	message = tmplt.vpt_es_reject_booking(booking)

	send_message(booking.email, "contact@vptmallorca.com", "VPTMallorca transfer", message)

def vpt_send_quote_es(quote : Quote):
	quote = Quote = vpt_quotes[quote_id]
	assert quote.language == "ES"


# --------------------------------------------------------------------------- #
#                              JANERBUS MODULES                               #
# --------------------------------------------------------------------------- #

def jb_get_unread_messages(jb_unread_bookings, jb_unread_quotes) -> None:
	outlook = win32com.client.Dispatch('outlook.application', pythoncom.CoInitialize())
	mapi = outlook.GetNamespace("MAPI")
	
	#Provisional fins tenir acces a bus@janer-bus.com a outlook
	jb_messages = mapi.Folders("contact@vptmallorca.com").Folders(1).Items
    
	for msg in list(jb_messages):
		if msg.UnRead == True:
			if msg.Subject.startswith('REQUEST NR:') or msg.Subject.startswith('Fwd: REQUEST NR:') or msg.Subject.startswith('BESTELLUNG NR:') or msg.Subject.startswith("Fwd: BESTELLUNG NR:"):
				jb_unread_bookings.append(msg)
			elif msg.Subject.startswith('Presupuesto de') or msg.Subject.startswith('Transferpreise vom'):
				jb_unread_quotes.append(msg)

def jb_get_booking_class(msg_body) -> Booking:
	"""Retrieves the booking information from the mail body and returns a Booking object"""
	booking_info = [[]]

	multiple_line_mail = msg_body.split('\r\n')
	for line in multiple_line_mail:
		booking_info.append(line.split(':'))

	print(booking_info[18][1])

	booking = Booking(None, booking_info[3][1][2:-1].split(' ')[0], booking_info[3][1][2:-2], booking_info[4][1][2:-8], booking_info[5][1][2:-2],booking_info[30][0][1:-2], None, None, None, None, None, None,None, None, None,None ,None,None,None, None, None, None, None, None, None, None, None, "Pending", None)


	if(booking_info[6][0] in ["ARRIVAL TRANSFER", "HINFAHRT"]):
		booking.pick_up_arrival = booking_info[10][0][1:-2].lower().capitalize()
		booking.destination_arrival = booking_info[17][0][1:-2].lower().capitalize()
		booking.arrival_date = booking_info[8][0][1:-2]
		booking.arrival_time =  booking_info[12][0][1:] + ":" + booking_info[12][1][:-2]
		booking.flight_n_arrival = booking_info[14][0][1:-2]

	if (booking_info[18][0] in ["DEPARTURE TRANSFER", "RÜCKFAHRT"]):
		
		booking.pick_up_departure = booking_info[24][0][1:-2].lower().capitalize()
		booking.destination_departure = "Palma Airport"
		booking.departure_date = booking_info[20][0][1:-2]
		booking.pick_up_time = booking_info[22][0][1:] + ":" + booking_info[22][1][:-2]
		booking.departure_time = booking_info[28][0][1:] + ":" + booking_info[28][1][:-2] 
		booking.flight_n_departure = booking_info[26][0][1:-2]
	

	#booking = Booking(None, booking_info[3][1][2:-1].split(' ')[0], booking_info[3][1][2:-2], booking_info[4][1][2:-8], booking_info[5][1][2:-2],booking_info[30][0][1:-2],booking_info[10][0][1:-2].lower().capitalize(), booking_info[17][0][1:-2].lower().capitalize(), booking_info[8][0][1:-2], booking_info[12][0][1:] + ":" + booking_info[12][1][:-2], booking_info[14][0][1:-2],booking_info[24][0][1:-2].lower().capitalize(),"Palma Airport", booking_info[20][0][1:-2], booking_info[22][0][1:] + ":" + booking_info[22][1][:-2],booking_info[28][0][1:] + ":" + booking_info[28][1][:-2] ,booking_info[26][0][1:-2],None,None, None, None, None, None, None, None, None, None, "Pending", None)

	return booking

def jb_manage_bookings()-> list:
	""" updates and manages bookings, returns a list with all the new bookings"""
	jb_unread_bookings = []
	jb_unread_quotes = []
	jb_bookings = []

	# updates global variables with new unread messages
	jb_get_unread_messages(jb_unread_bookings, jb_unread_quotes)
	for i in range(0, len(jb_unread_bookings)):
		# pre-process the e-mail in order to treat it correctly
		subject = jb_unread_bookings[i].Subject

		# get booking class
		booking = jb_get_booking_class(jb_unread_bookings[i].Body)

		# check the language of the e-mail and store the language.
		if subject.startswith('REQUEST') or subject.startswith('Re: VPTMallorca Quote'):
			booking.language = 'ENG'
		elif subject.startswith('Reserva de'):
			booking.language = 'DE'
		else:
			booking.language = 'ESP'
		booking.body = jb_unread_bookings[i].Body

		#CONTROL
		if "marcjanerferrer@gmail.com" in booking.email:
			jb_bookings.append(booking)

	return jb_bookings

#------------------------------------ENG--------------------------------------#

def jb_send_booking_confirmation_eng(booking : Booking):
	message = tmplt.jb_eng_booking_confirmation(booking)

	send_message(booking.email, "contact@vptmallorca.com", "Transfer confirmation " + booking.booking_number, message)

def jb_reject_booking_eng(booking : Booking):
	message = tmplt.jb_eng_reject_booking(booking)

	send_message(booking.email, "contact@vptmallorca.com", "VPTMallorca transfer", message)

def jb_send_quote_eng(quote : Quote):
	assert quote.language == "ENG"
	message = tmplt.jb_eng_quote(quote)

	send_message(quote.email, "contact@vptmallorca.com", "VPTMallorca Quote", message)


#-------------------------------------DE--------------------------------------#
def jb_send_booking_confirmation_de(booking : Booking):
	assert booking.language == "DE"

	message = tmplt.jb_de_booking_confirmation(booking)
	send_message(booking.email, "contact@vptmallorca.com", "Buchungsbestätigung VPT" + booking.booking_number, message)

def jb_reject_booking_de(booking : Booking):
	message = tmplt.jb_de_reject_booking(booking)

	send_message(booking.email, "contact@vptmallorca.com", "VPTMallorca transfer", message)

def jb_send_quote_de(quote : Quote):
	assert quote.language == "DE"
	message = tmplt.jb_de_quote(quote)

	send_message(quote.email, "contact@vptmallorca.com", "Janer-Bus Quote", message)

#-------------------------------------ES--------------------------------------#
def jb_send_booking_confirmation_es(booking : Booking):
	assert booking.language == "ES"

	message = tmplt.jb_es_booking_confirmation(booking)

	send_message(booking.email, "contact@vptmallorca.com", "Confirmación de reserva " + booking.booking_number, message)

def jb_reject_booking_es(booking : Booking):
	assert booking.language == "ES"
	message = tmplt.jb_es_reject_booking(booking)

	send_message(booking.email, "contact@vptmallorca.com", "VPTMallorca transfer", message)

def vpt_send_quote_es(quote : Quote):
	assert quote.language == "ES"
	message = tmplt.jb_de_quote(quote)

	send_message(quote.email, "contact@vptmallorca.com", "Janer-Bus Quote", message)


def jb_main():
	jb_bookings = jb_manage_bookings()

	print(len(jb_bookings))
	
	for mail in jb_bookings:
		print(mail)
		print(" ")


jb_main()