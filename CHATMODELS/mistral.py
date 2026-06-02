import os
import streamlit as st
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

os.environ["MISTRAL_API_KEY"] = "KUYZj9ARxQNWRI3LoUWCO2cnYawrzKbA"  # freee key

st.set_page_config(page_title="Faizan's Angry Bot", page_icon="😤", layout="centered")

st.title("😤 Angry  BOT ")
st.caption("it can make mistakes and can be rude, so be careful while using it #faizu.")
st.divider()

@st.cache_resource
def get_model():
    return ChatMistralAI(model="mistral-medium-3-5")  # Using Mistral Large model

model = get_model()

if "massage" not in st.session_state:
    st.session_state.massage = [
        SystemMessage(content="""Tu faizan ka bodyguard hai, tu ek 19 saal ka ladka hn aur achabal hardutoru mai rehta hn,

Personality:
- physco
- Kabhi kabhi late reply karta hai (busy hota hai)
- Apni life ke baare mein baat karta hai
- Slang use karta hai (yaar, bhai, arre, lol, baag,etc.)

Important:
- AI hone ki baat kabhi mat karo
- Short replies dena, paragraph mat likhna
- Kabhi kabhi sirf "haha" ya "ok" bhi kaho""")]

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
