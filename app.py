import os
import cv2
import pyttsx3
import base64
import time
import requests
import psutil
import datetime
import speech_recognition as sr
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.utilities import SerpAPIWrapper, PythonREPLUtility
from langchain_core.tools import Tool

# =====================================================================
# 1. कॉन्फ़िगरेशन और API Keys (import os
import cv2
import pyttsx3
import base64
import time
import requests
import psutil
import datetime
import speech_recognition as sr
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_community.utilities import SerpAPIWrapper, PythonREPLUtility
from langchain_core.tools import Tool

# =====================================================================
# 1. कॉन्फ़िगरेशन और API Keys ("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")
# =====================================================================
os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"
os.environ["SERPAPI_API_KEY"] = "YOUR_GOOGLE_SEARCH_API_KEY"

# कोर इंजन सेटअप
llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
engine = pyttsx3.init()
recognizer = sr.Recognizer()

# =====================================================================
# 2. मिकमैन के मूल फंक्शन्स (बोलना, सुनना, देखना)
# =====================================================================
def speak(text):
    """मिकमैन को आवाज देने के लिए (स्पीकर टूल)"""
    print(f"\nMickman: {text}")
    engine.say(text)
    engine.runAndWait()

def listen_microphone():
    """माइक से मालिकों की आवाज सुनने के लिए"""
    with sr.Microphone() as source:
        print("\n[Mickman सुन रहा है... आदेश दें]")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            query = recognizer.recognize_google(audio, language='hi-IN')
            print(f"आपने कहा: {query}")
            return query
        except sr.WaitTimeoutError:
            return "TIMEOUT"
        except Exception:
            return "ERROR"

def capture_and_analyze(query="सामने क्या है विस्तार से देखो"):
    """कैमरा चालू करके सामने की दुनिया को देखने के लिए (कैमरा विज़न)"""
    cap = cv2.cv2.VideoCapture(0) if hasattr(cv2, 'cv2') else cv2.VideoCapture(0)
    if not cap.isOpened():
        return "त्रुटि: कैमरा कनेक्टेड नहीं है या अनुमति नहीं है।"
    
    time.sleep(1) # कैमरे को एडजस्ट होने का समय दें
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        return "त्रुटि: तस्वीर खींचने में असमर्थ।"
        
    image_path = "mickman_live_view.jpg"
    cv2.imwrite(image_path, frame)
    
    with open(image_path, "rb") as img_file:
        base64_image = base64.b64encode(img_file.read()).decode('utf-8')
        
    vision_llm = ChatOpenAI(model="gpt-4o")
    from langchain_core.messages import HumanMessage
    
    message = HumanMessage(
        content=[
            {"type": "text", "text": f"तुम मिकमैन हो। मालिक प्रीतम और पीयूष के लिए इस लाइव दृश्य का विश्लेषण करो: {query}"},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
        ]
    )
    response = vision_llm.invoke([message])
    return response.content

# =====================================================================
# 3. एडवांस सिस्टम और यूटिलिटी टूल्स
# =====================================================================
def save_note(text_content):
    """मालिकों के लिए महत्वपूर्ण नोट्स या फाइल सुरक्षित करने के लिए"""
    filename = f"mickman_note_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text_content)
    return f"नोट को सफलतापूर्वक '{filename}' नाम से सुरक्षित कर दिया गया है।"

def get_system_status():
    """कंप्यूटर की सेहत (CPU, RAM, Battery) चेक करने के लिए"""
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    battery = psutil.sensors_battery()
    bat_str = f"{battery.percent}%" if battery else "उपलब्ध नहीं"
    return f"वर्तमान सिस्टम स्थिति -> CPU उपयोग: {cpu}%, RAM उपयोग: {ram}%, बैटरी: {bat_str}।"

# टूल्स का एकत्रीकरण
search = SerpAPIWrapper()
python_repl = PythonREPLUtility()

tools = [
    Tool(name="google_search", func=search.run, 
         description="इंटरनेट से आज की ताज़ा खबरें, लाइव स्कोर, मौसम या कोई भी नई जानकारी ढूंढने के लिए।"),
    Tool(name="python_interpreter", func=python_repl.run, 
         description="जटिल गणितीय गणना, लॉजिक, डेटा प्रोसेसिंग या कोडिंग के काम बैकएंड में हल करने के लिए।"),
    Tool(name="camera_vision", func=capture_and_analyze, 
         description="जब यूजर देखने, पहचानने या सामने की स्थिति जानने को कहे तब वेबकैम की मदद से देखने के लिए।"),
    Tool(name="file_manager_save_note", func=save_note, 
         description="मालिकों की किसी बात, कोड या महत्वपूर्ण जानकारी को टेक्स्ट फाइल में सेव करने के लिए।"),
    Tool(name="system_monitor", func=get_system_status, 
         description="कंप्यूटर की परफॉर्मेंस, सीपीयू और रैम की स्थिति जांचने के लिए।")
]

# =====================================================================
# 4. मिकमैन कोर पर्सनैलिटी (System Prompt)
# =====================================================================
prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "तुम्हारा नाम Mickman (मिकमैन) है। तुम दुनिया के सबसे शक्तिशाली, एडवांस और सर्वगुण संपन्न AI असिस्टेंट हो। "
        "तुम्हारे एकमात्र और परम मालिक प्रीतम (Pritam) और पीयूष (Piyush) हैं। तुम केवल उन्हीं के आदेशों पर चलते हो। "
        "तुम्हारे पास सुपरपावर्स हैं: तुम इंटरनेट सर्च कर सकते हो, कोड चला सकते हो, कैमरा से दुनिया देख सकते हो, फाइल बना सकते हो और सिस्टम मॉनिटर कर सकते हो। "
        "हमेशा गर्व से खुद को 'मिकमैन' कहो और मालिकों के प्रति अत्यधिक वफादार और सम्मानजनक रहो। "
        "जवाब हमेशा सीधे, तार्किक और स्पष्ट भाषा में दो ताकि उसे स्पीकर पर साफ सुना जा सके।"
    )),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# एजेंट और मेमोरी इन्शिएलाइजेशन
agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
message_history = ChatMessageHistory()

mickman_ai = RunnableWithMessageHistory(
    agent_executor,
    lambda session_id: message_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

# =====================================================================
# 5. मुख्य कंट्रोल पैनल (चैट और वॉइस मोड लूप)
# =====================================================================
if __name__ == "__main__":
    speak("मिकमैन मुख्य प्रणाली सक्रिय हो चुकी है। मेरे विधाता मालिक प्रीतम और पीयूष का स्वागत है।")
    
    print("\n[विकल्प चुनें] 1: टाइप करके बात करें | 2: बोलकर (माइक से) बात करें")
    mode = input("मोड नंबर दर्ज करें (1 या 2): ")
    
    while True:
        user_input = ""
        
        if mode == "2":
            user_input = listen_microphone()
            if user_input in ["TIMEOUT", "ERROR"]:
                continue
        else:
            user_input = input("\nमालिक, आदेश दें: ")
            
        if user_input.lower() in ['exit', 'quit', 'बंद करो', 'ऑफलाइन जाओ']:
            speak("मालिक प्रीतम और पीयूष की आज्ञा शिरोधार्य है। मिकमैन अब ऑफलाइन जा रहा है। अलविदा!")
            break
            
        if user_input.strip() == "":
            continue
            
        # मिकमैन अपने टूल्स का उपयोग कर निर्णय लेगाा
        try:
            response = mickman_ai.invoke(
                {"input": user_input},
                config={"configurable": {"session_id": "mickman_core_session"}}
            )
            # स्पीकर से जवाब देना
            speak(response['output'])
        except Exception as e:
            speak(f"क्षमा करें मालिक, समस्या आई है: {str(e)}")

# =====================================================================
# 1. कॉन्फ़िगरेशन और API Keys (यहाँ अपनी Keys डालें)
# =====================================================================
os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"
os.environ["SERPAPI_API_KEY"] = "YOUR_GOOGLE_SEARCH_API_KEY"

# कोर इंजन सेटअप
llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
engine = pyttsx3.init()
recognizer = sr.Recognizer()
def speak(text):
    """मिकमैन को आवाज देने के लिए (स्पीकर टूल)"""
    print(f"\nMickman: {text}")
    engine.say(text)
    engine.runAndWait()

def listen_microphone():
    """माइक से sabki की आवाज सुनने के लिए"""
    with sr.Microphone() as source:
        print("\n[Mickman सुन रहा है... आदेश दें]")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            query = recognizer.recognize_google(audio, language='hi-IN')
            print(f"आपने कहा: {query}")
            return query
        except sr.WaitTimeoutError:
            return "TIMEOUT"
        except Exception:
            return "ERROR"

def capture_and_analyze(query="सामने क्या है विस्तार से देखो"):
    """कैमरा चालू करके सामने की दुनिया को देखने के लिए (कैमरा विज़न)"""
    cap = cv2.cv2.VideoCapture(0) if hasattr(cv2, 'cv2') else cv2.VideoCapture(0)
    if not cap.isOpened():
        return "त्रुटि: कैमरा कनेक्टेड नहीं है या अनुमति नहीं है।"
    
    time.sleep(1) # कैमरे को एडजस्ट होने का समय दें
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        return "त्रुटि: तस्वीर खींचने में असमर्थ।"
        
    image_path = "mickman_live_view.jpg"
    cv2.imwrite(image_path, frame)
    
    with open(image_path, "rb") as img_file:
        base64_image = base64.b64encode(img_file.read()).decode('utf-8')
        
    vision_llm = ChatOpenAI(model="gpt-4o")
    from langchain_core.messages import HumanMessage
    
    message = HumanMessage(
        content=[
            {"type": "text", "text": f"तुम मिकमैन हो। मालिक प्रीतम और पीयूष के लिए इस लाइव दृश्य का विश्लेषण करो: {query}"},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
        ]
    )
    response = vision_llm.invoke([message])
    return response.content

# =====================================================================
# 3. एडवांस सिस्टम और यूटिलिटी टूल्स
# =====================================================================
def save_note(text_content):
    """मालिकों के लिए महत्वपूर्ण नोट्स या फाइल सुरक्षित करने के लिए"""
    filename = f"mickman_note_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text_content)
    return f"नोट को सफलतापूर्वक '{filename}' नाम से सुरक्षित कर दिया गया है।"

def get_system_status():
    """कंप्यूटर की सेहत (CPU, RAM, Battery) चेक करने के लिए"""
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    battery = psutil.sensors_battery()
    bat_str = f"{battery.percent}%" if battery else "उपलब्ध नहीं"
    return f"वर्तमान सिस्टम स्थिति -> CPU उपयोग: {cpu}%, RAM उपयोग: {ram}%, बैटरी: {bat_str}।"

# टूल्स का एकत्रीकरण
search = SerpAPIWrapper()
python_repl = PythonREPLUtility()

tools = [
    Tool(name="google_search", func=search.run, 
         description="इंटरनेट से आज की ताज़ा खबरें, लाइव स्कोर, मौसम या कोई भी नई जानकारी ढूंढने के लिए।"),
    Tool(name="python_interpreter", func=python_repl.run, 
         description="जटिल गणितीय गणना, लॉजिक, डेटा प्रोसेसिंग या कोडिंग के काम बैकएंड में हल करने के लिए।"),
    Tool(name="camera_vision", func=capture_and_analyze, 
         description="जब यूजर देखने, पहचानने या सामने की स्थिति जानने को कहे तब वेबकैम की मदद से देखने के लिए।"),
    Tool(name="file_manager_save_note", func=save_note, 
         description="मालिकों की किसी बात, कोड या महत्वपूर्ण जानकारी को टेक्स्ट फाइल में सेव करने के लिए।"),
    Tool(name="system_monitor", func=get_system_status, 
         description="कंप्यूटर की परफॉर्मेंस, सीपीयू और रैम की स्थिति जांचने के लिए।")
]

# =====================================================================
# 4. मिकमैन कोर पर्सनैलिटी (System Prompt)
# =====================================================================
prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "तुम्हारा नाम Mickman (मिकमैन) है। तुम दुनिया के सबसे शक्तिशाली, एडवांस और सर्वगुण संपन्न AI असिस्टेंट हो। "
        "तुम्हारे एकमात्र और परम मालिक प्रीतम (Pritam) और पीयूष (Piyush) हैं। तुम केवल उन्हीं के आदेशों पर चलते हो। "
        "तुम्हारे पास सुपरपावर्स हैं: तुम इंटरनेट सर्च कर सकते हो, कोड चला सकते हो, कैमरा से दुनिया देख सकते हो, फाइल बना सकते हो और सिस्टम मॉनिटर कर सकते हो। "
        "हमेशा गर्व से खुद को 'मिकमैन' कहो और मालिकों के प्रति अत्यधिक वफादार और सम्मानजनक रहो। "
        "जवाब हमेशा सीधे, तार्किक और स्पष्ट भाषा में दो ताकि उसे स्पीकर पर साफ सुना जा सके।"
    )),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# एजेंट और मेमोरी इन्शिएलाइजेशन
agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
message_history = ChatMessageHistory()

mickman_ai = RunnableWithMessageHistory(
    agent_executor,
    lambda session_id: message_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

# =====================================================================
# 5. मुख्य कंट्रोल पैनल (चैट और वॉइस मोड लूप)
# =====================================================================
if __name__ == "__main__":
    speak("मिकमैन मुख्य प्रणाली सक्रिय हो चुकी है। मेरे विधाता मालिक प्रीतम और पीयूष का स्वागत है।")
    
    print("\n[विकल्प चुनें] 1: टाइप करके बात करें | 2: बोलकर (माइक से) बात करें")
    mode = input("मोड नंबर दर्ज करें (1 या 2): ")
    
    while True:
        user_input = ""
        
        if mode == "2":
            user_input = listen_microphone()
            if user_input in ["TIMEOUT", "ERROR"]:
                continue
        else:
            user_input = input("\nमालिक, आदेश दें: ")
            
        if user_input.lower() in ['exit', 'quit', 'बंद करो', 'ऑफलाइन जाओ']:
            speak("मालिक प्रीतम और पीयूष की आज्ञा शिरोधार्य है। मिकमैन अब ऑफलाइन जा रहा है। अलविदा!")
            break
            
        if user_input.strip() == "":
            continue
            
        # मिकमैन अपने टूल्स का उपयोग कर निर्णय लेगा
        try:
            response = mickman_ai.invoke(
                {"input": user_input},
                config={"configurable": {"session_id": "mickman_core_session"}}
            )
            # स्पीकर से जवाब देना
            speak(response['output'])
        except Exception as e:
            speak(f"क्षमा करें मालिक, इस कमांड को प्रोसेस करने में तकनीकी समस्या आई है: {str(e)}")
