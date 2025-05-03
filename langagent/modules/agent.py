"""Agent module using LangGraph."""

from typing import Dict, Any, List, Tuple, Annotated, TypedDict, Union
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.tools import BaseTool
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langgraph.graph import END, StateGraph

from modules.llm import get_ollama_llm, create_agent_prompt
from tools.web_search import web_search
from tools.web_scraper import web_scrape
from tools.file_operations import read_file, write_file
from tools.bash_executor import execute_bash
from config import AgentConfig

from langfuse.callback import CallbackHandler
# load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Initialize Langfuse CallbackHandler for LangGraph/Langchain (tracing) https://cloud.langfuse.com
langfuse_handler = CallbackHandler() 

config = AgentConfig()


# Define the state
class AgentState(TypedDict):
    """State for the agent graph."""
    input: str
    chat_history: List[BaseMessage]
    agent_outcome: Any
    
# Define the tools
def get_tools() -> List[BaseTool]:
    """
    Get the list of available tools.
    
    Returns:
        List of tools for the agent
    """
    return [
        web_search,
        web_scrape,
        read_file,
        write_file,
        execute_bash,
    ]

def create_agent() -> AgentExecutor:
    """
    Create the agent executor.
    
    Returns:
        Configured AgentExecutor
    """
    # Get LLM
    llm = get_ollama_llm()
    
    # Get prompt
    prompt = create_agent_prompt()
    
    # Get tools
    tools = get_tools()
    
    # Create the agent - using the create_tool_calling_agent
    agent = create_tool_calling_agent(llm, tools, prompt)
    
    # Create the agent executor
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=config.max_iterations,
    )

def create_agent_graph() -> StateGraph:
    """
    Create the agent graph.
    
    Returns:
        StateGraph for agent execution
    """
    # Define the graph nodes
    agent = create_agent()
    
    # Define the workflow
    workflow = StateGraph(AgentState)
    
    # Define the nodes
    workflow.add_node("agent", agent)
    
    # Define the edges
    workflow.set_entry_point("agent")
    workflow.add_edge("agent", END)
    
    # Compile the graph
    return workflow.compile()

def run_agent(query: str, chat_history: List[BaseMessage] = None) -> Tuple[Any, List[BaseMessage]]:
    """
    Run the agent with a query.
    
    Args:
        query: User query
        chat_history: Optional chat history
        
    Returns:
        Tuple of agent response and updated chat history
    """
    if chat_history is None:
        chat_history = []
    
    # Create the graph
    graph = create_agent_graph()
    
    # Set the initial state
    state = {
        "input": query,
        "chat_history": chat_history,
        "agent_outcome": None,
    }
    
    # Run the graph
    result = graph.invoke(state, config={"callbacks": [langfuse_handler]})
    
    # Return the result
    return result["agent_outcome"], result["chat_history"]