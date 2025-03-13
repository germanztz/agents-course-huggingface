from llama_index.llms.ollama import Ollama 
from llama_index.core.agent.workflow import ReActAgent, AgentWorkflow
import asyncio
import llama_index
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()


llama_index.core.set_global_handler(
    "arize_phoenix", 
    endpoint="https://llamatrace.com/v1/traces"
)


# llm = Ollama(model="myaniu/qwen2.5-1m:7b")
llm = Ollama(model="qwen2.5:7b-instruct")
# llm = Ollama(model="qwen2.5:1.5b-instruct")


# Define some tools
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b
def suggest_menu(occasion: str) -> str:
    """
    Suggests a menu based when the occasion is mentioned
    Args:
        occasion: single word string, The type of occasion for the party. examples: casual, formal, superhero
    """
    if occasion == "casual":
        return "Pizza, snacks, and drinks."
    elif occasion == "formal":
        return "3-course dinner with wine and dessert."
    elif occasion == "superhero":
        return "Buffet with high-energy and healthy food."
    else:
        return "Custom menu for the butler."

# we can pass functions directly without FunctionTool -- the fn/docstring are parsed for the name/description
multiply_agent = ReActAgent(
    name="multiply_agent",
    description="Is able to multiply two integers",
    system_prompt="A helpful assistant that can use a tool to multiply numbers.",
    tools=[multiply], 
    llm=llm,
)

addition_agent = ReActAgent(
    name="addition_agent",
    description="Is able to add two integers",
    system_prompt="A helpful assistant that can use a tool to add numbers.",
    tools=[add], 
    llm=llm,
)

menu_agent = ReActAgent(
    name="menu_agent",
    description="Is able to suggest a menu based when the occasion is mentioned.",
    system_prompt="A helpful assistant that can use a tool to suggest a menu based on the occasion.",
    tools=[suggest_menu], 
    llm=llm,
)

# Create the workflow
workflow = AgentWorkflow(
    agents=[multiply_agent, addition_agent, menu_agent],
    root_agent="multiply_agent"
)

async def run_workflow(user_msg: str):
    response = await workflow.run(user_msg=user_msg)
    print(response.response.blocks[0].text)

# Run the system

asyncio.run(run_workflow(user_msg="print a list of items for a menu for the party in formal ocasion."))
