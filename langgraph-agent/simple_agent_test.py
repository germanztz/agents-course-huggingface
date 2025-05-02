"""Simple test for the LangGraph agent with Ollama."""

from typing import List
import time
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from modules.agent import run_agent

def simple_test():
    """Run a simple test of the agent."""
    print("🤖 Testing LangGraph Agent with Ollama Qwen3")
    print("-" * 80)
    
    # Define test queries
    test_queries = [
        "What is LangGraph and how can it be used for agent development?",
        "Write a simple Python function that calculates fibonacci numbers recursively",
    ]
    
    # Initialize an empty chat history
    chat_history: List[BaseMessage] = []
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🧑 Test Query #{i}: {query}")
        print("-" * 80)
        
        # Add the query as a human message
        human_message = HumanMessage(content=query)
        chat_history.append(human_message)
        
        # Run the agent
        try:
            print("Running agent...")
            start_time = time.time()
            result, chat_history = run_agent(query, chat_history)
            end_time = time.time()
            
            # Display the response
            if chat_history and len(chat_history) > 1:
                print("\n🤖 Agent response:")
                print(chat_history[-1].content)
                print(f"\nQuery completed in {end_time - start_time:.2f} seconds")
            else:
                print("❌ Agent didn't generate a response")
            
            print("-" * 80)
        except Exception as e:
            print(f"❌ Error running agent: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print("\n✅ Agent test completed")

if __name__ == "__main__":
    simple_test()