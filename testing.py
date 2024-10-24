import streamlit as st
import sqlite3
import pandas as pd
import base64
from PyPDF2 import PdfReader
import pytesseract
from PIL import Image
import io
import camelot

# Database setup
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    conn.close()

# Function to register a new user
def register_user(username, password):
    try:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        st.success("Registration successful! You can now log in.")
    except sqlite3.IntegrityError:
        st.error("Username already exists. Please choose a different username.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
    finally:
        conn.close()

# Function for the login page
def login():
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        try:
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            user = c.fetchone()
            if user:
                st.success(f"Welcome, {username}!")
                return True
            else:
                st.error("Invalid username or password.")
                return False
        except Exception as e:
            st.error(f"An error occurred: {e}")
        finally:
            conn.close()
    return False

# Function for the registration page
def register():
    st.title("Registration Page")
    username = st.text_input("Choose a Username")
    password = st.text_input("Choose a Password", type="password")

    if st.button("Register"):
        if username and password:
            register_user(username, password)
        else:
            st.error("Please fill in both fields.")

# Load default timetable data extracted from the CSV
@st.cache_data
def load_default_timetable():
    data = {
        "Time": ["09-10 AM", "10-11 AM", "11-12 AM", "12-01 PM", "01-02 PM", "02-03 PM", "03-04 PM", "04-05 PM"],
        "Monday": [
            "Lecture / G:All C:PEV112 / R: 56-703 / S:BO301",
            "Lecture / G:All C:PEA402 / R: 56-605 / S:BO301",
            "Lecture / G:All C:BTY496 / R: 56-708 / S:B2201",
            "",
            "Lecture / G:All C:BTY463 / R: 56-809 / S:B2201",
            "",
            "Lecture / G:All C:BTY441 / R: 56-801 / S:BM302",
            ""
        ],
        "Tuesday": [
            "Lecture / G:All C:PEV112 / R: 56-703 / S:BO301",
            "Lecture / G:All C:PEA402 / R: 56-605 / S:BO301",
            "Lecture / G:All C:BTY496 / R: 56-607 / S:B2201",
            "",
            "Lecture / G:All C:BTY651 / R: 56-710 / S:BE098",
            "",
            "",
            ""
        ],
        "Wednesday": [
            "Practical / G:1 C:PEV112 / R: 56-703 / S:BO301",
            "Practical / G:1 C:PEV112 / R: 56-703 / S:BO301",
            "Lecture / G:All C:BTY651 / R: 56-710 / S:BE098",
            "Lecture / G:All C:BTY651 / R: 56-609 / S:BE098",
            "Lecture / G:All C:BTY396 / R: 56-710 / S:B2201",
            "",
            "",
            ""
        ],
        "Thursday": [
            "",
            "",
            "",
            "Lecture / G:All C:BTY441 / R: 56-707 / S:BM302",
            "",
            "Tutorial / G:1 C:PEA402 / R: 56-509 ( Makeup Class ) / S:BO301",
            "",
            ""
        ],
        "Friday": [
            "Tutorial / G:1 C:PEA402 / R: 56-801 / S:BO301",
            "",
            "",
            "Lecture / G:All C:PESS01 / R: 56-510 / S:9B51R",
            "Lecture / G:All C:BTY396 / R: 56-710 / S:B2201",
            "Practical / G:2 C:BTY464 / R: 55-303 / S:B2201",
            "Practical / G:2 C:BTY416 / R: 57A-402 / S:B2201",
            ""
        ],
        "Saturday": [
            "Lecture / G:All C:PESS01 / R: 56-510 / S:9B51R",
            "Project Work/ Other Weekly Activities. Check Schedule Below",
            "",
            "",
            "",
            "",
            "",
            ""
        ]
    }
    return pd.DataFrame(data)

# Load course information
@st.cache_data
def load_course_info():
    course_data = {
        "CourseCode": ["BTY396", "BTY416", "BTY441", "BTY463", "BTY464", "BTY496", "BTY499", "BTY651", "ICT202B", "PEA402", "PESS01", "PEV112"],
        "CourseType": ["CR", "CR", "EM", "CR", "CR", "CR", "CR", "PW", "CR", "OM", "PE", "OM"],
        "CourseName": ["BIOSEPARATION ENGINEERING", "BIOSEPARATION ENGINEERING LABORATORY", "PHARMACEUTICAL ENGINEERING", 
                       "BIOINFORMATICS AND COMPUTATIONAL BIOLOGY", "BIOINFORMATICS AND COMPUTATIONAL BIOLOGY LABORATORY", 
                       "METABOLIC ENGINEERING", "SEMINAR ON SUMMER TRAINING", "QUALITY CONTROL AND QUALITY ASSURANCE", 
                       "AI, ML AND EMERGING TECHNOLOGIES", "ANALYTICAL SKILLS -II", "MENTORING - VII", "VERBAL ABILITY"],
        "Credits": [3, 1, 3, 2, 1, 2, 3, 3, 2, 4, 0, 3],
        "Faculty": ["Dr. Ajay Kumar", "Dr. Ajay Kumar", "Dr. Shashank Garg", "Dr. Anish Kumar", 
                    "Dr. Anish Kumar", "Dr. Shashank Garg", "", "Dr. Aarti Bains", 
                    "Dr. Piyush Kumar Yadav", "Kamal Deep", "", "Jaskiranjit Kaur"]
    }
    return pd.DataFrame(course_data)

# Function to display uploaded PDF
import base64

def display_pdf(pdf_file):
    # Display the PDF file using an iframe for an interactive viewer
    pdf_data = pdf_file.read()
    base64_pdf = base64.b64encode(pdf_data).decode('utf-8')
    
    # Embed the PDF within the app with adjustable width and height
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# Function to extract timetable from CSV
def extract_timetable_from_csv(csv_file):
    try:
        return pd.read_csv(csv_file)
    except Exception as e:
        st.error(f"Error reading CSV file: {e}")
        return load_default_timetable()

# Function to extract timetable from images
def extract_timetable_from_image(image_file):
    try:
        # Use PIL to open the image
        image = Image.open(image_file)
        # Use pytesseract to do OCR on the image
        text = pytesseract.image_to_string(image)
        # Here you may want to parse the text to extract timetable data
        # For simplicity, we will return the extracted text wrapped in a DataFrame
        return pd.DataFrame({"Extracted": [text]})
    except Exception as e:
        st.error(f"Error processing the image: {e}")
        return load_default_timetable()

def home():
    st.title("Academic Schedule and Course Information")
    st.write("Welcome to the Home Page of the multi-page app.")
    
    # Load the default timetable data
    timetable_df = load_default_timetable()  # Load the timetable data
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["Weekly Schedule", "Course Information", "PDF View"])
    
    with tab1:
        st.subheader("Weekly Class Schedule")

        # Add a button to upload the user's timetable in different formats
        uploaded_timetable_pdf = st.file_uploader("Upload your timetable PDF", type="pdf")
        uploaded_timetable_csv = st.file_uploader("Upload your timetable CSV", type="csv")
        uploaded_timetable_image = st.file_uploader("Upload your timetable Image", type=["jpg", "jpeg", "png"])

        if uploaded_timetable_pdf is not None:
            timetable_df = extract_timetable_from_pdf(uploaded_timetable_pdf)

        elif uploaded_timetable_csv is not None:
            timetable_df = extract_timetable_from_csv(uploaded_timetable_csv)

        elif uploaded_timetable_image is not None:
            timetable_df = extract_timetable_from_image(uploaded_timetable_image)
        

        # Display the updated or default timetable
    st.dataframe(timetable_df)  # Show the timetable
    
    with tab2:
        st.subheader("Course Information")
        course_info_df = load_course_info()  # Load course info
        st.dataframe(course_info_df)  # Display course information

    with tab3:
        st.subheader("Upload and View PDF")
        uploaded_pdf = st.file_uploader("Choose a PDF file", type="pdf")
        if uploaded_pdf is not None:
            display_pdf(uploaded_pdf)

import spacy
from PyPDF2 import PdfReader
import re

# Load a pre-trained spaCy model for NLP
nlp = spacy.load("en_core_web_sm")

def extract_timetable_from_pdf(pdf_file):
    try:
        # Read the uploaded PDF file
        pdf_data = pdf_file.read()
        
        # Create a BytesIO object from the PDF data
        from io import BytesIO
        pdf_bytes = BytesIO(pdf_data)
        
        # Pass the BytesIO object to PdfReader or camelot.read_pdf()
        pdf_reader = PdfReader(pdf_bytes)
        text = ""

        # Extract text from each page of the PDF
        for page in pdf_reader.pages:
            text += page.extract_text()

        # Pass the text to an AI/NLP model (e.g., spaCy) for structured extraction
        doc = nlp(text)

        # Example Regex for timetable pattern (modify based on format)
        pattern = re.compile(r'(\d{2}-\d{2} (AM|PM))\s(.*)')
        matches = pattern.findall(text)

        # If matches are found, process them to create a structured dataframe
        data = {
            "Time": [],
            "Monday": [],
            "Tuesday": [],
            "Wednesday": [],
            "Thursday": [],
            "Friday": [],
            "Saturday": [],
            # ... fill in the remaining days
        }

        for match in matches:
            time, session = match[0], match[2]
            # Add logic to map session to specific days and update data

        # Return the structured timetable as a pandas DataFrame
        return pd.DataFrame(data)

    except Exception as e:
        st.error(f"Error extracting timetable from PDF: {e}")
        return load_default_timetable()
import camelot

def extract_timetable_from_pdf(pdf_file):
    try:
        # Read the uploaded PDF file
        pdf_data = pdf_file.read()
        
        # Create a BytesIO object from the PDF data
        from io import BytesIO
        pdf_bytes = BytesIO(pdf_data)
        
        # Pass the BytesIO object to camelot.read_pdf()
        # Read the PDF using Camelot for table extraction
        tables = camelot.read_pdf(pdf_file, pages='all', flavor='stream')
        if tables:
            timetable_df = tables[0].df  # Extract the first table
            return timetable_df
        else:
            st.error("No table found in the PDF.")
            return load_default_timetable()

    except Exception as e:
        st.error(f"Error extracting timetable from PDF: {e}")
        return load_default_timetable()
import pytesseract
from PIL import Image

def extract_timetable_from_image_pdf(pdf_file):
    try:
        images = convert_from_path(pdf_file)
        text = ""
        for image in images:
            text += pytesseract.image_to_string(image)
        
        # Process the extracted text as needed using regex or NLP models
        
    except Exception as e:
        st.error(f"Error extracting timetable from PDF: {e}")
        return load_default_timetable()



# Function for the about page
def about():
    st.title("Simulation")
    st.write("Implement simulations")

# Function for the contact page
def contact():
    st.title("Questions")
    st.write("Welcome to the Engaging Page.")

# Function for the projects page
def projects():
    st.title("Reading Material")
    st.write("Here are some flashcards/reading material to engage students.")

# Define the main app with navigation after successful login
def main():
    st.sidebar.title("Navigation")
        # Create the menu with subpage options
    page = st.sidebar.selectbox("Choose a page", ("Home", "Simulation", "Reading Material", "Questions"))

    # Navigate to the selected page
    if page == "Home":
        home()
    elif page == "Simulation":
        about()
    elif page == "Reading Material":
        projects()
    elif page == "Questions":
        contact()

# Define the login flow
def app():
    init_db()  # Initialize the database
    if "login_status" not in st.session_state:
        st.session_state.login_status = False

    if not st.session_state.login_status:
        choice = st.sidebar.selectbox("Select Action", ("Login", "Register"))
        if choice == "Login":
            st.session_state.login_status = login()
        else:
            register()

    if st.session_state.login_status:
        main()

# Run the app
if _name_ == "_main_":
    app()

    #working well but not accecting the pdf file