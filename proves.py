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

vpt_unread_bookings = []

def vpt_get_unread_messages(vpt_unread_bookings: list) -> None:
	vpt_messages = vpt_inbox.Items
      #------------------------------ENG--------------------------------#
      #-------------------------------DE--------------------------------#
	for msg in list(vpt_messages):
		if msg.UnRead == True:
			if msg.Subject.startswith('Transfer de') or msg.Subject.startswith('Re: VPTMallorca Quote') or 				msg.Subject.startswith('Reserva de'):
				vpt_unread_bookings.append(msg)


def treat_email(msg_body: list)-> None:
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


def manage_bookings()-> list:
	""" updates and manages bookings, returns a list with all the new bookings """
	# updates global variables with new unread messages
	vpt_get_unread_messages(vpt_unread_bookings)
	bookings = []
	assert len(vpt_unread_bookings)>0
	for i in range(0, len(vpt_unread_bookings)):
		# pre-process the e-mail in order to treat it correctly
		msg_body = vpt_unread_bookings[i].Body.replace("\n","").split("\r")
		subject = vpt_unread_bookings[i].Subject

		treat_email(msg_body)

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
		bookings.append(booking)
	return bookings

bookings = manage_bookings()
print(booking)
