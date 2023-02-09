import streamlit as st
from bs4 import BeautifulSoup
from streamlit_option_menu import option_menu
import vpt_app as vpt
import jb_app as jb
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

def initialize():
    apply_styles()
    if "error_message" not in st.session_state:
        st.session_state.error_message = None

    with st.sidebar:
        st.header("Log in")
        username = st.text_input("Username")
        password = st.text_input("Password", type = "password")

    #username = "marc.janer"
    #password = "1234"

    if(auth(username, password)):
        with st.sidebar:
            option = option_menu(
            menu_title = None,
            options = ["VPTMallorca", "JanerBus"],
            orientation = "horizontal",
            default_index = 0,
            styles = {
                "container":{"padding": "0!important", "background-color" : "#f8f8f8"},
                "margin-top" : "5%",
                "nav-link": {
                    "font-size" : "12px",
                    "text-align" : "center",
                    "margin-left" : "5px",
                    "..hover-color": "#eee"
                }
           }
        )

        if option == "VPTMallorca":
            vpt.main()
        elif option == "JanerBus":
            jb.main()
        

initialize()
