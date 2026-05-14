🗨️ Streamlit Chat Assistant with LangGraph + LangChain
A lightweight yet stateful chat assistant web app built with Streamlit on the front‑end and a compiled LangGraph + LangChain chatbot under the hood. It supports persistent conversation threads, checkpointing, and a clean chat UI for managing multiple sessions.

🚀 Features
Interactive Chat UI: Streamlit front‑end with real‑time streaming responses.

Thread Management: Create, load, and persist multiple conversation threads with titles and IDs.

Stateful Conversations: LangGraph checkpointing ensures continuity across sessions.

SQLite Persistence: Local database stores both thread metadata and conversation state.

Seamless Integration: LangChain + OpenRouter model wrapper for flexible LLM backends.

📂 Key Files
main.py

Constructs the StateGraph, chatbot node(s), and integrates the ChatOpenRouter model.

Implements checkpointing with SqliteSaver.

Provides helper functions:

get_all_thread_metadata() → fetch all saved thread titles + IDs.

save_thread_metadata(thread_id, title) → insert new thread records.

app.py

Streamlit UI for chatting with the compiled chatbot.

Displays threads in the sidebar and streams assistant responses.

Handles session state (message_history, current_thread, threads_id).

🛠️ Tech Stack
Frontend: Streamlit

Backend / Orchestration: LangGraph, LangChain, ChatOpenRouter

Database: SQLite (chatbot.db)

Utilities: dotenv, uuid, Python typing (TypedDict, Annotated)

Standard Libraries: os, sqlite3

💾 Data & Persistence
Thread Metadata: Stored in thread_metadata table (thread_id, title).

Conversation State: Managed by LangGraph SqliteSaver scoped to each thread_id.

Session State: Streamlit keeps track of active thread and message history.

🔄 How It Works
Chat Node: main.py defines chat_node → calls model.invoke(messages) → returns assistant messages.

Graph Compilation: StateGraph compiled with SqliteSaver → exposed as chatbot.

Streaming: app.py calls chatbot.stream → streams chunks to UI.

Thread Lifecycle:

New chat → save_thread_metadata() inserts record.

Sidebar → load past threads via chatbot.get_state(config={thread_id}).

📌 Getting Started

# Clone the repo
git clone https://github.com/sandip9664/AI_chatbot.git && cd AI_chatbot

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
echo "OPENROUTER_API_KEY=your_key_here" > .env

# Run the app
streamlit run app.py

