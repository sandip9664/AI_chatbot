import streamlit as st
from main import chatbot,get_all_thread_metadata,save_thread_metadata
from langchain_core.messages import HumanMessage
import uuid

# 1. Page Configuration
st.set_page_config(page_title="AI Assistant", page_icon="❄️", layout="centered")

# 2. Arctic Frost Styling (Clean, Light, Elegant)
st.markdown("""
    <style>
    /* Hide Sidebar and Header Clutter */
   
    .css-1d391kg {display: none;} /* Hide Streamlit header */

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
if 'threads_id' not in st.session_state:
    st.session_state['threads_id']=get_all_thread_metadata()

if 'current_thread' not in st.session_state:
    current_thread=str(uuid.uuid4())
    st.session_state['current_thread']=current_thread
    
# 5. Message Rendering
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

# 6. Chat Logic
user_input = st.chat_input("How can I help you today?")







    

if user_input:
    # Append User
    if not st.session_state['message_history']:
        # Extract first 20 chars as the thread name
        new_title = user_input[:20] + ("..." if len(user_input) > 20 else "")
        
        st.session_state['threads_id'].append({"title": new_title, "id": st.session_state['current_thread']})
        save_thread_metadata(st.session_state['current_thread'], new_title)
            # This makes the sidebar update immediately

    
    
    # TASK B: Respond & Save to Chat
    st.session_state['message_history'].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Process AI Response
    with st.chat_message("assistant"):
        with st.spinner(" "): # Hidden spinner for clean look
            try:
                # Assuming your compiled chatbot from main.py
                current_id = st.session_state['current_thread']
                config = {"configurable": {"thread_id": current_id}}
                
                ai_message = st.write_stream(
                    message_chunk.content for message_chunk,metedata in chatbot.stream(
                        {'messages':[HumanMessage(content=user_input)]},
                         config=config,
                         stream_mode='messages'
                    )
                )
                
                
                st.session_state['message_history'].append({"role": "assistant", "content": ai_message})
            except Exception as e:
                st.error("The system is currently unavailable. Please try again later.")


with st.sidebar:
    st.title("❄️ Chat History")
    
    
    if st.button(' New Chat', use_container_width=True):
        st.session_state['message_history'] = []
        current_thread = str(uuid.uuid4())
        st.session_state['current_thread'] = current_thread
        
        st.rerun()

    st.divider()
    
    
    for thread_obj in reversed(st.session_state['threads_id']):
        
        if st.button(f"💬 {thread_obj['title']}", key=f"btn_{thread_obj['id']}", use_container_width=True):
            st.session_state['current_thread'] = thread_obj['id']
            messages=chatbot.get_state(config={"configurable": {"thread_id": thread_obj['id']}}).values['messages']
            temp_history=[]
            
            for message in messages:
                
                role = 'user' if isinstance(message, HumanMessage) else 'assistant'
                temp_history.append({'role':role,'content':message.content})
            st.session_state['message_history']=temp_history
            st.rerun()
            
            


