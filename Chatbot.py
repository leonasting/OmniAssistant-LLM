import streamlit as st
import os
import pathlib
import textwrap
from IPython.display import display
from IPython.display import Markdown

import google.generativeai as genai
st.set_page_config(page_title="Q&A Demo")



def get_gemini_response(question):
    
    response =chat.send_message(question,stream=True)
    return response

with st.sidebar:
    google_api_key = st.text_input("Generative API Key", key="google_api_key", type="password")
    "[Get an Generative AI API key](https://makersuite.google.com/app/apikey)"
    "[View the source code]()"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("💬 Chatbot")
st.caption("🚀 A streamlit chatbot powered by Google Generative LLM")


st.header("Gemini LLM Application")
# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []


if prompt := st.chat_input():
    if not google_api_key:
        st.info("Please add your Generative AI API key to continue.")
        st.stop()
    else:
        genai.configure(api_key=google_api_key)
        ## Function to load OpenAI model and get respones
        model = genai.GenerativeModel('gemini-pro')
        chat = model.start_chat(history=[])

        response=get_gemini_response(prompt)
        # Add user query and response to session state chat history
        st.session_state['chat_history'].append(("You", prompt))
        st.subheader("The Response is")
        res=[]
        for chunk in response:
            st.write(chunk.text)
            res.append(chunk.text)
        
        st.session_state['chat_history'].append(("Bot", res))
        

    st.subheader("The Chat History is")
    
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")
    

