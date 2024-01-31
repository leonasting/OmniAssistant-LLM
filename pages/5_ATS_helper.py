import streamlit as st
import PyPDF2 as pdf
import pdf2image
import io
import base64
from PIL import Image
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import json
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

#st.set_page_config(page_title="PDF explaination app")
def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ## Convert the PDF to image
        images=pdf2image.convert_from_bytes(uploaded_file.read())

        first_page=images[0]

        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")






def main():
    st.set_page_config("ATS Resume EXpert")
    google_api_key = None
    with st.sidebar:
        if not google_api_key:
            "Please Update the API Key to use the app"
            google_api_key = st.text_input("Generative API Key", key="google_api_key", type="password")
            "[Get an Generative AI API key](https://makersuite.google.com/app/apikey)"
            "[View the source code]()"
            "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"
            
        if not google_api_key:
            st.info("Please add your Generative AI API key to continue.")
        
            st.stop()
        else:
            genai.configure(api_key=google_api_key)

    if google_api_key:
        os.environ['GOOGLE_API_KEY'] = google_api_key
        genai.configure(api_key=google_api_key)
        st.header("ATS Tracking System")
        input_text=st.text_area("Job Description: ",key="input")
        uploaded_file=st.file_uploader("Upload your resume(PDF)...",type=["pdf"])


        if uploaded_file is not None:
            st.write("PDF Uploaded Successfully")


        submit1 = st.button("Tell Me About the Resume")

        #submit2 = st.button("How Can I Improvise my Skills")

        submit3 = st.button("Percentage match")

        input_prompt1 = """
        You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
        Please share your professional evaluation on whether the candidate's profile aligns with the role. 
        Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
        """

        input_prompt3 = """
        You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
        your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
        the job description. First the output should come as percentage and then keywords missing and last final thoughts.
        """

        if submit1:
            if uploaded_file is not None:
                pdf_content=input_pdf_setup(uploaded_file)
                response=get_gemini_response(input_prompt1,pdf_content,input_text)
                st.subheader("The Repsonse is")
                st.write(response)
            else:
                st.write("Please uplaod the resume")

        elif submit3:
            if uploaded_file is not None:
                pdf_content=input_pdf_setup(uploaded_file)
                response=get_gemini_response(input_prompt3,pdf_content,input_text)
                st.subheader("The Repsonse is")
                st.write(response)
            else:
                st.write("Please uplaod the resume")



if __name__ == "__main__":
    main()
