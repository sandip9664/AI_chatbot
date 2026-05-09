import streamlit as st
from main import chatbot
from langchain_core.messages import HumanMessage

# 1. Page Configuration
st.set_page_config(page_title="AI Assistant", page_icon="❄️", layout="centered")

# 2. Arctic Frost Styling (Clean, Light, Elegant)
st.markdown("""
    <style>
    /* Hide Sidebar and Header Clutter */
    [data-testid="stSidebar"], section[data-testid="stSidebar"] { display: none !important; }
    [data-testid="stHeader"] { background: rgba(255, 255, 255, 0); }
    footer {visibility: hidden;}

    /* Background: Soft Arctic White/Gray Gradient */
    .stApp {
        background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
    }

    /* Main Heading */
    .main-heading {
        font-family: 'SF Pro Display', 'Inter', sans-serif;
        color: #1e293b;
        font-weight: 700;
        font-size: 2.8rem;
        text-align: center;
        letter-spacing: -1.5px;
        margin-top: 3rem;
    }

    .sub-heading {
        color: #94a3b8;
        text-align: center;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 4px;
        margin-bottom: 4rem;
    }

    /* User Message: Crisp & Subtle */
    [data-testid="stChatMessageUser"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0;
        border-radius: 20px 20px 4px 20px;
        color: #334155;
        padding: 1.2rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.02);
    }

    /* Assistant Message: Glassmorphism / Frosted Look */
    [data-testid="stChatMessageAssistant"] {
        background-color: rgba(255, 255, 255, 0.6) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.8);
        border-radius: 20px 20px 20px 4px;
        color: #1e293b;
        padding: 1.2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.04);
    }

    /* Chat Input: Ultra-Clean Floating Bar */
    .stChatInputContainer {
        padding-bottom: 50px;
    }
    
    .stChatInput input {
        background-color: rgba(255, 255, 255, 0.8) !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 100px !important; /* Pill shape */
        color: #1e293b !important;
        padding: 15px 25px !important;
    }

    /* Markdown text improvements */
    .stMarkdown p {
        font-family: 'Inter', sans-serif;
        line-height: 1.75;
        font-size: 1.05rem;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Heading
st.markdown('<h1 class="main-heading">Interact with AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-heading">Intelligent Assistant</p>', unsafe_allow_html=True)

# 4. Session History
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

# 5. Message Rendering
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

# 6. Chat Logic
user_input = st.chat_input("How can I help you today?")

if user_input:
    # Append User
    st.session_state['message_history'].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Process AI Response
    with st.chat_message("assistant"):
        with st.spinner(" "): # Hidden spinner for clean look
            try:
                # Assuming your compiled chatbot from main.py
                config = {"configurable": {"thread_id": "arctic_thread"}}
                response = chatbot.invoke(
                    {"messages": [HumanMessage(content=user_input)]}, 
                    config=config
                )
                ai_message = response['messages'][-1].content
                
                st.markdown(ai_message)
                st.session_state['message_history'].append({"role": "assistant", "content": ai_message})
            except Exception as e:
                st.error("The system is currently unavailable. Please try again later.")