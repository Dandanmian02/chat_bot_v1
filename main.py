
import streamlit as st

import openai

import time

import os

st.set_page_config(page_title="AI CHatbot", page_icon="=)", layout="wide")
st.image('file:///C:/Users/This%20PC/Desktop/Character_Venti_Full_Wish.webp')
ASSISTANT_ID="asst_A95bhvZds5YyTWYFxnhBR1ox"
THREAD_ID='thread_xlA2Lljk2KldAe9tEtauCbf2'

api_key = st.secrets.get("OPEN_API_KEY")
client = openai = openai.OpenAI(api_key=api_key)

st.title('AI Chatbot')
if "messages" not in st.session_state:
    st.session_state.messages = []

def get_assistant_response(assistant_id, thread_id, user_input):
    try:
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_input
        )
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id
        )
        while True:
            run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
            if run_status.status == 'completed':
                break
            time.sleep(1)
        messages = client.beta.threads.messages.list(thread_id=thread_id)

        return messages.data[0].content[0].text.value
    except Exception as e:
        st.error(f"Error getting assistaent reponse: {str(e)}")
        return "I'm sorry, but an error occurred while processing your request."

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask me anything!")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = get_assistant_response(
            ASSISTANT_ID,
            THREAD_ID,
            prompt
        )
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
                     
                                                           
