import streamlit as st
import pandas as pd

@st.cache_data
def load_default_timetable():
    data = {
        "Time": ["09-10 AM", "10-11 AM", "11-12 AM", "12-01 PM", "01-02 PM", "02-03 PM", "03-04 PM", "04-05 PM"],
        "Monday": ["Lecture / G:All C:PEV112 / R: 56-703 / S:BO301", "Lecture / G:All C:PEA402 / R: 56-605 / S:BO301", "Lecture / G:All C:BTY496 / R: 56-708 / S:B2201", "", "Lecture / G:All C:BTY463 / R: 56-809 / S:B2201", "", "Lecture / G:All C:BTY441 / R: 56-801 / S:BM302", ""],
        "Tuesday": ["Lecture / G:All C:PEV112 / R: 56-703 / S:BO301", "Lecture / G:All C:PEA402 / R: 56-605 / S:BO301", "Lecture / G:All C:BTY496 / R: 56-607 / S:B2201", "", "Lecture / G:All C:BTY651 / R: 56-710 / S:BE098", "", "", ""],
        "Wednesday": ["Practical / G:1 C:PEV112 / R: 56-703 / S:BO301", "Practical / G:1 C:PEV112 / R: 56-703 / S:BO301", "Lecture / G:All C:BTY651 / R: 56-710 / S:BE098", "Lecture / G:All C:BTY651 / R: 56-609 / S:BE098", "Lecture / G:All C:BTY396 / R: 56-710 / S:B2201", "", "", ""],
        "Thursday": ["", "", "", "Lecture / G:All C:BTY441 / R: 56-707 / S:BM302", "", "Tutorial / G:1 C:PEA402 / R: 56-509 / S:BO301", "", ""],
        "Friday": ["", "", "", "", "", "", "", ""]
    }
    return pd.DataFrame(data)

@st.cache_data
def load_course_info():
    course_data = {
        "CourseCode": ["BTY396", "BTY416", "BTY441", "BTY463", "BTY464", "BTY496", "BTY499", "BTY651", "ICT202B", "PEA402", "PEMS07", "PESS01", "PEV112"],
        "CourseType": ["CR", "CR", "EM", "CR", "CR", "CR", "CR", "PW", "CR", "OM", "PE", "PE", "OM"],
        "CourseName": ["BIOSEPARATION ENGINEERING", "BIOSEPARATION ENGINEERING LABORATORY", "PHARMACEUTICAL ENGINEERING", "BIOINFORMATICS AND COMPUTATIONAL BIOLOGY", "BIOINFORMATICS AND COMPUTATIONAL BIOLOGY LABORATORY", "METABOLIC ENGINEERING", "SEMINAR ON SUMMER TRAINING", "QUALITY CONTROL AND QUALITY ASSURANCE", "AI, ML AND EMERGING TECHNOLOGIES", "ANALYTICAL SKILLS -II", "MENTORING - VII", "SOFTSKILLS - I", "VERBAL ABILITY"],
        "Credits": [3, 1, 3, 2, 1, 2, 3, 3, 2, 4, 0, 0, 3],
        "Faculty": ["Dr. Ajay Kumar", "Dr. Ajay Kumar", "Dr. Shashank Garg", "Dr. Anish Kumar", "Dr. Anish Kumar", "Dr. Shashank Garg", "", "Dr. Aarti Bains", "Dr. Piyush Kumar Yadav", "Kamal Deep", "", "Ayush Srivastava", "Jaskiranjit Kaur"]
    }
    return pd.DataFrame(course_data)

def get_llminfo():
    st.sidebar.header("Options", divider='rainbow')
    model = st.sidebar.radio("Choose LLM:", ("gemini-1.5-pro", "gemini-1.5-flash", "gemini-1.5-standard", "gemini-1.5-advanced"))
    temperature = st.sidebar.slider("Temperature:", 0.0, 2.0, 1.0, 0.25)
    top_p = st.sidebar.slider("Top P:", 0.0, 1.0, 0.94, 0.01)
    max_tokens = st.sidebar.slider("Maximum Tokens:", 100, 5000, 2000, 100)
    top_k = st.sidebar.slider("Top K:", 0, 100, 50, 1)
    return model, temperature, top_p, max_tokens, top_k
