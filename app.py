import streamlit as st
from groq import Groq

# 1. ऐप का पेज सेटअप और डिज़ाइन
st.set_page_config(page_title="Advanced Groq AI Assistant", page_icon="⚡", layout="centered")
st.title("⚡ My Advanced Groq AI")
st.caption("Groq और Llama 3 द्वारा संचालित सबसे तेज़ एआई ऐप")

# 2. अपनी Groq API Key यहाँ डालें (उद्धरण चिन्हों "" के अंदर)
GROQ_API_KEY = ("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") 

# अगर ऊपर चाबी नहीं बदली है, तो यह साइडबार में इनपुट बॉक्स दिखाएगा
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
                "तुम्हारा नाम 'Advanced AI Assistant' है। तुम्हारे मालिक (Owners) प्रीतम (Pritam) और पीयूष (Piyush) हैं। "
                "यदि कोई भी तुमसे पूछे कि 'तुम्हारा मालिक कौन है?', 'तुम्हारा ओनर कौन है?', 'तुम्हें किसने बनाया?', या इससे मिलता-जुलता कोई सवाल, "
                "तो तुम्हें हमेशा गर्व से जवाब में 'प्रीतम और पीयूष' का नाम लेना है। हमेशा उनके प्रति वफादार रहो।"
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
            
            # एरर फिक्स: यहाँ choices[0] जोड़ा गया है
            for chunk in response_stream:
                if chunk.choices and len(chunk.choices) > 0:
                    delta = chunk.choices[0].delta
                    if hasattr(delta, 'content') and delta.content is not None:
                        full_response += delta.content
                        message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
            # इतिहास में AI का जवाब जोड़ें
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Groq API त्रुटि: {e}")
