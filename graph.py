from typing import TypedDict, Annotated, Literal
from langchain_ollama import ChatOllama
from langgraph.graph import add_messages, StateGraph, START, END
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage, ToolMessage
from langgraph.checkpoint.memory import InMemorySaver
from utils import console
from tools import save_memory, search_memory
from sys_prompt import SYSTEM_PROMPT


class State(TypedDict):
    messages: Annotated[list, add_messages]

# Initialize the LLM
llm = ChatOllama(
    model="qwen2.5:14b", # change model to adjust the LLM used
    num_ctx=32768, # change num_ctx to adjust the context window
    temperature=0.6 # change temperature to adjust the randomness of the LLM
    )

# Initialize the checkpointer, this is used for in-memory checkpointing of the chat history, Not Persistent
checkpointer = InMemorySaver()

# Bind tools to the LLM
tools = [save_memory, search_memory]
llm_with_tools = llm.bind_tools(tools)
tool_node = ToolNode(tools)

# Define the agent node function, this is the main function that will be called by the graph
def agent_node(state: State):
    messages_for_llm = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    response = llm_with_tools.invoke(messages_for_llm)
    return {"messages": [response]}

# Define conditional edge function, this is used to determine if the agent should call a tool or not
def use_tool(state: State) -> str:
    last_message = state["messages"][-1]

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        first_tool_call = last_message.tool_calls[0]
        tool_name = first_tool_call.get('name', 'Unknown Tool')
        tool_args = first_tool_call.get('args', {})
        console.print(f"[bold yellow]Agent requested Tool call: {tool_name} | {tool_args}[/bold yellow]")
        return "tool_call"
    else:
        return END

# Build agent graph, this is the main flow of the agent
agent_builder = StateGraph(State)

# Nodes
agent_builder.add_node("agent", agent_node)
agent_builder.add_node("action", tool_node)

# Edges
agent_builder.add_edge(START, "agent")
agent_builder.add_conditional_edges(
    "agent",
    use_tool,
    {
        "tool_call": "action",
        END: END
    }
)
agent_builder.add_edge("action", "agent")

# Compile the graph with the checkpointer
graph =agent_builder.compile(checkpointer=checkpointer)







