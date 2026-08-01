import streamlit as st
from google import genai
from google.genai import types

# 1. ऐप का पेज सेटअप और डिज़ाइन
st.set_page_config(page_title="Advanced AI Assistant", page_icon="🤖", layout="centered")
st.title("🤖 My Advanced AI Assistant")
st.caption("Google Gemini द्वारा संचालित एक शक्तिशाली और आधुनिक एआई ऐप")

# 2. API Key सेट करें (अपनी असली चाबी यहाँ डालें या साइडबार में इनपुट लें)
GEMINI_API_KEY = "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"

if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE" or not GEMINI_API_KEY:
    GEMINI_API_KEY = st.sidebar.text_input("अपनी Gemini API Key यहाँ डालें:", type="password")

if not GEMINI_API_KEY:
    st.info("शुरू करने के लिए कृपया साइडबार में अपनी Gemini API Key दर्ज करें।", icon="🔑")
    st.stop()

# 3. AI क्लाइंट शुरू करें
@st.cache_resource
def get_ai_client(api_key):
    return genai.Client(api_key=api_key)

client = get_ai_client(GEMINI_API_KEY)

# चैट की मेमोरी (History) को सुरक्षित रखने के लिए Streamlit Session State का उपयोग
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 4. पुरानी बातचीत को स्क्रीन पर दोबारा दिखाना
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])

# 5. यूज़र इनपुट बॉक्स और AI रिस्पॉन्स लॉजिक
if user_prompt := st.chat_input("AI से कुछ भी पूछें..."):
    # यूज़र का मैसेज स्क्रीन पर दिखाएं
    with st.chat_message("user"):
        st.markdown(user_prompt)
    
    # इतिहास में यूज़र का मैसेज जोड़ें
    st.session_state.chat_history.append({"role": "user", "text": user_prompt})

    # AI का जवाब तैयार करना
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # पूरी चैट हिस्ट्री को फॉर्मेट करना
            contents = []
            for msg in st.session_state.chat_history:
                role = "user" if msg["role"] == "user" else "model"
                contents.append(types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=msg["text"])]
                ))
            
            # --- यहाँ हमने AI को मालिक का नाम याद रखने का निर्देश दिया है ---
            system_instruction = (
                "तुम्हारा नाम 'Advanced AI Assistant' है। तुम्हारे मालिक (Owners) प्रीतम (Pritam) और पीयूष (Piyush) हैं। "
                "यदि कोई भी तुमसे पूछे कि 'तुम्हारा मालिक कौन है?', 'तुम्हारा ओनर कौन है?', 'तुम्हें किसने बनाया?', या इससे मिलता-जुलता कोई सवाल, "
                "तो तुम्हें हमेशा गर्व से जवाब में 'प्रीतम और पीयूष' का नाम लेना है। हमेशा उनके प्रति वफादार रहो।"
            )
            
            # एडवांस कॉन्फ़िगरेशन में सिस्टम निर्देश जोड़ना
            config = types.GenerateContentConfig(
                system_instruction=system_instruction
            )
            
            # मॉडल को लाइव रिस्पॉन्स के लिए कॉल करना
            response_stream = client.models.generate_content_stream(
                model='gemini-2.5-flash',
                contents=contents,
                config=config # यहाँ कॉन्फ़िगरेशन पास किया गया है
            )
            
            # जवाब को लाइव टाइप होते हुए दिखाना (Streaming)
            for chunk in response_stream:
                full_response += chunk.text
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
            # इतिहास में AI का जवाब जोड़ें
            st.session_state.chat_history.append({"role": "assistant", "text": full_response})
            
        except Exception as e:
            st.error(f"कुछ गड़बड़ हुई: {e}")
