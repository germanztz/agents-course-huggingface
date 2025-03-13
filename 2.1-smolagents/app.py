from phoenix.otel import register
from openinference.instrumentation.smolagents import SmolagentsInstrumentor
from smolagents import CodeAgent, ToolCallingAgent, DuckDuckGoSearchTool, VisitWebpageTool, LiteLLMModel, FinalAnswerTool, tool


@tool
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


register(project_name="smolagents-local" )
SmolagentsInstrumentor().instrument()

# manager_model = LiteLLMModel(model_id="ollama_chat/myaniu/qwen2.5-1m:7b", api_base="http://localhost:11434" ) # sigue instruct pero llena la memoria
# manager_model = LiteLLMModel(model_id="ollama_chat/qwen2.5-coder:1.5b-base", api_base="http://localhost:11434" ) # no sigue las instrucciones bien
manager_model = LiteLLMModel(model_id="ollama_chat/llama3.1:8b-instruct-q3_K_S", api_base="http://localhost:11434" ) # de momento es el mejor
# manager_model = LiteLLMModel(model_id="ollama_chat/llama3.2", api_base="http://localhost:11434" ) # no llama a agentes
tool_model = LiteLLMModel(model_id="ollama_chat/llama3.2", api_base="http://htpc.local:11434" )

menu_agent = ToolCallingAgent(
    tools=[suggest_menu], 
    model=manager_model, 
    name="menu_agent",
    description="""This is an agent that Suggests a menu based when the occasion is mentioned. For example: 
     - I'm having a casual party, what we can have?.
     - If you're having a formal party, what would you like?.""",
    )


# search_agent = ToolCallingAgent(
#     tools=[DuckDuckGoSearchTool()],
#     model=tool_model,
#     name="search_agent",
#     description="This is an agent that can do web search.",
# )

manager_agent = CodeAgent(
    name="manager_agent",
    description="This is the manager agent. It orchestrates tasks and MUST call `final_answer` to return a final response.",
    tools=[FinalAnswerTool()],
    model=manager_model,
    managed_agents=[menu_agent],
    # additional_authorized_imports=['requests','re', 'itertools', 'collections', 'stat', 'random', 'statistics', 'math', 'unicodedata', 'datetime', 'time', 'queue'],
    # max_steps=5

)


if __name__ == "__main__":
    # manager_agent.visualize()
    # manager_agent.run("If the US keeps its 2024 growth rate, how many years will it take for the GDP to double?" )
    # manager_agent.run("what is the curren value of the GDP of france?" )
    # search_agent.run("what is the curren value of the GDP of france?" )
    manager_agent.run("use the menu_agent to Suggest all the plates and drinks for a menu for the party in formal ocasion.")
    

# python -m phoenix.server.main serve
# http://127.0.0.1:6006/projects/UHJvamVjdDox/traces