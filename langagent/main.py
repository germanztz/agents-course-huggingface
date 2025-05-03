"""Main application for the LangGraph agent."""

import os
import sys
import argparse
import uuid
from typing import List, Dict, Any
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

from modules.agent import run_agent

def display_message(message: BaseMessage) -> None:
    """
    Display a chat message with appropriate formatting.
    
    Args:
        message: The message to display
    """
    if isinstance(message, HumanMessage):
        prefix = "🧑 Human: "
    elif isinstance(message, AIMessage):
        prefix = "🤖 Assistant: "
    else:
        prefix = "🔄 System: "
    
    print(f"{prefix}{message.content}")
    print("-" * 80)

def main() -> None:
    """Main function to run the agent."""
    parser = argparse.ArgumentParser(description="LangGraph Agent with Ollama Qwen3")
    parser.add_argument("--query", "-q", type=str, help="Query for the agent")
    parser.add_argument("--interactive", "-i", action="store_true", help="Run in interactive mode", default=True)
    parser.add_argument("--session", "-s", type=str, help="Session ID for conversation persistence")
    
    args = parser.parse_args()
    
    if not args.query and not args.interactive:
        parser.print_help()
        sys.exit(1)
    
    # Generate or use provided session ID
    session_id = args.session if args.session else str(uuid.uuid4())
    print(f"Session ID: {session_id}")
    
    # Load chat history if it exists (not implemented - would need DB)
    chat_history: List[BaseMessage] = []
    
    if args.query:
        human_message = HumanMessage(content=args.query)
        chat_history.append(human_message)
        
        result, chat_history = run_agent(args.query, chat_history)
        display_message(chat_history[-1])
    else:
        print("🤖 LangGraph Agent with Ollama Qwen3")
        print("Type 'exit' or 'quit' to exit the program")
        print("-" * 80)
        
        while True:
            query = input("🧑 Enter your query: ")
            if query.lower() in ["exit", "quit"]:
                break
            
            human_message = HumanMessage(content=query)
            chat_history.append(human_message)
            
            result, chat_history = run_agent(query, chat_history)
            display_message(chat_history[-1])

if __name__ == "__main__":
    main()