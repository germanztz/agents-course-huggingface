"""LLM module for interacting with Ollama models."""

from typing import Dict, Any, List, Optional
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
# Updated import for ChatOllama
from langchain_ollama import ChatOllama

from config import AgentConfig

config = AgentConfig()

def get_ollama_llm() -> ChatOllama:
    """
    Initialize and return an Ollama Chat model instance.
    
    Returns:
        Configured ChatOllama instance
    """
    return ChatOllama(
        base_url=config.ollama_base_url,
        model=config.model_name,
        temperature=config.temperature,
        format="json",  # Helps with JSON formatting for tool calls
    )

def create_agent_prompt() -> ChatPromptTemplate:
    """
    Create the prompt template for the agent.
    
    Returns:
        ChatPromptTemplate for the agent
    """
    system_message = """You are an intelligent assistant that helps users accomplish tasks using tools.
You have access to the following tools:
1. Web search - Search the web for information
2. Web scraper - Extract content from web pages
3. File operations - Read and write files
4. Bash command execution - Run shell commands on the system

When using tools:
- Think carefully about which tool to use based on the task
- For complex tasks, break them down into smaller steps
- After learning from documentation, apply what you've learned to solve the problem
- Be specific with your commands and queries
- When writing code, ensure it's correct and follows best practices

When you need information, first search for relevant documentation, then scrape the results to learn about the topic.
When writing files, be precise about the filepath and content.
When executing commands, be careful with system modifications.

Think step-by-step and explain your reasoning.
"""
    
    # Create a structured ChatPromptTemplate for agent usage
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    return prompt