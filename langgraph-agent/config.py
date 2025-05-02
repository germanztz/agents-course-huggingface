"""Configuration file for the LangGraph agent system."""

import os
from typing import Dict, Any, Optional
from pydantic import BaseModel

# Model configuration
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
MODEL_NAME = "qwen3"
TEMPERATURE = 0.1
MAX_TOKENS = 4096

# Agent configuration
DEFAULT_MAX_ITERATIONS = 15

# Web search configuration
SEARCH_RESULT_COUNT = 5

class AgentConfig(BaseModel):
    """Configuration for the agent system."""
    ollama_base_url: str = OLLAMA_BASE_URL
    model_name: str = MODEL_NAME
    temperature: float = TEMPERATURE
    max_tokens: int = MAX_TOKENS
    max_iterations: int = DEFAULT_MAX_ITERATIONS
    search_result_count: int = SEARCH_RESULT_COUNT