import streamlit as st
from groq import Groq
import os

# 1. Page Configuration और Title सेट करें
st.set_page_config(page_title="My World AI Pro", page_icon="🚀", layout="wide")

# 2. एडवांस साइडबार सेटिंग्स
with st.sidebar:
    st.title("⚙️ AI सेटिंग्स")
    # API Key को सुरक्षित रखने के लिए छुपा हुआ इनपुट बॉक्स
    api_key = st.text_input("Groq API Key डालें", value="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", type="password")
    
    # एडवांस मॉडल चुनने का विकल्प
    model_choice = st.selectbox(
        "AI मॉडल चुनें:",
        ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"]
    )
    
    st.markdown("---")
    # चैट इतिहास साफ़ करने का बटन
    if st.button("🗑️ बातचीत साफ़ करें (Clear Chat)"):
        st.session_state.messages = [
            {"role": "system", "content": "तुम्हारा मालिक Pritam and Piyush है। तुम एक एडवांस और मददगार AI असिस्टेंट हो।"}
        ]
        st.rerun()

st.title("दुनिया का नया एडवांस AI असिस्टेंट 🌐")
st.caption("अब आप इसमें फाइल अपलोड करके भी सवाल पूछ सकते हैं!")

# Groq Client शुरू करें
if not api_key:
    st.warning("कृपया साइडबार में अपनी Groq API Key डालें।")
    st.stop()
client = Groq(api_key=api_key)

# 3. चैट हिस्ट्री को सिस्टम निर्देश के साथ शुरू करें
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "तुम्हारा मालिक Pritam and Piyush है। तुम एक एडवांस और मददगार AI असिस्टेंट हो।"}
    ]

# 4. पुरानी बातचीत को स्क्रीन पर दिखाएं
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# 5. एडवांस फ़ाइल अपलोडर (PDF और Images के लिए)
uploaded_file = st.file_uploader("अपनी PDF या इमेज फ़ाइल यहाँ अपलोड करें:", type=["pdf", "png", "jpg", "jpeg"])
file_context = ""

if uploaded_file is not None:
    st.success(f"फ़ाइल सफलतापुर्वक लोड हुई: {uploaded_file.name}")
    # यहाँ हम AI को बताएंगे कि यूज़र ने एक फ़ाइल अटैच की है
    file_context = f"\n\n[यूज़र ने '{uploaded_file.name}' नाम की फ़ाइल सबमिट की है। इस फ़ाइल के संदर्भ में बातचीत करें।]"

# 6. यूज़र से इनपुट लें
if prompt := st.chat_input("मुझसे कुछ भी पूछें..."):
    # अगर फ़ाइल अपलोड है तो उसे प्रॉम्प्ट के साथ जोड़ें
    full_prompt = prompt + file_context if file_context else prompt
    
    # यूज़र का मैसेज स्क्रीन पर दिखाएं
    with st.chat_message("user"):
        st.write(prompt)
        
    # यूज़र का मैसेज लिस्ट में जोड़ें
    st.session_state.messages.append({"role": "user", "content": full_prompt})
    
    try:
        # Groq API से जवाब लें
        response = client.chat.completions.create(
            model=model_choice,
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        )
        
        ans = response.choices[0].message.content
        
        # AI का जवाब लिस्ट में जोड़ें
        st.session_state.messages.append({"role": "assistant", "content": ans})
        
        # AI का जवाब स्क्रीन पर दिखाएं
        with st.chat_message("assistant"):
            st.write(ans)
            
    except Exception as e:
        with st.chat_message("assistant"):
            st.error(f"एरर आया: {e}")
