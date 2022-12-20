import streamlit as st
from bs4 import BeautifulSoup
from streamlit_option_menu import option_menu
import outlook as otl
from typing_extensions import TypeAlias
import json

def read_json(filename):
    with open(filename) as f:
        dataset= json.load(f)
    return dataset

def auth(username, password) -> bool:
    users = read_json("auth.json")
    for user in users["users"]:
        if user["username"] == username and user["password"] == password:
            return True
    return False

def apply_styles() -> None:
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

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

def show_hero() -> None:
    show("hero")

def show_messages() -> None:
    return True

def send_booking(index, booking_number, price, town):
    return True

def inputs_filled(inputs):
    for input in inputs:
        if len(input) == 0:
            return False
    return True

def decrease_index(len):
    st.session_state.index = (st.session_state.index - 1)%len
def increase_index(len):
    st.session_state.index = (st.session_state.index + 1)%len

def show_booking(variables):
    st.markdown(get_html_by_id("booking").format(
        index = variables[0]
    ), unsafe_allow_html = True)

def bookings() -> None:

    if "disabled" not in st.session_state:
        st.session_state["disabled"] = True
    if "index" not in st.session_state:
        st.session_state["index"] = 0

    show("booking_hero")

    right_left, right_right = st.columns(2)

    bookings_len = 5
    with right_left:
        st.button("Previous", on_click = decrease_index, args= (bookings_len,))
    with right_right:
        st.button("Next", on_click = increase_index, args = (bookings_len,))

    left,right = st.columns(2)

    with left:
        index = st.text_input("Booking index")
        booking_number = st.text_input("Booking number")
        price = st.text_input("Price per transfer")
        town = st.text_input("Destination town")
        inputs = [index, booking_number, price, town]

        if(inputs_filled(inputs)):
            st.session_state["disabled"] = False
        else:
            st.session_state["disabled"] = True

        st.button("Answer", on_click = send_booking, args = (index,booking_number,price,town), disabled = st.session_state.disabled)
    with right:
        show_booking([st.session_state.index])


def quotes() -> None:
    show("quote_hero")

def main() -> None:
    apply_styles()
    show_hero()

    #MENU
    menu = page_menu()
    if menu == "Bookings":
        bookings()
    elif menu == "Quotes":
        quotes()

def initialize():

    with st.sidebar:
        st.header("Log in")
        username = st.text_input("Username")
        password = st.text_input("Password", type = "password")

    username = "marc.janer"
    password = "prova"

    if(auth(username, password)):
        main()

initialize()
