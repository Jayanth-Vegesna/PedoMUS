import streamlit as st
from db import init_db
import sqlite3

def register_page():
    st.subheader("Register Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if password == confirm_password:
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            try:
                c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                st.success("Registered successfully! You can now log in.")
            except sqlite3.IntegrityError:
                st.error("Username already exists. Please choose a different one.")
            finally:
                conn.close()
        else:
            st.error("Passwords do not match.")
