import streamlit as st
import google.generativeai as genai
from db import init_db
from home import home_page
from login import login_page
from register import register_page
from config import API_KEY

genai.configure(api_key=st.secrets["API_Key"])

init_db()
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    home_page()
else:
    st.sidebar.header("Login")
    choice = st.sidebar.selectbox("Login or Register", ("Login", "Register"))
    if choice == "Login": 
        login_page()
    else:
        register_page()
