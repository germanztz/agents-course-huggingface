# LangGraph Agent with Ollama Qwen3 (LangAgent)

LangAgent implements an agentic system using LangGraph, local Ollama's Qwen3 model, and various tools for web searching, web scraping, file operations, and bash command execution.

The goal of LangAgent is to create an execution plan, store it in a yaml file, execute the plan task by task and step by step, test and check every task, and check the results. 

In order to achieve this, LangAgent uses LangGraph's planning capabilities to create a plan based on user input. The plan is then stored in a yaml file and executed step-by-step.

If the file already exists, LangAgent has to determine the status of every task and continue executing the tasks until all steps are completed.

The user is able to modify the `langagent.yaml` file manually if needed. Running again LangAgent over this file will continue executing the tasks from where it left off.

## Workflow logic

1. **Creation of a new project**: The user invoques LangAgent by providing a prompt with a first aproach of what they want, for example: "`Create an application that generates an status report of a project based on documents of a folder`".
2. **Deep dive**: LangAgent generates a list and description of the key elements and modules needed to achieve the goal. Also a list of alternetives or questions about the architecture, platform, scope, requeriments, etc. LangAgent also suggests a summary of the project. For example: Key modules needed: `Data collection`, `Report generation`, `Document parsing`, etc., Alternatives: `Use a database to store data`, `Use an API to fetch data`. Examples of questions: `Will the app be running locally?`, `The report has to be sended via email?`
4. **ask questions to clarify the plan**: Present the alternatives to chose the architecture, platform, scope, requeriments, etc. and questions to clarify the plan and register the answers of the user, then redefine the summary and the modules and the plan with the final information.
3. **Research**: For each module and feature LangAgent will search in internet to find documentation about libraries needed and existing examples. LangAgent will digest and embed this information in a vector db stores in the project and generate a detailed plan for each task based on this information. for example: "For the module `Data collection`, create a function to read data from a CSV file and store it in a database. use the library `pandas` to read the CSV file and the library `sqlite3` to store the data in a database. The function should return a dictionary with the data stored in the database." 
6. **Project plan**: LangAgent creates a plan in a file and executes it step-by-step. The plan is stored in a yaml file named `langagent.yaml` with the following seccions:

- **Project Name**: The name of the project, for example: `Project001`
- **Description**: A brief description of the project, based on user input
- **Features**: A list of features that the project will have, for example: `Features: Data collection, Report generation`
- **Requested Tools/Libraries**: A list of tools, libraries, or frameworks that are required for the project, for example: `Requested Tools/Libraries: Pandas, Matplotlib, Flask`
- **Modules**: A list of modules that will be implemented in the project
  - **Module Name**: The name of the module, for example: `Report generation`
  - **Module Description**: A Complete description of the module, for example: "This module will be responsible for generating reports based on the data collected by the `Data collection` module."
  - **Features**: A list of features that the module will have, for example: `Features: Report generation`
- **Execution Plan**: A detailed plan of tasks to be executed, each task with its own description and dependencies
  - **Task ID**: A unique identifier for each task, For example: `Task001`
  - **Task name**: The name of the task, For example: `Task001: Generate a report`
  - **Description**: A detailed description of the task, For example: "For the module `Data collection`, create a function to read data from a CSV file and store it in a database. use the library `pandas` to read the CSV file and the library `sqlite3` to store the data in a database. The function should return a dictionary with the data stored in the database."
  - **Module**: The module that will be implemented by solving this task, For example: `Module: Report generation`
  - **Output**: Description of the desired output of the task, file format, or any other relevant information, For example: "`Output: File,  Format: PDF Named 'report.pdf'`
  - **Dependencies**: A list of previous tasks that must be completed before this task can be executed, for example: `Dependencies: Task002, Task003`
  - **Status**: The current status of the task, either "Pending", "In Progress", or "Completed", for example: "`Status: In Progress`"
  - **Tools**: A list of tools used by the IA agents to complete the task, if any,  For example: `Tools: web_search`, `web_scraping`, `file_operations`, `bash_command_execution`
  - **Task validation**: A set of rules or criteria that must be met before a task can be considered complete, for example: `Validation: All required files are present and formatted correctly`

- **Project structure**: Tree list of all directories and files in the project, and a brief description of each directory or file, For example: `Project001/main.py - Main entry point of Project001`

7. **Analice current status**: 

- Read all the files in the project directory, including `langagent.yaml`, and analyze their contents to determine the current status of each task.
- Read the project plan file `langagent.yaml` carefully and make sure you understand all the tasks, dependencies, and tools required to complete the project.
- Run the test cases provided in the project plan file to ensure that all tasks are implemented correctly.
- Update the status of each task based on your analysis and test results.

8. **Execute the plan**: 

- Create new AI agents for each task listed in the project plan file, following the guidelines provided in the project plan.
- Test each AI agent to ensure that it can complete the task as specified in the project plan.
- Update the status of each task based on your analysis and test results.

## Features

- **Web Search**: Search the web for documentation using DuckDuckGo
- **Web Scraping**: Extract and process information from web pages
- **File Operations**: Create and modify files with code and data
- **Bash Command Execution**: Run Ubuntu bash commands to interact with LangAgent

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




