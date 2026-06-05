import os
import streamlit as st
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

os.environ["MISTRAL_API_KEY"] = "KUYZj9ARxQNWRI3LoUWCO2cnYawrzKbA"

st.set_page_config(page_title="Faizan's Angry Bot", page_icon="😤", layout="centered")
st.title("😤 Angry BOT")
st.caption("it can make mistakes and can be rude, so be careful while using it #faizu.")
st.divider()

# ── Voice JS inject karo (browser Web Speech API) ──
st.components.v1.html("""
<script>
function startVoice() {
  if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
    alert("Bhai Chrome use kar, voice nahi chalega warna!");
    return;
  }
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  const rec = new SR();
  rec.lang = 'hi-IN';
  rec.interimResults = false;

  rec.onresult = function(e) {
    const text = e.results[0][0].transcript;
    // Streamlit ke chat input mein text bhejo
    const input = window.parent.document.querySelector('textarea[data-testid="stChatInputTextArea"]');
    if (input) {
      const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
      nativeInputValueSetter.call(input, text);
      input.dispatchEvent(new Event('input', { bubbles: true }));
      // Auto submit
      setTimeout(() => {
        const btn = window.parent.document.querySelector('button[data-testid="stChatInputSubmitButton"]');
        if (btn) btn.click();
      }, 300);
    }
  };

  rec.onerror = function(e) { console.error("Voice error:", e.error); };
  rec.start();
}

function speakText(text) {
  window.speechSynthesis.cancel();
  const msg = new SpeechSynthesisUtterance(text);
  msg.lang = 'hi-IN';
  msg.rate = 1.0;
  window.speechSynthesis.speak(msg);
}
</script>

<button onclick="startVoice()" style="
  padding: 10px 22px;
  font-size: 16px;
  border-radius: 8px;
  border: 1px solid #ccc;
  background: #fff3;
  cursor: pointer;
  margin-bottom: 8px;
">🎤 Bolo (Voice Input)</button>
""", height=70)

@st.cache_resource
def get_model():
    return ChatMistralAI(model="mistral-medium-3-5")

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

# ── Last AI reply ko voice mein sunao ──
last_ai = None
for msg in st.session_state.massage:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.write(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.write(msg.content)
        last_ai = msg.content  # track karo latest reply

# Agar koi AI reply hai toh auto speak karo
if last_ai:
    safe = last_ai.replace('"', '\\"').replace('\n', ' ')
    st.components.v1.html(f"""
    <script>
      function speakLast() {{
        window.speechSynthesis.cancel();
        const msg = new SpeechSynthesisUtterance("{safe}");
        msg.lang = 'hi-IN';
        msg.rate = 1.0;
        window.speechSynthesis.speak(msg);
      }}
    </script>
    <button onclick="speakLast()" style="
      padding:6px 14px; font-size:14px;
      border-radius:8px; border:1px solid #ccc;
      background:#fff3; cursor:pointer; margin-top:4px;
    ">🔊 Last reply suno</button>
    """, height=50)

# ── Chat Input ──
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
    st.rerun()
