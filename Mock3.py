import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader
import os
import time

USER_CREDENTIALS = {"admin": "password"}

def page_setup():
    st.title("Educational Dashboard")
    st.header("Mock 3")
    st.markdown("---")
    
    hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """
    st.markdown(hide_menu_style, unsafe_allow_html=True)

def login_page():
    st.title("Login Page")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username and password:
            with st.spinner("Logging in..."):
                time.sleep(1) 
                if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
                    st.session_state.logged_in = True
                    st.success("Logged in successfully!")
                else:
                    st.error("Invalid credentials. Please try again.")
        else:
            st.error("Please enter both username and password.")

def home_page():
    st.sidebar.title("Navigation")
    
    selected_page = st.sidebar.radio("Select a page:", 
                                      ("Home", "Reading Material", "Simulation", "Questions"))

    st.sidebar.markdown("<style>h2 {color: #0073e6;}</style>", unsafe_allow_html=True)

    if selected_page == "Home":
        st.subheader("Welcome to the Home Page")
        st.write("This application allows you to interact with various media types.")
        st.write("Use the sidebar to navigate to different sections.")
        st.markdown("---")
    elif selected_page == "Reading Material":
        reading_material_page()
    elif selected_page == "Simulation":
        simulation_page()
    elif selected_page == "Questions":
        questions_page()

def reading_material_page():
    st.subheader("Reading Material Interaction")

    model, temperature, top_p, max_tokens, top_k = get_llminfo()

    typepdf = st.radio("Select the type of media to interact with:", ("PDF", "Images", "Videos"), index=0)

    if typepdf == "PDF":
        st.write("You selected PDF. Upload your files below.")
        uploaded_files = st.file_uploader("Choose one or more PDFs", type='pdf', accept_multiple_files=True)
        if uploaded_files:
            text = ""
            for pdf in uploaded_files:
                pdf_reader = PdfReader(pdf)
                for page in pdf_reader.pages:
                    text += page.extract_text()
            
            generation_config = {
                "temperature": temperature,
                "top_p": top_p,
                "max_output_tokens": max_tokens,
                "top_k": top_k,
                "response_mime_type": "text/plain",
            }
            model_instance = genai.GenerativeModel(
                model_name=model,
                generation_config=generation_config,
            )
            st.write(model_instance.count_tokens(text))
            question = st.text_input("Enter your question and hit return.")
            if question:
                response = model_instance.generate_content([question, text])
                st.write(response.text)

    elif typepdf == "Images":
        st.write("You selected Images. Upload your image file below.")
        image_file = st.file_uploader("Upload your image file.", type=["jpg", "jpeg", "png"])
        if image_file:
            temp_file_path = image_file.name
            with open(temp_file_path, "wb") as f:
                f.write(image_file.getbuffer())
            
            st.write("Uploading image...")
            uploaded_image = genai.upload_file(path=temp_file_path)
            while uploaded_image.state.name == "PROCESSING":
                time.sleep(5)
                uploaded_image = genai.get_file(uploaded_image.name)
            
            if uploaded_image.state.name == "FAILED":
                st.error("Failed to process image.")
                return
            
            st.write("Image uploaded successfully. Enter your prompt below.")
            prompt2 = st.text_input("Enter your prompt for the image.")
            if prompt2:
                generation_config = {
                    "temperature": temperature,
                    "top_p": top_p,
                    "max_output_tokens": max_tokens,
                }
                model_instance = genai.GenerativeModel(model_name=model, generation_config=generation_config)
                response = model_instance.generate_content([uploaded_image, prompt2])
                st.markdown(response.text)

                genai.delete_file(uploaded_image.name)

    elif typepdf == "Videos":
        st.write("You selected Videos. Upload your video file below.")
        video_file = st.file_uploader("Upload your video file.", type=["mp4", "mov", "avi"])
        if video_file:
            temp_file_path = video_file.name
            with open(temp_file_path, "wb") as f:
                f.write(video_file.getbuffer())

            st.write("Uploading video...")
            uploaded_video = genai.upload_file(path=temp_file_path)
            while uploaded_video.state.name == "PROCESSING":
                time.sleep(5)
                uploaded_video = genai.get_file(uploaded_video.name)

            if uploaded_video.state.name == "FAILED":
                st.error("Failed to process video.")
                return
            
            st.write("Video uploaded successfully. Enter your prompt below.")
            prompt3 = st.text_input("Enter your prompt for the video.")
            if prompt3:
                model_instance = genai.GenerativeModel(model_name=model)
                response = model_instance.generate_content([uploaded_video, prompt3])
                st.markdown(response.text)

                genai.delete_file(uploaded_video.name)  

def simulation_page():
    st.subheader("Simulation Page")
    st.write("Here are the simulations:")
    iframe_code_gene_expression = """
    <iframe src="https://phet.colorado.edu/sims/html/gene-expression-essentials/latest/gene-expression-essentials_en.html"
        width="650"
        height="500"
        allowfullscreen>
    </iframe>
    """
    iframe_code_beers_law = """
    <iframe src="https://phet.colorado.edu/sims/html/beers-law-lab/latest/beers-law-lab_en.html"
        width="650"
        height="500"
        allowfullscreen>
    </iframe>
    """
    iframe_code_keplers_laws = """
    <iframe src="https://phet.colorado.edu/sims/html/keplers-laws/latest/keplers-laws_en.html"
        width="650"
        height="500"
        allowfullscreen>
    </iframe>
    """
    st.components.v1.html(iframe_code_gene_expression, height=600)
    st.components.v1.html(iframe_code_beers_law, height=600)
    st.components.v1.html(iframe_code_keplers_laws, height=600)
    
def get_llminfo():
    st.sidebar.header("Options", divider='rainbow')
    model = st.sidebar.radio("Choose LLM:", 
                              ("gemini-1.5-pro", "gemini-1.5-flash", "gemini-1.5-standard", "gemini-1.5-advanced"))
    temperature = st.sidebar.slider("Temperature:", 0.0, 2.0, 1.0, 0.25, 
                                      help="Lower temp for deterministic, higher for creative results")
    top_p = st.sidebar.slider("Top P:", 0.0, 1.0, 0.94, 0.01, 
                               help="Lower for less random, higher for more random")
    max_tokens = st.sidebar.slider("Maximum Tokens:", 100, 5000, 2000, 100, 
                                     help="Max output tokens")
    top_k = st.sidebar.slider("Top K:", 0, 100, 50, 1, 
                               help="Number of top candidates to consider during sampling")
    return model, temperature, top_p, max_tokens, top_k

def questions_page():
    st.subheader("Questions Page")
    
    model, temperature, top_p, max_tokens, top_k = get_llminfo()

    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_file is not None:
        text = ""
        pdf_reader = PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        st.text_area("Extracted Text", value=text, height=300)

        if st.button("Generate MCQs"):
            if text:
                generation_config = {
                    "temperature": temperature,
                    "top_p": top_p,
                    "max_output_tokens": max_tokens,
                    "top_k": top_k
                }
                model_instance = genai.GenerativeModel(model_name=model, generation_config=generation_config)
                question = f"Please generate 5 multiple-choice questions without answers based on the following text:\n\n{text}\n\nQuestions:"
                response = model_instance.generate_content([question, text])
                mcqs = response.text.strip().split('\n')
                mcqs = [mcq.strip() for mcq in mcqs if mcq.strip()]
                
                st.subheader("Generated MCQs:")
                for question in mcqs:
                    st.write(question)
            else:
                st.error("No text extracted from the PDF.")

if __name__ == "__main__":
    genai.configure(api_key = st.secrets["API_Key"])
    page_setup()
    if "logged_in" not in st.session_state:
        login_page()
    elif st.session_state.logged_in:
        home_page()
