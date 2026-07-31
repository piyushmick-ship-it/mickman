import streamlit as st
from groq import Groq

st.set_page_config(page_title="My World AI", page_icon="🤖")
st.title("दुनिया का नया AI असिस्टेंट 🌐")

# अपनी कॉपी की हुई Groq API Key यहाँ डालें
client = Groq(api_key="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


if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("मुझसे कुछ भी पूछें..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=st.session_state.messages
    )
    ans = response.choices.message.content
    st.session_state.messages.append({"role": "assistant", "content": ans})
    with st.chat_message("assistant"):
        st.write(ans)
