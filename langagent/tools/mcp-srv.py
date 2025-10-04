from mcp.server.fastmcp import FastMCP
from langchain_core.tools import tool
from langchain_mcp_adapters.tools import to_fastmcp
from web_operations import web_scrape, web_search
from file_operations import read_file, write_file
from bash_executor import execute_bash

@tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

@tool()
def get_current_time():
    """Returns current system time in YYYY-MM-DD HH:MM:SS format."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

tools=[
    to_fastmcp(add), 
    to_fastmcp(multiply), 
    to_fastmcp(get_current_time),
    to_fastmcp(web_search),
    to_fastmcp(web_scrape),
    to_fastmcp(read_file),
    to_fastmcp(write_file),
    to_fastmcp(execute_bash),
    ]

mcp = FastMCP("mcp", tools=tools)

if __name__ == "__main__":
    mcp.run(transport="stdio")
    # print(web_search("Create custom components langflow"))
    # print(web_scrape("https://docs.langflow.org/components-custom-components"))
    # print(execute_bash("pwd"))