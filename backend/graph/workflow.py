from datetime import date
from operator import add
from typing import Annotated, Any, List, Optional, TypedDict

import pytesseract
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, BaseMessage
from langchain_groq import ChatGroq
from langgraph.graph import END, START, StateGraph
from PIL import Image
from pydantic import BaseModel, Field
from datetime import datetime

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Users\Asus\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
)


load_dotenv()

llm = ChatGroq(model="qwen/qwen3.6-27b")


# graph schema
class graph_Schema(TypedDict):
    input_type: str
    text: Optional[str]
    image_path: Optional[str]
    reply: Annotated[List[BaseMessage], add]
    caption: Optional[str]


# schema for llm response
class ExpenseSchema(BaseModel):
    amount: float = Field(description="Transaction amount")

    category: Optional[str] = Field(
        description="Broad expense category such as Travel, Food, Transportation, Utilities, Shopping, Entertainment, Healthcare, Education, Housing. Avoid overly specific subcategories. If cant get catgeory just return ,  null"
    )

    transaction_date: str = Field(
        description="Date of the transaction if available", default_factory= datetime.now
    )


# llm call with schema
structured_llm = llm.with_structured_output(ExpenseSchema)


# choose path based on input
def choose(state: graph_Schema) -> str:
    if state["input_type"] == "image":
        return "welcome1"

    if state["input_type"] == "text":
        return "welcome"

    return "error"


# call llm when text send only
def welcome(state: graph_Schema) -> graph_Schema:

    expense = structured_llm.invoke(
        f"""
        Extract expense information from the text below.

        Text:
        {state["text"]}
        """
    )

    print("Reply ready")

    if not expense.category:
        reply_text = f"❓ I recorded an expense of ₹{expense.amount:.2f}, but what did you spend it on? (e.g., Food, Travel, Shopping)"
        return {"reply": [AIMessage(content=reply_text)]}

    ai_msg = AIMessage(content=expense.model_dump_json())

    return {"reply": [ai_msg]}


# call ocr to extarct text from image and call llm
def welcome1(state: graph_Schema) -> graph_Schema:

    image_path = state["image_path"]

    img = Image.open(image_path)

    text = pytesseract.image_to_string(img)

    print("Image extraction completed")

    expense = structured_llm.invoke(
        f"""
        Extract expense information from the text below. and captions is also provided 

        Text:
        {text}
        
        Caption : 
        {state["caption"]}
        """
    )

    print("Reply ready")

    if not expense.category:
        reply_text = f"❓ I recorded an expense of ₹{expense.amount:.2f}, but what did you spend it on? (e.g., Food, Travel, Shopping)"
        return {"reply": [AIMessage(content=reply_text)]}

    ai_msg = AIMessage(content=expense.model_dump_json())

    return {"reply": [ai_msg]}


# graph start
graph = StateGraph(graph_Schema)

graph.add_node("welcome", welcome)
graph.add_node("welcome1", welcome1)

graph.add_conditional_edges(
    START,
    choose,
    {
        "welcome": "welcome",
        "welcome1": "welcome1",
    },
)

graph.add_edge("welcome", END)
graph.add_edge("welcome1", END)

first_graph = graph.compile()
