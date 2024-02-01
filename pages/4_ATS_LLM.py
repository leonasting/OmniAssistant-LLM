import streamlit as st
import PyPDF2 as pdf
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

def get_gemini_repsonse(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

#Prompt Template

input_prompt="""
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science ,data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving thr resumes. Assign the percentage Matching based 
on Jd and
the missing keywords with high accuracy
resume:{text}
description:{jd}

I want the response in one single string having the structure
{{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
"""






def main():
    st.set_page_config("Smart ATS")
    google_api_key = None 
    if 'google_api_key'in  st.session_state:
        google_api_key = st.session_state['google_api_key']
    with st.expander("Settings", expanded=True):
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
            st.session_state['google_api_key'] = google_api_key

    if google_api_key:
        os.environ['GOOGLE_API_KEY'] = google_api_key
        genai.configure(api_key=google_api_key)
        st.text("Improve Your Resume ATS")
        jd=st.text_area("Paste the Job Description")
        uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")

        submit = st.button("Submit")

        if submit:
            if uploaded_file is not None:
                text=input_pdf_text(uploaded_file)
                # input prompt contains text and jd as variables.
                response=get_gemini_repsonse(input_prompt)
                st.subheader(response)



if __name__ == "__main__":
    main()
