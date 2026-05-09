from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver
from langchain_openrouter import ChatOpenRouter
from langchain_core.messages import BaseMessage,HumanMessage
from typing import TypedDict,Annotated,Literal
from dotenv import load_dotenv
import os


load_dotenv()

class chatstate(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]

model=ChatOpenRouter(model='baidu/cobuddy:free',api_key=os.getenv('OPEN_ROUTER_API_KEY'))

def chat_node(state:chatstate):
    messages=state['messages']
    response=model.invoke(messages)
    return {'messages': [response]}

checkpointer=InMemorySaver()

graph=StateGraph(chatstate)

graph.add_node("chat_node",chat_node)



graph.add_edge(START,"chat_node")
graph.add_edge("chat_node",END)



chatbot=graph.compile()
