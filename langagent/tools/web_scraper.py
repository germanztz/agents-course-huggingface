"""Web scraping tool to extract content from web pages."""

import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from langchain_core.tools import tool

class WebScraperInput(BaseModel):
    """Input for web scraper."""
    url: str = Field(..., description="URL of the webpage to scrape")
    elements: Optional[str] = Field(
        default="p,h1,h2,h3,h4,h5,code,pre", 
        description="Comma-separated list of HTML elements to extract"
    )

@tool
def web_scrape(url: str, elements: str = "p,h1,h2,h3,h4,h5,code,pre") -> str:
    """
    Scrape the content from a webpage.
    
    Args:
        url: The URL of the webpage to scrape
        elements: Comma-separated list of HTML elements to extract (default: p,h1,h2,h3,h4,h5,code,pre)
        
    Returns:
        Extracted text content from the webpage
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract text from the specified elements
        element_list = elements.split(',')
        content = []
        
        for element_type in element_list:
            element_type = element_type.strip()
            for element in soup.find_all(element_type):
                text = element.get_text().strip()
                if text:
                    # Add element type as a prefix for context
                    content.append(f"[{element_type}] {text}")
        
        return "\n\n".join(content)
    except Exception as e:
        return f"Error scraping {url}: {str(e)}"