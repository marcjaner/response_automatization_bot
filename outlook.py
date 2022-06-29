from typing_extensions import TypeAlias
from dataclasses import dataclass
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

# --------------------------------------------------------------------------- #
#                             JANERBUS VARIABLES                              #
# --------------------------------------------------------------------------- #
# jb = mapi.Folders("bus@janer-bus.com")
# jb_inbox = jb.Folders(1)
# jb_messages = jb_inbox.Items


# --------------------------------------------------------------------------- #
#                               GLOBAL MODULES                                #
# --------------------------------------------------------------------------- #

# def reply():


# --------------------------------------------------------------------------- #
#                                VPT MODULES                                  #
# --------------------------------------------------------------------------- #

def vpt_get_unread_messages():
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


#
# def vpt_summarize_bookings():
#
# def vpt_summarize_quotes():

def main():
	vpt_get_unread_messages()
	vpt_summarize_bookings(vpt_unread_bookings)
	vpt_summarize_quotes(vpt_unread_quotes)


main()

# --------------------------------------------------------------------------- #
#                              JANERBUS MODULES                               #
# --------------------------------------------------------------------------- #
