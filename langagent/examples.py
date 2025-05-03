"""Example usage of the LangGraph agent."""

from modules.agent import run_agent
from langchain_core.messages import HumanMessage

# Example queries to test the agent
EXAMPLE_QUERIES = [
    "Search for information about LangGraph and summarize what it is.",
    "Find a tutorial on creating a simple Flask application and generate a hello world app.",
    "Create a Python script called 'weather.py' that fetches weather data from an API.",
    "Run 'ls -la' to show files in the current directory.",
]

def run_examples():
    """Run example queries to demonstrate the agent's capabilities."""
    print("🤖 LangGraph Agent Examples")
    print("=" * 80)
    
    for i, query in enumerate(EXAMPLE_QUERIES, 1):
        print(f"\nExample {i}: {query}")
        print("-" * 80)
        
        # Run the agent
        human_message = HumanMessage(content=query)
        result, chat_history = run_agent(query, [human_message])
        
        # Print the result
        print(f"🤖 Response:")
        print(chat_history[-1].content)
        print("=" * 80)
        
        # Ask if user wants to continue
        if i < len(EXAMPLE_QUERIES):
            cont = input("Continue to next example? (y/n): ")
            if cont.lower() != 'y':
                break

if __name__ == "__main__":
    run_examples()