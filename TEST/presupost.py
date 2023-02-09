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
class VPT_budget:
	name:str
	email:str
	destination: str
	pax: int
	subtotal: int
	total: int
	language : str
	status:str


vpt_unread_budgets = []

def vpt_get_unread_budgets() -> None:
    """ updates list of unread budgets """
    vpt_messages = vpt_inbox.Items
    for msg in list(vpt_messages):
        if msg.UnRead == True:
            if msg.Subject.startswith('Presupuesto de') or msg.Subject.startswith('Transferpreise vom'):
                vpt_unread_budgets.append(msg)

def treat_budget(msg_body : list)-> None:
    """ removes empty index """
    for string in msg_body:
        if string == '':
            msg_body.remove('')

def get_budget(msg_body: list)-> list:
	""" returns a list with the info needed to create an instance of VPT_budget """
	budget_info = []
	for string in msg_body:
		if ":" in string:
			budget_info.append(string.split(":")[1])
	return budget_info

def get_budget_class(budget_info: list)-> VPT_budget:
    """ from the info list, creates an instance of the budget class """
    budget = VPT_budget(budget_info[0],budget_info[1],budget_info[2],budget_info[3], None, None, None, None)
    return budget

def manage_budgets()->list:
    """ updates and manages budgets, returns a list of the unread budgets """
    vpt_get_unread_budgets()

    budgets = []
    assert len(vpt_unread_budgets)>0

    for i in range(0, len(vpt_unread_budgets)):
        # pre-process the e-mail in order to treat it correctly
        msg_body = vpt_unread_budgets[i].Body.replace("\n","").split("\r")
        subject = vpt_unread_budgets[i].Subject

        treat_budget(msg_body)

        budget_info = get_budget(msg_body)

        budget = get_budget_class(budget_info)

        if subject.startswith('Presupuesto de'):
            budget.language = 'ENG'
        elif subject.startswith('Transferpreise vom'):
            budget.language = 'DE'
        else:
            budget.language = 'ESP'

        budgets.append(budget)
    print(budgets)


manage_budgets()
