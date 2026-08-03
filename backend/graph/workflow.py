from operator import add
from typing import Annotated, Any, List, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage
from langchain_groq import ChatGroq
from langgraph.graph import END, START, StateGraph

class graph_schema(TypedDict):
    messages_manual: List[Any]
    message_auto: Annotated[List[Any], add]


load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile")


class graph_Schema(TypedDict):
    message: Annotated[List[Any], add]


def welcome(state: graph_Schema) -> graph_Schema:
    curr_message = state.get("message" , [])
    
    response = llm.invoke(curr_message).content

    ai_msg = AIMessage(content=response)
    
    return {"message" : [ai_msg]}


graph = StateGraph(graph_Schema)

graph.add_node("welcome", welcome)
graph.add_edge(START, "welcome")
graph.add_edge("welcome", END)

first_graph = graph.compile()

