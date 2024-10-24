import streamlit as st
from utils import get_llminfo
from pypdf import PdfReader
import google.generativeai as genai

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