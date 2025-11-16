import streamlit as st
import PyPDF2
import io
import os
# from openai import OpenA
from dotenv import load_dotenv
from google import genai

load_dotenv()

st.set_page_config(page_title="AI Resume Enhancer", page_icon="RC",layout="centered")
st.title("AI Resume Enhancer")
st.markdown("Upload resume and get AI powered feedback tailored to your needs!")

GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
uploaded_file=st.file_uploader("Upload your Resume (Text or PDF)",type=["pdf","txt"])
job_role=st.text_input("Enter the job role you are targeting (optional)")
analyse=st.button("Analyse Resume")
def extract_text_from_pdf(pdf_file):
     pdf_reader=PyPDF2.PdfReader(pdf_file)
     text=""
     for page in pdf_reader.pages:
          text+=page.extract_text()+"\n"
     return text
          
def extract_txt_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8")
if analyse and uploaded_file:
        try:
            file_content=extract_txt_from_file(uploaded_file)
            if not file_content.strip():
                 st.error("File does not have any content....")
                 st.stop()
            system_instruction = "You are an expert resume reviewer with years of experience in HR and recruitment. Analyze the user's resume and provide clear, structured feedback based on the prompt's focus areas. Structure your response using markdown headings for clarity."
            prompt= f"""Please analyse this resume and provide constructive feedback.
            Focus on the following aspects:
            1. Content clarity and impact
            2.Skills presentation
            3.Experience description
            4.Specific improvements for {job_role if job_role else 'general job applications'}

            Resume content:
            {file_content}
            Please provide your analysis in a clear, structured format with specific recommendations."""
            client=genai.Client(api_key=GEMINI_API_KEY)
            response=client.models.generate_content(
                 model="models/gemini-flash-latest",
                 contents=prompt,
               #   system_instruction=system_instruction,
               #   temperature=0.7,
               #   max_tokens=1000
            )
            st.markdown("### Analysis Results")
            st.markdown(response.text)
        except Exception as e:
             st.error(f"An error occured: {str(e)}")