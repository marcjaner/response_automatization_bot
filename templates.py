from typing_extensions import TypeAlias

from dataclasses import dataclass


def vpt_eng_booking_confirmation():
    return open("TEMPLATES/HTML/vpt_booking_eng.html").read()
