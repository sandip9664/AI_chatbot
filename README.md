AI Chatbot 🤖

Description

An elegant, minimalist AI chatbot featuring a premium "Arctic Frost" interface. It uses LangGraph to manage conversation states, ensuring intelligent responses and persistent memory.

Procedure

Install: Run pip install streamlit langgraph langchain-openrouter python-dotenv.

Key: Put your OpenRouter API key in a .env file.

Run: Start the app with streamlit run app.py

Tools & Skills Used

Core Technologies

Python: The primary programming language used for all logic and backend development.  

LangGraph: Used for building the agentic state machine that manages conversation flows and memory.  

Streamlit: The framework used to build the interactive web interface.  

OpenRouter API: Utilized to access and integrate large language models like baidu/cobuddy.  

Technical Skills

Stateful Orchestration: Designing a StateGraph to manage message history and node transitions.  

Prompt Engineering: Crafting specialized system prompts to define the AI's behavior and personality.  

Custom UI/UX Design: Injecting custom CSS into Streamlit to create a premium "Arctic Frost" theme with glassmorphism and frosted-glass effects.  

Backend Architecture: Developing a persistent memory system using InMemorySaver and thread_id to handle multi-turn interactions.  


