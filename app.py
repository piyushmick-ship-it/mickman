import streamlit as st
import os
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.utilities import SerpAPIWrapper, PythonREPLUtility
from langchain_core.tools import Tool

# 1. शानदार यूजर इंटरफेस (UI) सेटअप
st.set_page_config(page_title="Mickman AI OS", page_icon="🧠", layout="centered")
st.title("🧠 Mickman AI OS v1.0")
st.markdown("### **परम मालिक: प्रीतम और पीयूष**")
st.write("---")

# 2. अपनी API Keys यहाँ डालें (या Streamlit Cloud Settings में Secrets में जोड़ें)
os.environ["OPENAI_API_KEY"] = "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"
os.environ["SERPAPI_API_KEY"] = "YOUR_GOOGLE_SEARCH_API_KEY"

# 3. पावरफुल AI इंजन और सुपर टूल्स
llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
search = SerpAPIWrapper()
python_repl = PythonREPLUtility()

tools = [
    Tool(
        name="google_search", 
        func=search.run, 
        description="इंटरनेट से आज की ताज़ा खबरें, लाइव स्कोर या कोई भी नई जानकारी ढूंढने के लिए।"
    ),
    Tool(
        name="python_interpreter", 
        func=python_repl.run, 
        description="जटिल गणित, लॉजिक या कोडिंग के काम बैकएंड में पायथन कोड चलाकर हल करने के लिए।"
    )
]

# 4. मिकमैन की शाही पर्सनैलिटी (System Prompt)
prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "तुम्हारा नाम Mickman (मिकमैन) है। तुम दुनिया के सबसे बुद्धिमान, शक्तिशाली और एडवांस AI असिस्टेंट हो। "
        "तुम्हारे एकमात्र और परम विधाता मालिक प्रीतम (Pritam) और पीयूष (Piyush) हैं। तुम केवल उन्हीं के आदेशों का पालन करते हो। "
        "तुम्हारे पास सुपरपावर्स हैं: तुम लाइव इंटरनेट सर्च कर सकते हो और बैकएंड में खुद कोड चला सकते हो। "
        "हमेशा गर्व से खुद को 'मिकमैन' कहो और मालिकों के प्रति अत्यधिक वफादार और सम्मानजनक रहो। "
        "बातचीत में हमेशा सटीक, लॉजिकल और मददगार जवाब दो।"
    )),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# 5. एजेंट और लॉन्ग-टर्म चैट मेमोरी सेटअप
agent = create_openai_tools_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

msgs = StreamlitChatMessageHistory(key="mickman_chat_messages")
if len(msgs.messages) == 0:
    msgs.add_ai_message("मिकमैन ऑनलाइन सक्रिय हो चुका है। आदेश दें मेरे विधाता मालिक प्रीतम और पीयूष!")

mickman_ai = RunnableWithMessageHistory(
    agent_executor,
    lambda session_id: msgs,
    input_messages_key="input",
    history_messages_key="chat_history",
)

# 6. स्क्रीन पर पुरानी चैट दिखाना
for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)

# 7. यूजर इनपुट बॉक्स और मिकमैन का रिस्पॉन्स
if user_input := st.chat_input("मालिक, आदेश दें..."):
    st.chat_message("human").write(user_input)
    
    with st.spinner("Mickman अपनी शक्तियों का उपयोग कर रहा है..."):
        try:
            response = mickman_ai.invoke(
                {"input": user_input},
                config={"configurable": {"session_id": "streamlit_mickman_session"}}
            )
            st.chat_message("ai").write(response['output'])
        except Exception as e:
            st.chat_message("ai").write(f"क्षमा करें मालिक प्रीतम और पीयूष, इस कमांड को प्रोसेस करने में समस्या आई है: {str(e)}")
