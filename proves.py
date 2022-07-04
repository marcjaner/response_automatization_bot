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
	fligh_n_departure: str
	origin: str
	city: str
	total: int
	subtotal_first: int
	subtotal_second: int
	subtotal_third: int
	language : str
	status: str

vpt_unread_bookings_eng = []
vpt_unread_bookings_de = []

def vpt_get_unread_messages(vpt_unread_bookings_eng: List, vpt_unread_bookings_de: List) -> None:
	vpt_messages = vpt_inbox.Items
      #------------------------------ENG--------------------------------#
      #-------------------------------DE--------------------------------#
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

vpt_get_unread_messages(vpt_unread_bookings_eng, vpt_unread_bookings_de)
assert len(vpt_unread_bookings_eng)>0
print("MAIL ANGLÈS")
print(vpt_unread_bookings_eng[0])
print("MAIL ALEMANY")
assert len(vpt_unread_bookings_de)>0
print(vpt_unread_bookings_de[0])
