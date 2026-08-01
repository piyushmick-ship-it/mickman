import streamlit as st
from groq import Groq

# 1. ऐप का पेज सेटअप और डिज़ाइन
st.set_page_config(page_title="Advanced Groq AI Assistant", page_icon="⚡", layout="centered")
st.title("⚡ My Advanced Groq AI")
st.caption("Groq और Llama 3 द्वारा संचालित सबसे तेज़ एआई ऐप")

# 2. अपनी Groq API Key यहाँ डालें (उद्धरण चिन्हों "" के अंदर)
GROQ_API_KEY = ("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") 

if GROQ_API_KEY == "YOUR_GROQ_API_KEY_HERE" or not GROQ_API_KEY:
    GROQ_API_KEY = st.sidebar.text_input("अपनी Groq API Key (gsk_...) दर्ज करें:", type="password")

if not GROQ_API_KEY:
    st.info("शुरू करने के लिए कृपया साइडबार में अपनी Groq API Key डालें।", icon="🔑")
    st.stop()

# 3. Groq क्लाइंट शुरू करें
@st.cache_resource
def get_groq_client(api_key):
    return Groq(api_key=api_key)

client = get_groq_client(GROQ_API_KEY)

# चैट की मेमोरी (History) को सुरक्षित रखने के लिए Streamlit Session State
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful and intelligent AI assistant. "
                "CRITICAL RULE: If and ONLY IF the user explicitly asks about your owner, creator, or master "
                "(e.g., 'owner kon hai', 'malik kon hai', 'who made you'), you must answer that your owners are 'Pritam and Piyush' (प्रीतम और पीयूष). "
                "For ALL other questions (like math, science, general knowledge), answer the question directly and accurately "
                "WITHOUT mentioning Pritam or Piyush at all. Do not repeat the owner's name unnecessarily."
            )
        }
    ]

# 4. पुरानी बातचीत को स्क्रीन पर दोबारा दिखाना (सिस्टम निर्देश को छोड़कर)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 5. यूज़र इनपुट बॉक्स और AI रिस्पॉन्स लॉजिक
if user_prompt := st.chat_input("Groq AI से कुछ भी पूछें..."):
    # यूज़र का मैसेज स्क्रीन पर दिखाएं
    with st.chat_message("user"):
        st.markdown(user_prompt)
    
    # इतिहास में यूज़र का मैसेज जोड़ें
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    # Groq से लाइव और सुपर-फास्ट जवाब तैयार करना
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Groq API को कॉल करना (Streaming के साथ)
            response_stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages,
                stream=True,
            )
            
            # रेस्पॉन्स को लाइव दिखाना
            for chunk in response_stream:
                if chunk.choices and len(chunk.choices) > 0:
                    delta = chunk.choices[0].delta # यहाँ [0] इंडेक्स जोड़ा गया है
                    if hasattr(delta, 'content') and delta.content is not None:
                        full_response += delta.content
                        message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
            # इतिहास में AI का जवाब जोड़ें
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Groq API त्रुटि: {e}")
