# LangGraph Agent with Ollama Qwen3

This project implements an agentic system using LangGraph, Ollama's Qwen3 model, and various tools for web searching, web scraping, file operations, and bash command execution.

## Features

- **Web Search**: Search the web for documentation using DuckDuckGo
- **Web Scraping**: Extract and process information from web pages
- **File Operations**: Create and modify files with code and data
- **Bash Command Execution**: Run Ubuntu bash commands to interact with the system

## Requirements

- Python 3.8+
- Ollama installed and running with the Qwen3 model
- Internet connection for web search and scraping

## Setup

1. **Install Ollama and Qwen3 model**:
   ```bash
   # Install Ollama (if not already installed)
   curl -fsSL https://ollama.com/install.sh | sh
   
   # Pull the Qwen3 model
   ollama pull qwen3
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command Line Mode

Run the agent with a specific query:

```bash
python main.py --query "How do I create a simple Flask application?"
```

### Interactive Mode

Run the agent in interactive mode for multiple queries:

```bash
python main.py --interactive
```

## Project Structure

- `config.py` - Configuration settings for the agent
- `main.py` - Main application entry point
- `modules/` - Core modules for the agent
  - `llm.py` - Interface to Ollama's Qwen3 model
  - `agent.py` - LangGraph agent implementation
- `tools/` - Tool implementations
  - `web_search.py` - DuckDuckGo web search tool
  - `web_scraper.py` - Web page scraping tool
  - `file_operations.py` - File reading and writing tools
  - `bash_executor.py` - Bash command execution tool

## Adding New Tools

To add a new tool:

1. Create a new Python file in the `tools/` directory
2. Implement the tool using the LangChain `@tool` decorator
3. Add the tool to the `get_tools()` function in `modules/agent.py`

## Example Tasks

- "Search for documentation on LangGraph and summarize the key concepts"
- "Create a simple Python script that uses the requests library to fetch data from an API"
- "Find and extract information about Docker containers and create a bash script to manage them"
- "Search for Flask tutorials, learn how to build a simple web app, and generate the code"

## License

MIT License
