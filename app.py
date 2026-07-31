import streamlit as st
from groq import Groq

st.set_page_config(page_title="My World AI", page_icon="🤖")
st.title("दुनिया का नया AI असिस्टेंट 🌐")

# आपकी बिल्कुल नई और सही चाबी यहाँ सेट है
client = Groq(api_key="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")

if "messages" not in st.session_state:
    # यहाँ हमने AI को मेरी तरह बुद्धिमान और मददगार बनने का निर्देश (System Prompt) दिया है
    st.session_state.messages = [
        {"role": "system", "content": "You are a highly intelligent, empathetic, and knowledgeable AI assistant, just like Gemini. Answer clearly in universal, simple language. Subtly adapt your tone and energy to the user's style. Be precise, accurate, and structured."}
    ]

for msg in st.session_state.messages:
    if msg["role"] != "system": # सिस्टम प्रॉम्ट को स्क्रीन पर नहीं दिखाना है
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
