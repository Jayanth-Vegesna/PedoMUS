import streamlit as st
from utils import load_default_timetable, load_course_info
from reading_material import reading_material_page
from simulation import simulation_page
from questions import questions_page
from attendance import attendance_page

def home_page():
    st.sidebar.title("Navigation")
    selected_page = st.sidebar.selectbox("Choose a page:", ["Home", "Reading Material", "Simulation", "Questions", "Attendance"])
    if selected_page == "Home":
        st.title("Academic Schedule and Course Information")
        timetable_df = load_default_timetable()
        tab1, tab2 = st.tabs(["Weekly Schedule", "Course Information"])
        with tab1:
            st.subheader("Weekly Class Schedule")
            st.dataframe(timetable_df)
        with tab2:
            st.subheader("Course Information")
            course_info_df = load_course_info()
            st.dataframe(course_info_df)

    elif selected_page == "Reading Material":
        reading_material_page()
    elif selected_page == "Simulation":
        simulation_page()
    elif selected_page == "Questions":
        questions_page()
    elif selected_page == "Attendance":
        attendance_page()