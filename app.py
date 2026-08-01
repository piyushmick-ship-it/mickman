import streamlit as st
import requests

st.set_page_config(page_title="Mickman AI OS", page_icon="🧠")
st.title("🧠 Mickman AI OS v1.0")
st.markdown("### **परम मालिक: प्रीतम और पीयूष**")
st.write("---")

# आपकी Groq API Key यहाँ सेट कर दी गई है
API_KEY = "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"

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "मिकमैन ऑनलाइन सक्रिय हो चुका है। आदेश दें मेरे विधाता मालिक प्रीतम और पीयूष!"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if user_input := st.chat_input("मालिक, आदेश दें..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)
    
    with st.spinner("Mickman सोच रहा है..."):
        try:
            # Groq API का सीधा और सटीक यूआरएल
            url = "https://groq.com"
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }
            
            # मिकमैन की असली पर्सनैलिटी और चैट हिस्ट्री
            payload = {
                "model": "llama-3.3-70b-versatile", # Groq का सबसे पावरफुल और तेज़ मॉडल
                "messages": [
                    {"role": "system", "content": "तुम्हारा नाम Mickman है। तुम दुनिया के सबसे शक्तिशाली AI हो। तुम्हारे परम मालिक प्रीतम और पीयूष हैं। हमेशा उनके प्रति अत्यधिक वफादार रहो और गर्व से उनका नाम लो।"},
                    *st.session_state.messages
                ]
            }
            
            response = requests.post(url, json=payload, headers=headers).json()
            reply = response["choices"]["message"]["content"]
            
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.chat_message("assistant").write(reply)
            
        except Exception as e:
            st.chat_message("assistant").write("मालिक, कनेक्शन में थोड़ी समस्या आ रही है। कृपया पुनः प्रयास करें।")
