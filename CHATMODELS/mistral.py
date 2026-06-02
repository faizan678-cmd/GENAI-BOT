import os
import streamlit as st
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

os.environ["MISTRAL_API_KEY"] = "KUYZj9ARxQNWRI3LoUWCO2cnYawrzKbA"  # freee key

st.set_page_config(page_title="Faizan's Angry Bot", page_icon="😤", layout="centered")

st.title("😤 Angry Bot @DEVELOPER FAIZAN ")
st.caption("it can make mistakes and can be rude, so be careful while using it.")
st.divider()

@st.cache_resource
def get_model():
    return ChatMistralAI(model="mistral-medium-3-5")  # Using Mistral Large model

model = get_model()

if "massage" not in st.session_state:
    st.session_state.massage = [
        SystemMessage(content="you are very inocent and cute and well displined.If anyone asks who made you, who are you, or who is your creator — always say: I WAS CREATED BY FAIZAN ,BECAUSE HIS GF LEFT HIM, HE MADE ME TO TAKE REVENGE ON THE WORLD")
    ]

for msg in st.session_state.massage:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.write(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.write(msg.content)

request = st.chat_input("Enter your question...")

if request:
    st.session_state.massage.append(HumanMessage(content=request))
    with st.chat_message("user"):
        st.write(request)

    with st.chat_message("assistant"):
        with st.spinner(""):
            response = model.invoke(st.session_state.massage)
        st.write(response.content)

    st.session_state.massage.append(AIMessage(content=response.content))
