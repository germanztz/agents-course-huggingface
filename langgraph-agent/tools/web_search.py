"""Web search tool using DuckDuckGo."""

from typing import List, Dict, Any, Optional
from duckduckgo_search import DDGS
from pydantic import BaseModel, Field
from langchain_core.tools import tool

from config import AgentConfig

config = AgentConfig()

class SearchInput(BaseModel):
    """Input for search query."""
    query: str = Field(..., description="The search query to use")
    num_results: Optional[int] = Field(default=5, description="Number of search results to return")

class SearchResult(BaseModel):
    """A single search result."""
    title: str
    link: str
    snippet: str

@tool
def web_search(query: str, num_results: int = config.search_result_count) -> List[Dict[str, str]]:
    """
    Search the web using DuckDuckGo for the given query.
    
    Args:
        query: The search query
        num_results: Number of results to return (default: 5)
        
    Returns:
        List of search results with title, link, and snippet
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=num_results))
            
        formatted_results = []
        for result in results:
            formatted_results.append({
                "title": result.get("title", ""),
                "link": result.get("href", ""),
                "snippet": result.get("body", "")
            })
        
        return formatted_results
    except Exception as e:
        return [{"title": f"Error in web search", "link": "", "snippet": f"Error: {str(e)}"}]