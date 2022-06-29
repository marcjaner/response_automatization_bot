from typing_extensions import TypeAlias
from dataclasses import dataclass
import win32com.client


outlook = win32com.client.Dispatch('outlook.application')
mapi = outlook.GetNamespace("MAPI")

for account in mapi.Accounts:
	print(account.DeliveryStore.DisplayName)
