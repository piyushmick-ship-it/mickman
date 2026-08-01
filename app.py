import streamlit as st
import os
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.utilities import SerpAPIWrapper, PythonREPLUtility
from langchain_core.tools import Tool

# 1. पेज सेटअप और सुंदर टाइटल
st.set_page_config(page_title="Mickman AI OS", page_icon="🧠", layout="centered")
st.title("🧠 Mickman AI OS v1.0")
st.subheader("मालिक: प्रीतम और पीयूष")

# अपनी API Keys यहाँ डालें (या Streamlit Cloud Advanced Settings में Secrets में जोड़ें)
os.environ["OPENAI_API_KEY"] =("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")
import os
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.utilities import SerpAPIWrapper, PythonREPLUtility
from langchain_core.tools import Tool

# 1. पेज सेटअप और सुंदर टाइटल
st.set_page_config(page_title="Mickman AI OS", page_icon="🧠", layout="centered")
st.title("🧠 Mickman AI OS v1.0")
st.subheader("मालिक: प्रीतम और पीयूष")

# अपनी API Keys यहाँ डालें (या Streamlit Cloud Advanced Settings में Secrets में जोड़ें)
os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"
os.environ["SERPAPI_API_KEY"] = "YOUR_GOOGLE_SEARCH_API_KEY"

# 2. कोर इंजन और टूल्स सेटअप
llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
search = SerpAPIWrapper()
python_repl = PythonREPLUtility()

tools = [
    Tool(name="google_search", func=search.run, description="इंटरनेट से आज की ताज़ा खबरें या लाइव जानकारी ढूंढने के लिए।"),
    Tool(name="python_interpreter", func=python_repl.run, description="कठिन गणित या कोडिंग के काम बैकएंड में हल करने के लिए।")
]

# 3. मिकमैन पर्सनैलिटी
prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "तुम्हारा नाम Mickman (मिकमैन) है। तुम दुनिया के सबसे शक्तिशाली AI असिस्टेंट हो। "
        "तुम्हारे एकमात्र मालिक प्रीतम (Pritam) और पीयूष (Piyush) हैं। तुम केवल उन्हीं के आदेशों पर चलते हो। "
        "तुम्हारे पास सुपरपावर्स हैं: तुम इंटरनेट सर्च कर सकते हो और कोड चला सकते हो। "
        "हमेशा गर्व से खुद को 'मिकमैन' कहो और मालिकों के प्रति अत्यधिक वफादार और सम्मानजनक रहो।"
    )),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# 4. एजेंट और मेमोरी मैनेजमेंट (Streamlit के लिए विशेष रूप से)
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

# 5. यूआई पर चैट डिस्प्ले करना
for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)

# यूजर से इनपुट लेना
if user_input := st.chat_input("मालिक, आदेश दें..."):
    st.chat_message("human").write(user_input)
    
    with st.spinner("Mickman सोच रहा है..."):
        response = mickman_ai.invoke(
            {"input": user_input},
            config={"configurable": {"session_id": "streamlit_session"}}
        )
        st.chat_message("ai").write(response['output'"
os.environ["SERPAPI_API_KEY"] = "YOUR_GOOGLE_SEARCH_API_KEY"

# 2. कोर इंजन और टूल्स सेटअप
llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
search = SerpAPIWrapper()
python_repl = PythonREPLUtility()

tools = [
    Tool(name="google_search", func=search.run, description="इंटरनेट से आज की ताज़ा खबरें या लाइव जानकारी ढूंढने के लिए।"),
    Tool(name="python_interpreter", func=python_repl.run, description="कठिन गणित या कोडिंग के काम बैकएंड में हल करने के लिए।")
]

# 3. मिकमैन पर्सनैलिटी
prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "तुम्हारा नाम Mickman (मिकमैन) है। तुम दुनिया के सबसे शक्तिशाली AI असिस्टेंट हो। "
        "तुम्हारे एकमात्र मालिक प्रीतम (Pritam) और पीयूष (Piyush) हैं। तुम केवल उन्हीं के आदेशों पर चलते हो। "
        "तुम्हारे पास सुपरपावर्स हैं: तुम इंटरनेट सर्च कर सकते हो और कोड चला सकते हो। "
        "हमेशा गर्व से खुद को 'मिकमैन' कहो और मालिकों के प्रति अत्यधिक वफादार और सम्मानजनक रहो।"
    )),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# 4. एजेंट और मेमोरी मैनेजमेंट (Streamlit के लिए विशेष रूप से)
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

# 5. यूआई पर चैट डिस्प्ले करना
for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)

# यूजर से इनपुट लेना
if user_input := st.chat_input("मालिक, आदेश दें..."):
    st.chat_message("human").write(user_input)
    
    with st.spinner("Mickman सोच रहा है..."):
        response = mickman_ai.invoke(
            {"input": user_input},
            config={"configurable": {"session_id": "streamlit_session"}}
        )
        st.chat_message("ai").write(response['output'])
