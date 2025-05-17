import streamlit as st
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

load_dotenv()

# Define tools
@tool
def calculator(a: float, b: float) -> str:
    """Useful for performing basic arithmetic calculations with numbers"""
    return f"The sum of {a} and {b} is {a + b}"

@tool
def say_hello(name: str) -> str:
    """Useful for greeting a user"""
    return f"Hello {name}, I hope you are well today"

# Initialize the model and tools
model = ChatOpenAI(temperature=0)
tools = [calculator, say_hello]
agent_executor = create_react_agent(model, tools)

# Streamlit UI
st.set_page_config(page_title="AI Assistant", page_icon="🧠")
st.title("🧠 AI Assistant")

st.markdown("Ask the assistant to calculate or greet someone!")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input box
user_input = st.text_input("You:", key="user_input")

if user_input:
    # Append user's message
    st.session_state.chat_history.append(("You", user_input))
    # Stream output
    response_text = ""
    response_placeholder = st.empty()

    for chunk in agent_executor.stream(
        {"messages": [HumanMessage(content=user_input)]}
    ):
        if "agent" in chunk and "messages" in chunk["agent"]:
            for message in chunk["agent"]["messages"]:
                response_text += message.content
                response_placeholder.markdown(f"**Assistant:** {response_text}")

    st.session_state.chat_history.append(("Assistant", response_text))

# Show chat history
if st.session_state.chat_history:
    st.markdown("---")
    st.subheader("Chat History")
    for speaker, msg in st.session_state.chat_history:
        st.markdown(f"**{speaker}:** {msg}")
