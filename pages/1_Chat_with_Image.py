import streamlit as st
import os
import pathlib
import textwrap
from IPython.display import display
from IPython.display import Markdown
from PIL import Image


import google.generativeai as genai
#st.set_page_config(page_title="Gemini Image Demo")



def get_gemini_response(input,image):
    model = genai.GenerativeModel('gemini-pro-vision')
    if input!="":
       response = model.generate_content([input,image])
    else:
       response = model.generate_content(image)
    return response.text
def main():
    st.set_page_config(page_title="Gemini Image Demo")
    #print("wow")
    google_api_key = None
    if 'google_api_key'in  st.session_state:
        google_api_key = st.session_state['google_api_key']
    with st.expander("Settings", expanded=True):
        if not google_api_key:
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
        st.title("💬 Chatbot with image input")
        st.caption("🚀 A streamlit chatbot powered by Google Generative LLM")


        st.header("Chat with Image input and optional prompt")
        # Initialize session state for chat history if it doesn't exist
        if 'chat_history' not in st.session_state:
            st.session_state['chat_history'] = []


        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
        image=""
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image.", use_column_width=True)   
        submit=st.button("Tell me about the image")
        if submit:
            
            if uploaded_file is None:
                st.info("Please add upload image to continue conversation.")
                st.stop()
            genai.configure(api_key=google_api_key)
            model = genai.GenerativeModel('gemini-pro-vision')
            response=get_gemini_response("",image)
            st.subheader("The Response is")
            st.write(response)
            st.session_state['chat_history'].append(("Bot", response))

        if prompt := st.chat_input():

            genai.configure(api_key=google_api_key)
            ## Function to load OpenAI model and get respones
            model = genai.GenerativeModel('gemini-pro-vision')
            chat = model.start_chat(history=[])
            
            if uploaded_file is None:
                st.info("Please add upload image to continue conversation.")
                st.stop()

            response=get_gemini_response(prompt,image)
            # Add user query and response to session state chat history
            
            st.session_state['chat_history'].append(("You", prompt))
            st.subheader("The Response is")
            st.write(response)
            # res=[]
            # for chunk in response:
            #     st.write(chunk.text)
            #     res.append(chunk.text)
            
            st.session_state['chat_history'].append(("Bot", response))
        with st.sidebar:
            with st.expander("history", expanded=False):        
                if st.session_state['chat_history']:
                    "The Chat History is"
                    
                    for role, text in st.session_state['chat_history']:
                        st.write(f"{role}: {text}")
if __name__ == "__main__":
    main()    

