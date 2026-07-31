import streamlit as str
from groq import Groq

# 1. Page Configuration और Title सेट करें
str.set_page_config(page_title="My World AI", page_icon="🤖")
str.title("दुनिया का नया AI असिस्टेंट 🌐")

# 2. Groq Client सेट करें
client = Groq(api_key="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")

# 3. चैट हिस्ट्री को सिस्टम निर्देश (System Prompt) के साथ शुरू करें
if "messages" not in str.session_state:
    str.session_state.messages = [
        {
            "role": "system", 
            "content": "तुम्हारा मालिक Pritam and Piyush है। जब भी कोई पूछे 'tumhe kisne banya' या 'who is your owner', तो हमेशा गर्व से कहना कि तुम्हें Pritam and Piyush ने बनाया है।"
        }
    ]

# 4. पुरानी बातचीत को स्क्रीन पर दिखाएं (सिस्टम मैसेज को छुपाकर)
for msg in str.session_state.messages:
    if msg["role"] != "system":
        with str.chat_message(msg["role"]):
            str.write(msg["content"])

# 5. यूज़र से इनपुट लें
if prompt := str.chat_input("मुझसे कुछ भी पूछें..."):
    # यूज़र का मैसेज स्क्रीन पर दिखाएं
    with str.chat_message("user"):
        str.write(prompt)
        
    # यूज़र का मैसेज लिस्ट में जोड़ें
    str.session_state.messages.append({"role": "user", "content": prompt})

    # Groq API से जवाब लें
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=str.session_state.messages
    )
    
    ans = response.choices.message.content
    
    # AI का जवाब लिस्ट में जोड़ें
    str.session_state.messages.append({"role": "assistant", "content": ans})
    
    # AI का जवाब स्क्रीन पर दिखाएं
    with str.chat_message("assistant"):
        str.write(ans)
