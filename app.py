from dotenv import load_dotenv
load_dotenv() #loading all the environment variables.

import streamlit as st
import os
import google.generativeai as genai
import pathlib
import textwrap 
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
history=[[],[]]
model=genai.GenerativeModel("gemini-pro-vision")
#function to load and run Gemini Pro
def get_gemini_response(input,img):
    if input=='':
        response=model.generate_content(img)
    else:
        history[0].append(input)
        response=model.generate_content([input,img])
    return response.text

st.set_page_config(page_title='Gemini Image content')
st.header('Gemini Application')

input=st.text_input("Input Prompt: ",key="input")
uploaded_file= st.file_uploader("Upload an image:", type=['jpg', 'jpeg', 'png'])
image=''
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image, caption="uploaded Image", use_column_width=True)

submit=st.button('Press to generate content')
if submit:
    response=get_gemini_response(input,image)
    history[1].append(response)
    st.subheader('The response is:')
    st.write(response)

st.subheader('Chat history:')
for i in range(len(history[0])):
    st.write('prompt:',history[0][i])
    st.write('response:',history[1][i])
