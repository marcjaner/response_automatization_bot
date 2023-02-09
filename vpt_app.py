import streamlit as st
from bs4 import BeautifulSoup
from streamlit_option_menu import option_menu
import outlook as otl
import vpt_app as vpt
from typing_extensions import TypeAlias
import json

def page_menu():
    option = option_menu(
           menu_title = None,
           options = ["Bookings", "Quotes"],
           orientation = "horizontal",
           default_index = 0,
           styles = {
                "container":{"padding": "0!important", "background-color" : "#f8f8f8"},
                "icon" : { "font-size": "18px"},
                "margin-top" : "5%",
                "nav-link": {
                    "font-size" : "18px",
                    "text-align" : "center",
                    "margin-left" : "10px",
                    "..hover-color": "#eee"
                }
           }
        )
    return option

def get_html_by_id(id) -> str:
    with open("index.html") as f:
        html = f.read()
        soup = BeautifulSoup(html, "html.parser")
        return str(soup.find(id = id))

def show(id:str) -> None:
    st.markdown(get_html_by_id(id), unsafe_allow_html = True)

def show_hero(page) -> None:
    show(page + "_hero")

def show_messages() -> None:
    return True

def reply_vpt_quote(index, price):
    index = int(index)
    price = int(price)

    try:
        assert index < len(st.session_state.vpt_quotes)

        quote = st.session_state.vpt_quotes[index]

        quote.subtotal = price
        quote.total = price * 2

        assert quote.status == "Pending"
        if quote.language == "ENG":
            otl.vpt_send_quote_eng(quote)
        elif quote.language == "DE":
            otl.vpt_send_quote_de(quote)
        elif quote.language == "ES":
            otl.vpt_send_quote_es(quote)

        quote.status = "answered"
        otl.mark_as_read(quote)

    except Exception as e:
        print(e)
        st.session_state.error_message = "This quote may have already been answered"

def accept_vpt_booking(index, booking_number, price, town):
    price = int(price)

    try:
        assert int(index) < int(len(st.session_state.vpt_bookings))

        booking = st.session_state.vpt_bookings[int(index)]

        booking.booking_number = booking_number

        booking.subtotal_first = str(price)
        booking.total = price * 2
        booking.subtotal_second = 10 * round(price *0.4 / 10)
        booking.subtotal_third = price - int(booking.subtotal_second)

        booking.city = town

        assert booking.status == "Pending"

        if booking.language == "ENG":
            otl.vpt_send_booking_confirmation_eng(booking)
        else:
            otl.vpt_send_booking_confirmation_de(booking)
        booking.status = "accepted"
        otl.mark_as_read(booking)
    except Exception as e:
        st.write(e)
        st.session_state.error_message = "Can't accept this booking, it may have already been answered"

def inputs_filled(inputs):
    for input in inputs:
        if len(input) == 0:
            return False
    return True

def index_input_filled(inputs):
    return len(inputs[0]) > 0

def decrease_quote_index(len):
    st.session_state.vpt_quote_index = (int(st.session_state.vpt_quote_index) - 1)%len

def increase_quote_index(len):
    st.session_state.vpt_quote_index = (int(st.session_state.vpt_quote_index) + 1)%len

def decrease_vpt_booking_index(len):
    st.session_state.vpt_booking_index = (st.session_state.vpt_booking_index - 1)%len

def increase_vpt_booking_index(len):
    st.session_state.vpt_booking_index = (st.session_state.vpt_booking_index + 1)%len

def transf_type(booking):
    if booking.destination_departure == '':
        return 'one-way'
    else:
        return 'return'

def show_vpt_booking(variables, id):
    vpt_bookings = variables[1]
    booking = vpt_bookings[variables[0]]


    st.markdown(get_html_by_id(id).format(
        index = variables[0],
        pick_up_arrival = booking.pick_up_arrival,
        destination_arrival = booking.destination_arrival,
        pax = booking.pax,
        arrival_date = booking.arrival_date,
        arrival_time = booking.arrival_time,
        flight_n_arrival = booking.flight_n_arrival,
        pick_up_departure = booking.pick_up_departure,
        destination_departure = booking.destination_departure,
        departure_date = booking.departure_date,
        departure_time = booking.departure_time,
        flight_n_departure = booking.flight_n_departure,
        status = booking.status,
        type = transf_type(booking)
    ), unsafe_allow_html = True)

def all_vpt_bookings():
    show("all_bookings")
    html = '<div id="bookings_grid">'

    for i in range(0, len(st.session_state.vpt_bookings)):
        booking = st.session_state.vpt_bookings[i]
        booking_html = '<div id="booking" class ="booking_item"><h3>Booking index: {index}</h3><p class="small {status}"> {status}</p><br /><h4 class= "{type}">Arrival transfer</h4><p>{pick_up_arrival} -> {destination_arrival}</p><p>{pax} pax | {arrival_date} | {arrival_time} | {flight_n_arrival}</p><h4 class= "{type}">Departure transfer</h4><p class= "{type}">{pick_up_departure} -> {destination_departure}</p><p class= "{type}">{pax} pax | {departure_date} | {departure_time} | {flight_n_departure}</p><h4>Additional comments</h4></div>'.format(
            index = i,
            pick_up_arrival = booking.pick_up_arrival,
            destination_arrival = booking.destination_arrival,
            pax = booking.pax,
            arrival_date = booking.arrival_date,
            arrival_time = booking.arrival_time,
            flight_n_arrival = booking.flight_n_arrival,
            pick_up_departure = booking.pick_up_departure,
            destination_departure = booking.destination_departure,
            departure_date = booking.departure_date,
            departure_time = booking.departure_time,
            flight_n_departure = booking.flight_n_departure,
            status = booking.status,
            type = transf_type(booking)
        )
        html += booking_html

    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

def set_index_cero():
    st.session_state.index = 0

def show_quote(variables):
    vpt_quotes = variables[1]
    quote = vpt_quotes[int(variables[0])]

    st.markdown(get_html_by_id("quote").format(
        index = variables[0],
        pax = quote.pax,
        destination = quote.destination,
        status = quote.status,
    ), unsafe_allow_html = True)

def get_vpt_bookings(vpt_bookings):

    st.session_state.vpt_bookings = otl.vpt_manage_bookings(vpt_bookings)

def vpt_get_quotes():
    st.session_state.vpt_quotes = otl.vpt_manage_quotes()

def reject_vpt_booking(index):

    assert index < len(st.session_state.vpt_bookings)

    booking = st.session_state.vpt_bookings[index]
    try:
        assert booking.status != "answered"

        if booking.language == "ENG":
            otl.vpt_reject_booking_eng(booking)
        elif booking.language == "DE":
            otl.vpt_reject_booking_de(booking)
        elif booking.language == "ES":
            otl.vpt_reject_booking_es(booking)

        booking.status = "rejected"
        otl.mark_as_read(booking)


    except:
        st.session_state.error_message = "It looks as this bookngs has already been answered"

def vpt_bookings() -> None:
    if "accept_disabled" not in st.session_state:
        st.session_state["vpt_accept_disabled"] = True
        st.session_state["vpt_reject_disabled"] = True
    if "vpt_booking_index" not in st.session_state:
        st.session_state["vpt_booking_index"] = 0

    if "vpt_bookings" not in st.session_state:
        st.session_state["vpt_bookings"] = []
    show("vpt_booking_hero")
    vpt_bookings = []
    st.button("Get bookings", on_click= get_vpt_bookings, args= (vpt_bookings,))

    bookings_len = len(st.session_state["vpt_bookings"])
    st.write("We have found " + str(bookings_len) + " bookings")
    show("spacer")

    right_left, right_right = st.columns(2)


    if bookings_len > 0:
        with right_left:
            st.button("  Previous", on_click = decrease_vpt_booking_index, args= (bookings_len,))
            with right_right:
                st.button("Next ", on_click = increase_vpt_booking_index, args = (bookings_len,))

        left,right = st.columns(2)

        with left:

            index = st.text_input("Booking index", value = st.session_state.vpt_booking_index)

            booking_number = st.text_input("Booking number")
            price = st.text_input("Price per transfer")
            town = st.text_input("Destination town")
            inputs = [index, booking_number, price, town]

            if(inputs_filled(inputs)):
                st.session_state["vpt_accept_disabled"] = False
            else:
                st.session_state["vpt_accept_disabled"] = True

            if(index_input_filled(inputs)):
                st.session_state["vpt_reject_disabled"] = False
            else:
                st.session_state["vpt_reject_disabled"] = True

            st.button("Accept", on_click = accept_vpt_booking, args = (index,booking_number,price,town), disabled = st.session_state.vpt_accept_disabled)

            st.button("Reject", disabled = st.session_state.vpt_reject_disabled, on_click = reject_vpt_booking, args = (int(index),))
        with right:


            variables = [st.session_state.vpt_booking_index, st.session_state.vpt_bookings]
            show_vpt_booking(variables, "booking")

        all_vpt_bookings()



        if st.session_state.error_message is not None:
            st.error(st.session_state.error_message)
            st.session_state.error_message = None
    else:
        st.info('It looks that there are no unread bookings. Press the"Get bookings" button to refresh' )

def vpt_quotes() -> None:

    if "vpt_quotes" not in st.session_state:
        st.session_state["vpt_quotes"] = []

    show("vpt_quote_hero")
    st.button("Get quotes", on_click = vpt_get_quotes)

    len_quote = len(st.session_state.vpt_quotes)
    st.write("We have found " + str(len_quote) + " quotes")

    show("spacer")

    if "reply_disabled" not in st.session_state:
        st.session_state["reply_disabled"] = True
    if "quote_index" not in st.session_state:
        st.session_state["quote_index"] = 0



    if len_quote > 0:
        left_top, right_top = st.columns(2)

        with left_top:
            st.button("Previous", on_click = decrease_quote_index, args = (len_quote,))
        with right_top:
            st.button("Next", on_click = increase_quote_index, args = (len_quote,))

        main_left, main_right = st.columns(2)

        with main_left:
            quote_index = st.text_input("Quote index", value = st.session_state["quote_index"])
            st.session_state["quote_index"] = quote_index
            quote_price = st.text_input("Transfer price")

            quote_inputs = [quote_index, quote_price]

            if inputs_filled(quote_inputs):
                st.session_state.reply_disabled = False
            else:
                st.session_state.reply_disabled = True

            st.button("Reply", disabled = st.session_state["reply_disabled"], on_click = reply_vpt_quote, args= (quote_index, quote_price,))

        with main_right:
            quote_variables = [int(st.session_state.quote_index), st.session_state.vpt_quotes]
            show_quote(quote_variables)

        if st.session_state.error_message is not None:
            st.error(st.session_state.error_message)
            st.session_state.error_message = None
    else:
        st.info("It looks as there are no unread quotes. Press the button in order to refresh the page")

def main() -> None:
    show_hero("vpt")

    #MENU
    menu = page_menu()
    if menu == "Bookings":
        vpt_bookings()
    elif menu == "Quotes":
        vpt_quotes()
