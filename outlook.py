from typing_extensions import TypeAlias
from dataclasses import dataclass
import templates as tmplt
import win32com.client

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
vpt_unread_bookings = list
vpt_unread_quotes = list

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

class VPT_quote:
	name:str
	pax: int
	destination: str
	price: str

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

def send_mail(to : str, from : str, subject : str, body : str):
	mail = outlook.CreateItem(0)
	mail.Subject = subject
	mail.To = to
	mail.From = from
	mail.HTMLbody = body
	mail.send()



# --------------------------------------------------------------------------- #
#                                VPT MODULES                                  #
# --------------------------------------------------------------------------- #

def vpt_get_unread_messages() -> list:
	vpt_messages = vpt_inbox.Items

	global vpt_unread_bookings
	vpt_unread_bookings = []
	global vpt_unread_quotes
	vpt_unread_quotes = []

	# global vpt_unread
	for msg in list(vpt_messages):
		if msg.UnRead == True:
			if msg.Subject.startswith('Transfer de'):
				vpt_unread_bookings.append(msg)
			elif msg.Subject.startswith('Presupuesto de'):
				vpt_unread_quotes.append(msg)



def vpt_summarize_bookings():

def vpt_summarize_quotes():

def vpt_send_booking_confirmation_eng(booking_id : int):
	booking : VPT_booking = vpt_bookings[booking_id]
	template = tmplt.vpt_eng_booking_confirmation()

	message = template.format(booking_number=booking.booking_number, name = booking.name, fullname=booking.fullname, email = booking.email, phone=booking.phone, pax=booking.pax, pick_up_arrival=booking.pick_up_arrival, destination_arrival=booking.destination_arrival, arrival_date=booking.arrival_date, arrival_time=booking.arrival_time, flight_n_arrival=booking.flight_n_arrival, pick_up_departure=booking.pick_up_departure, destination_departure=booking.destination_departure, departure_date=booking.destination_date, pick_up_time=booking.pick_up_time, fligh_n_departure=booking.fligh_n_departure, origin=booking.origin, city=bookin.city, total=booking.total, subtotal_first=booking.subtotal_first, subtotal_second=booking.subtotal_second, subtotal_third=booking.subtotal_third)

	send_mail(booking.email, "contact@vptmallorca.com", "Transfer confirmation VPT" + booking.booking_number, message)




def main():
	vpt_get_unread_messages()
	vpt_summarize_bookings(vpt_unread_bookings)
	vpt_summarize_quotes(vpt_unread_quotes)


main()

# --------------------------------------------------------------------------- #
#                              JANERBUS MODULES                               #
# --------------------------------------------------------------------------- #
