"""Test script for Ollama integration."""

import sys
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from config import AgentConfig

def test_ollama_integration():
    """Test that the Ollama integration works correctly."""
    config = AgentConfig()
    
    try:
        # Make sure Ollama is running
        print(f"Testing connection to Ollama at {config.ollama_base_url}")
        print(f"Using model: {config.model_name}")
        
        # Initialize ChatOllama
        chat_model = ChatOllama(
            base_url=config.ollama_base_url,
            model=config.model_name,
            temperature=config.temperature,
        )
        
        # Test a simple prompt
        prompt = "Say hello and introduce yourself in one sentence."
        print(f"\nTesting prompt: {prompt}")
        
        response = chat_model.invoke([HumanMessage(content=prompt)])
        print(f"\nResponse from Ollama ({config.model_name}):")
        print(response.content)
        
        # Test tool calling capability
        print("\nTesting tool calling capability...")
        tool_schema = {
            "name": "calculator",
            "description": "Useful for performing calculations",
            "parameters": {
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "enum": ["add", "subtract", "multiply", "divide"]
                    },
                    "a": {"type": "number"},
                    "b": {"type": "number"}
                },
                "required": ["operation", "a", "b"]
            }
        }
        
        try:
            # Try to use bind_tools - this may not work with all models
            tool_model = chat_model.bind_tools([tool_schema])
            calculator_prompt = "What is 5 multiplied by 10?"
            tool_response = tool_model.invoke([HumanMessage(content=calculator_prompt)])
            print(f"\nTool response: {tool_response}")
            print(f"Tool calls: {tool_response.tool_calls if hasattr(tool_response, 'tool_calls') else 'Not supported'}")
        except Exception as e:
            print(f"\nTool calling test failed (this is normal for some models): {str(e)}")
        
        print("\nOllama integration test successful!")
        return True
    except Exception as e:
        print(f"\nError testing Ollama integration: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Make sure Ollama is running with 'ollama serve'")
        print(f"2. Make sure the model '{config.model_name}' is pulled with 'ollama pull {config.model_name}'")
        print("3. Check the Ollama base URL in config.py")
        return False

if __name__ == "__main__":
    success = test_ollama_integration()
    sys.exit(0 if success else 1)