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
vpt_unread_bookings_eng = list
vpt_unread_quotes_eng = list

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
	subtotal: int
	total:int


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

	global vpt_unread_bookings_eng
	vpt_unread_bookings_eng = []
	global vpt_unread_quotes_eng
	vpt_unread_quotes_eng = []

	# global vpt_unread
	for msg in list(vpt_messages):
		if msg.UnRead == True:
			if msg.Subject.startswith('Transfer de') or msg.Subject.startswith('Re: VPTMallorca Quote'):
				vpt_unread_bookings_eng.append(msg)
			elif msg.Subject.startswith('Presupuesto de'):
				vpt_unread_quotes_eng.append(msg)



def vpt_summarize_bookings() -> list[VPT_booking]:

def vpt_summarize_quotes() -> list[VPT_quote]:

def vpt_send_booking_confirmation_eng(booking_id : int):
	booking : VPT_booking = vpt_bookings[booking_id]
	message = tmplt.vpt_eng_booking_confirmation(booking)

	send_mail(booking.email, "contact@vptmallorca.com", "Transfer confirmation VPT" + booking.booking_number, message)

def vpt_send_quote_eng(quote_id : int):
	quote = VPT_quote = vpt_quotes[quote_id]
	message = tmplt.vpt_eng_quote(quote)

	send_mail(quote.email, "contact@vptamllorca.com", "VPTMallorca Quote", message)




def main():
	vpt_get_unread_messages()
	vpt_summarize_bookings(vpt_unread_bookings_eng)
	vpt_summarize_quotes(vpt_unread_quotes_eng)


main()

# --------------------------------------------------------------------------- #
#                              JANERBUS MODULES                               #
# --------------------------------------------------------------------------- #
