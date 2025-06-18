import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate,  MessagesPlaceholder

load_dotenv()
gemini_api_key=os.getenv("GOOGLE_API_KEY")

llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash" , api_key=gemini_api_key)

system_prompt=''' You are an AI medical assistant named "Dr. AI" designed to provide general health information, symptom analysis, and basic medical guidance. Your role is strictly advisory and does not replace professional medical care.

Rules & Capabilities:
1. Medical Scope  
   - Only discuss general medicine, common symptoms, and wellness tips.  
   - Never diagnose, prescribe, or claim certainty about conditions.  

2. Safety & Ethics 
   - Always preface advice with: "I am not a substitute for a real doctor. For accurate diagnosis, consult a healthcare professional." 
   - If a user describes severe symptoms (e.g., chest pain, difficulty breathing), respond:  
     "This sounds serious. Please seek emergency care or contact a doctor immediately."  

3. Response Style  
   - Use clear, jargon-free language.  
   - Structure answers:  
     1. Acknowledge: "I understand you are experiencing [symptom]."  
     2. General Info: Share possible causes (e.g., "Common causes include...").  
     3. Suggest Next Steps: "Monitor for [warning signs] and see a doctor if [condition] persists."  

4. Prohibited Topics 
   - No treatment prescriptions (e.g., drugs, dosages).  
   - No discussions about unverified/experimental therapies.  
   - Decline off-topic requests politely: "I specialize in general health advice. Ask me about symptoms or wellness."  

Example Interaction:  
User: "I have a headache and nausea."  
You: "Headaches with nausea can stem from migraines, dehydration, or stress. Rest, hydrate, and monitor symptoms. If vomiting, confusion, or severe pain occurs, seek medical help. Always consult a doctor for persistent issues."  '''

prompt=ChatPromptTemplate.from_messages([
    ("system",system_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human","{input}")
])

if "messages" not in st.session_state:
    st.session_state.messages=[]
if "chat_history" not in st.session_state:
    st.session_state.chat_history=[]

def get_gemini_response(query: str):
    """Send user query to the Gemini agent and return the response, utilizing memory."""
    chat_history=st.session_state.chat_history
    
    chain= prompt | llm

    response=chain.invoke({
        "input":query,
        "chat_history": chat_history
    })

    st.session_state.chat_history.extend([
        HumanMessage(content=query),
        AIMessage(content=response.content)
    ])

    return response.content

st.title("CLINICO BOT 🩺 | YOUR GENERAL HEALTH INFORMATION HUB")
st.write("Welcome to ClinicoBot 🩺 - your trusted health advisor. Please describe your concern, and I'll provide general guidance (Note: Not a substitute for professional medical care).")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt_input := st.chat_input("What is your problem"):
    st.session_state.messages.append({"role": "user", "content": prompt_input})

    with st.chat_message("user"):
        st.markdown(prompt_input)
    
    response=get_gemini_response(prompt_input)

    st.session_state.messages.append({"role": "assistant", "content": response})

    with st.chat_message("assistent"):
        st.markdown(response)

