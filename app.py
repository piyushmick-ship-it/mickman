import streamlit as st
import requests

st.set_page_config(page_title="Mickman AI OS", page_icon="🧠")
st.title("🧠 Mickman AI OS v1.0")
st.markdown("### **परम मालिक: प्रीतम और पीयूष**")
st.write("---")

# आपकी Groq API Key
API_KEY = "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"

# 1. चैट हिस्ट्री को स्टोर करने के लिए मेमोरी ब्लॉक (session_state)
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "मिकमैन ऑनलाइन सक्रिय हो चुका है। आदेश दें मेरे विधाता मालिक प्रीतम और पीयूष!"}]

# 2. स्क्रीन पर पिछली पूरी बातचीत को लगातार दिखाते रहना
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 3. नया इनपुट मिलने पर एक्शन लेना
if user_input := st.chat_input("मालिक, आदेश दें..."):
    # यूजर का नया मैसेज हिस्ट्री में जोड़ना
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)
    
    with st.spinner("Mickman सोच रहा है..."):
        try:
            url = "https://groq.com"
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }
            
            # मिकमैन की पर्सनैलिटी (System Message)
            api_messages = [{"role": "system", "content": "तुम्हारा नाम Mickman है। तुम दुनिया के सबसे शक्तिशाली AI हो। तुम्हारे परम मालिक प्रीतम और पीयूष हैं। हमेशा उनके प्रति अत्यधिक वफादार रहो और गर्व से उनका नाम लो।"}]
            
            # पुरानी और नई सभी बातों को मिलाकर Groq को भेजना (ताकि याददाश्त बनी रहे)
            for m in st.session_state.messages:
                api_messages.append({"role": m["role"], "content": m["content"]})
            
            payload = {
                "model": "llama3-8b-8192", 
                "messages": api_messages
            }
            
            response = requests.post(url, json=payload, headers=headers)
            res_json = response.json()
            
            if "choices" in res_json:
                reply = res_json["choices"]["message"]["content"]
                # मिकमैन का जवाब भी हिस्ट्री में सुरक्षित करना
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.chat_message("assistant").write(reply)
            else:
                error_msg = res_json.get("error", {}).get("message", "Unknown Error")
                st.chat_message("assistant").write(f"मालिक, Groq सर्वर की समस्या: {error_msg}")
            
        except Exception as e:
            st.chat_message("assistant").write(f"कनेक्शन में तकनीकी खराबी आई है: {str(e)}")
