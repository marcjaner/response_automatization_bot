from typing_extensions import TypeAlias
from dataclasses import dataclass
import templates as tmplt
import win32com.client
from win32printing import Printer
import pythoncom

outlook = win32com.client.Dispatch('outlook.application')
mapi = outlook.GetNamespace("MAPI")

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

booking = VPT_booking("VPT123-1609", "Marc", "Marc Janer", "marcjanerferrer@gmail.com", "636990408", "6", "round", "Palma Airport", "Alcudia", "06/07/2022", "10:35 pm", "VLG5678", "Alcudia", "Palma Airport", "14/07/2022", "9:00 am", "UX6730", None, None, "Palma Airport", "Alcudia", 144, 72, 30, 42, "DE", None)

def send_message(to : str, subject : str, body : str):
	mail = outlook.CreateItem(0)
	mail.Subject = subject
	mail.To = to
	mail.HTMLbody = body
	mail.Send()

def main():
    to = booking.email
    subject = "Booking confirmation " + booking.booking_number
    body = tmplt.vpt_eng_booking_confirmation(booking)
    print("Template formated")
    print(type(body))
    send_message(to, subject, body)
    print("Message sent")
main()
