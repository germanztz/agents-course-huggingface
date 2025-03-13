from smolagents import CodeAgent, DuckDuckGoSearchTool, FinalAnswerTool, HfApiModel, Tool, tool, VisitWebpageTool, LiteLLMModel
from llama_index.embeddings.ollama import OllamaEmbedding
import ollama
from phoenix.otel import register
from openinference.instrumentation.smolagents import SmolagentsInstrumentor

register(project_name="smolagents-local" )
SmolagentsInstrumentor().instrument()


@tool
def suggest_menu(occasion: str) -> str:
    """
    Suggests a menu based on the occasion.
    Args:
        occasion: The type of occasion for the party.
    """
    if occasion == "casual":
        return "Pizza, snacks, and drinks."
    elif occasion == "formal":
        return "3-course dinner with wine and dessert."
    elif occasion == "superhero":
        return "Buffet with high-energy and healthy food."
    else:
        return "Custom menu for the butler."

@tool
def catering_service_tool(query: str) -> str:
    """
    This tool returns the highest-rated catering service in Gotham City.
    
    Args:
        query: A search term for finding catering services.
    """
    # Example list of catering services and their ratings
    services = {
        "Gotham Catering Co.": 4.9,
        "Wayne Manor Catering": 4.8,
        "Gotham City Events": 4.7,
    }
    
    # Find the highest rated catering service (simulating search query filtering)
    best_service = max(services, key=services.get)
    
    return best_service

class SuperheroPartyThemeTool(Tool):
    name = "superhero_party_theme_generator"
    description = """
    This tool suggests creative superhero-themed party ideas based on a category.
    It returns a unique party theme idea."""
    
    inputs = {
        "category": {
            "type": "string",
            "description": "The type of superhero party (e.g., 'classic heroes', 'villain masquerade', 'futuristic Gotham').",
        }
    }
    
    output_type = "string"

    def forward(self, category: str):
        themes = {
            "classic heroes": "Justice League Gala: Guests come dressed as their favorite DC heroes with themed cocktails like 'The Kryptonite Punch'.",
            "villain masquerade": "Gotham Rogues' Ball: A mysterious masquerade where guests dress as classic Batman villains.",
            "futuristic Gotham": "Neo-Gotham Night: A cyberpunk-style party inspired by Batman Beyond, with neon decorations and futuristic gadgets."
        }
        
        return themes.get(category.lower(), "Themed party idea not found. Try 'classic heroes', 'villain masquerade', or 'futuristic Gotham'.")

# Define a custom model class for Ollama
class OllamaModel:
    def __init__(self, model_name):
        self.model_name = model_name

    def __call__(self, prompt, stop_sequences=["Task"]):
        # Use Ollama's generate or chat API to handle prompts
        response = ollama.chat(model=self.model_name, messages=[{"role": "user", "content": prompt}])
        return response['message']['content']

# Initialize the agent with OllamaModel
# ollama_model = OllamaModel(model_name="llama3.1:8b-instruct-q3_K_S")
ollama_model = LiteLLMModel(model_id="ollama_chat/llama3.1:8b-instruct-q3_K_S", api_base="http://localhost:11434" )
# Alfred, the butler, preparing the menu for the party
agent = CodeAgent(
    tools=[
        DuckDuckGoSearchTool(), 
        VisitWebpageTool(),
        suggest_menu,
        catering_service_tool,
        SuperheroPartyThemeTool()
    ], 
    model=ollama_model,
    max_steps=10,
    verbosity_level=2,
    additional_authorized_imports=['requests','re', 'itertools', 'collections', 'stat', 'random', 'statistics', 'math', 'unicodedata', 'datetime', 'time', 'queue'],
)


agent.run("Give me the best playlist for a party at the Wayne's mansion. The party idea is a 'villain masquerade' theme")