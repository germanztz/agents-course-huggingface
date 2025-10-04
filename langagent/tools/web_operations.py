import requests
from bs4 import BeautifulSoup
from typing import Annotated, List, Dict, Any, Optional
from langchain_core.tools import tool

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


from langchain_community.document_loaders import WebBaseLoader
@tool
def scrape_webpages(urls: List[str]) -> str:
    """Use requests and bs4 to scrape the provided web pages for detailed information."""
    loader = WebBaseLoader(urls)
    docs = loader.load()
    return "\n\n".join(
        [
            f'<Document name="{doc.metadata.get("title", "")}">\n{doc.page_content}\n</Document>'
            for doc in docs
        ]
    )


from typing import List, Dict, Any, Optional
from duckduckgo_search import DDGS
from langchain_core.tools import tool
@tool
def web_search(query: str, num_results: int = 5) -> List[Dict[str, str]]:
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
            results = list(ddgs.text(query, max_results=num_results, backend='lite'))
            
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


from langchain_tavily import TavilySearch

tavily_tool = TavilySearch(max_results=5)