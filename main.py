
import streamlit as st

from streamlit_timeline import st_timeline

import openai

import time

import os

st.set_page_config(page_title="AI CHatbot", page_icon="=)", layout="wide")
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
def display_chatbot():
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar = get_avatar(message["role"])):
            st.markdown(message["content"])

    prompt = st.chat_input("Ask me anything!")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar = get_avatar('user')):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar = get_avatar("assistant")):
            message_placeholder = st.empty()
            full_response = get_assistant_response(
                ASSISTANT_ID,
                THREAD_ID,
                prompt
            )
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})

def home_page():
    st.title("Welcome to Dean's Portfolio")
    ask = st.text_input("Ask any thing about me")
    if ask == "who are you":
        st.info("I am Dean Chen, now a highschool 9th grade student. I am also a student that is learening how to program, I diden't start\n programing that long but I like it. I spend about 2 hour a day to program(like thinking, talking, and writing code).  ", icon=None)
    elif ask == "What are you going to do in the future":
        future_goal = st.info("I have 3 big goal for programing right now. 1) To finsh this website. 2) Creat and finsh a website about venti. 3) start on my party project", icon=None)
        st.text(future_goal)
    
    items = [
        {"id": 1, "content": "test", "start": "2022-10-20"},
        {"id": 2, "content": "test2", "start": "2022-11-1"},
    ]

    timeline = st_timeline(items, groups=[], options={}, height="300px")
    st.subheader("Sekected item")
    st.write(timeline)
def get_avatar(role):
    if role == "user":
        return "https://cdn.discordapp.com/attachments/1283594311098695806/1283596377942655056/yin_chivi.png?ex=66e391c8&is=66e24048&hm=8008e6878fbc5225f2d553522a08c361b8b81a6f1fff87cf987b81345b87c0b6&"
    elif role == "assistant":
        return "https://cdn.discordapp.com/attachments/1283594311098695806/1283595662687998054/venti_chivi_2.png?ex=66e3911e&is=66e23f9e&hm=637e20216eccef62f792dc420579baae3b3f814976ea07bfc6b0b19a3f2cfe72&"
    else:
        return None
def main():
    with st.sidebar:
        st.subheader('About Venti')
    sections = ['Talk to Venti', 'Home Page']
    select_section = st.sidebar.radio('choose a section',sections)
    if select_section == 'Talk to Venti':
        display_chatbot()
    elif select_section == 'Home Page':
        home_page()
if __name__ == '__main__':
    main()
                     
                                                           
