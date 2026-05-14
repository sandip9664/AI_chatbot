
from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_openrouter import ChatOpenRouter
from langchain_core.messages import BaseMessage,HumanMessage
from typing import TypedDict,Annotated,Literal
from dotenv import load_dotenv
import os
import sqlite3


load_dotenv()

class chatstate(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]

model=ChatOpenRouter(model='baidu/cobuddy:free',api_key=os.getenv('OPEN_ROUTER_API_KEY'))

def chat_node(state:chatstate):
    messages=state['messages']
    response=model.invoke(messages)
    return {'messages': [response]}

conn=sqlite3.connect(database="chatbot.db",check_same_thread=False)

checkpointer=SqliteSaver(conn=conn)

def init_db():
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS thread_metadata 
                      (thread_id TEXT PRIMARY KEY, title TEXT)''')
    conn.commit()

init_db()

graph=StateGraph(chatstate)

graph.add_node("chat_node",chat_node)



graph.add_edge(START,"chat_node")
graph.add_edge("chat_node",END)



chatbot=graph.compile(checkpointer=checkpointer)

def get_all_thread_metadata():
    cursor = conn.cursor()
    cursor.execute("SELECT title, thread_id FROM thread_metadata ")
    return [{"title": row[0], "id": row[1]} for row in cursor.fetchall()]

def save_thread_metadata(thread_id, title):
    cursor = conn.cursor()
    cursor.execute("INSERT  INTO thread_metadata (thread_id, title) VALUES (?, ?)", 
                   (thread_id, title))
    conn.commit()


