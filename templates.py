from typing_extensions import TypeAlias

from dataclasses import dataclass


def vpt_eng_booking_confirmation(booking):

    body = open("TEMPLATES/HTML/vpt_booking_eng.html").read().format(booking_number=booking.booking_number, name = booking.name, fullname=booking.fullname, email = booking.email, phone=booking.phone, pax=booking.pax, pick_up_arrival=booking.pick_up_arrival, destination_arrival=booking.destination_arrival, arrival_date=booking.arrival_date, arrival_time=booking.arrival_time, flight_n_arrival=booking.flight_n_arrival, pick_up_departure=booking.pick_up_departure, destination_departure=booking.destination_departure, departure_date=booking.departure_date, departure_time=booking.departure_time, flight_n_departure=booking.flight_n_departure, origin=booking.origin, city=booking.city, total=booking.total, subtotal_first=booking.subtotal_first, subtotal_second=booking.subtotal_second, subtotal_third=booking.subtotal_third)

    return str(body, "utf-8")

def vpt_eng_quote(quote):

    body = open("TEMPLATES/HTML/vpt_quote_eng.html").read().format(name=quote.name, destination=quote.destination, subtotal=quote.subtotal, total=quote.total)

    return body


def vpt_de_booking_confirmation(booking):

    dict = {"booking_number": booking.booking_number, "name" :  booking.name, "fullname": booking.fullname, "email" :  booking.email, "phone": booking.phone, "pax": booking.pax, "pick_up_arrival": booking.pick_up_arrival, "destination_arrival": booking.destination_arrival, "arrival_date": booking.arrival_date, "arrival_time": booking.arrival_time, "flight_n_arrival": booking.flight_n_arrival, "pick_up_departure": booking.pick_up_departure, "destination_departure": booking.destination_departure, "departure_date": booking.departure_date, "pick_up_time": booking.departure_time, "flight_n_departure": booking.flight_n_departure, "origin": booking.origin, "city": booking.city, "total": booking.total, "subtotal_first": booking.subtotal_first, "subtotal_second": booking.subtotal_second, "subtotal_third": booking.subtotal_third}

    body = open("TEMPLATES/HTML/vpt_booking_de.html").read().format_map(dict)
    return body
