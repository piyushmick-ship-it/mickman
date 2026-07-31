import streamlit as st
from groq import Groq

st.title("My World AI")
st.write("नया AI असिस्टेंट 🌐")

# सीधे स्क्रीन पर API Key डालने का सुरक्षित बॉक्स
user_key = st.sidebar.text_input("अपनी Groq API Key यहाँ डालें:", type="password")

if not user_key:
    st.info("कृपया आगे बढ़ने के लिए बाएँ (Left) पैनल में अपनी Groq API Key डालें।")
    st.stop()

# यूजर द्वारा डाली गई की से क्लाइंट शुरू करें
client = Groq(api_key=user_key)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

if prompt := st.chat_input("मुझसे कुछ भी पूछें..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
        
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=st.session_state.messages
        )
        answer = response.choices.message.content
        st.session_state.messages.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.write(answer)
    except Exception as e:
        st.error(f"एक गड़बड़ हुई: {e}")
