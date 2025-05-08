# LangAgent
### LangGraph Agent with Ollama model 

LangAgent is a local-first autonomous system designed to streamline software project execution. It leverages LangGraph for orchestrating agent workflows and Ollama's local language models to understand, plan, and implement user-defined software tasks. LangAgent transforms natural language prompts into structured execution plans, documents the development process, and performs tasks in a modular and verifiable way.

The system uses stateful agent collaboration to ensure clarity, traceability, and reproducibility. LangAgent operates through the command line interface (CLI), emphasizing transparency and user control in a single-user environment.

## Agents

### 1. Manager

The Manager is responsible for managing the execution of tasks by LangAgent. It receives the prompt from the user and then engages in a conversation with the user to gather all the necessary details about the project. The plan is then executed step-by-step by LangAgent. The Manager also provides feedback on the progress of the task execution and allows the user to modify the plan if needed. Once all the tasks are completed, the Manager generates a final report and sends it back to the user.

- Understands the user’s request.
- **Deep dive**: Checks with the user for confirmation and clarification.
- Assigns the Analyst Agent to analyze the request.
- Starts the execution graph.
- Produces documentation:
    - `README.md`
- Tools:
  - `file operations`: File operations such as list, reading, writing, deleting, etc.

### 2. Analist

The Analyst Agent is responsible for analyzing the requirements and scope of the project, identifying potential issues, and suggesting solutions. It also helps in defining the architecture and platform of the project.

- **Understand the project**: The Analyst Agent reads the `README.md` file and analyzes its content, identifying potential issues and suggesting solutions.
- **Research**: For each feature will search in internet to find documentation about libraries needed and existing examples. will digest and embed this information obtained in the internet in a vector db stores inside the project. This documentation about tools, libraries, tools, etc. will be used by the `PM` for further analysis and for the `Developer`.
- **Ask for clarification**: Present the alternatives to chose the architecture, platform, scope, requeriments, etc. and the questions to clarify the plan and register the answers of the user, then redefine the summary and the moduleswith the final information.
Then, generates a list and description of the key elements and modules needed to achieve the goal. Also a list of alternetives or questions about the architecture, platform, scope, requeriments, etc. the agent also suggests a summary of the project. 
Key modules needed: `Data collection`, `Report generation`, `Document parsing`, etc., Alternatives: `Use a database to store data`, `Use an API to fetch data`.
- **Project structure**: The Analyst creates a project structure based on the requirements and scope of the project. It also defines the architecture and platform of the project and stores that information in files.
- Produces documentation:
  - `docs/modules.md`: List of modules needed for the project.
  - `docs/architecture.md`: Description of the architecture of the project.
- Tools:
  - `file operations`: File operations such as list, reading, writing, deleting, etc.
  - `internet search`: Search for information online.
  - `web scraping`: Extract data from websites.


### 3. PM

The Project Manager is responsible for managing the project and ensuring that it meets the requirements. It will be responsible for creating a detailed plan.
The Project Manager will also be responsible for monitoring the progress of the project and reporting any issues or delays to the team.

- **Understand the project**: Read all the files in the project structure created by the other agents and extract a deep understanding of the meaning, the goal, tools, needs, requeriments, structures, arquitecture, means etc of the project.
- **Project plan**: Based on the information extracted, create a detailed plan for the project. The plan should include all the necessary steps and tasks required to achieve the goal.
- **DoD**: Define the DoD (Definition of Done) for the project. This will include all the criteria that must be met to consider the tasks complete, depending on the type of project (e.g., software development, data analysis, etc.).; The tests specified in the documentation, etc. This section of the file will be used by the `Developer`.
- Produces documentation:
  - `docs/planing.md`: Detailed plan for the project.
- Tools:
  - `file operations`: File operations such as list, reading, writing, deleting, etc.


### 4. Developer

The Developer agent is responsible for implementing the tasks outlined in the project plan. They will work closely with the IA agents to ensure that all tasks are completed correctly and efficiently. They will also work closely with the IA agents to ensure that all tasks are completed correctly and efficiently. For every task the agent has to undertand the project as a whole defined in `Readme.md`, stick to the architecture defined on `docs/architecture.md`, the modules defined in `dosc/modules.md`, 

- **Understand the project**: The Developer agent should understand the project as a whole defined in `Readme.md`, stick to the architecture defined on `docs/architecture.md`, the modules defined in `dosc/modules.md`.
- **Undestand the task**: 
- **Implement the task**: Implement the task according to the requeriments specified in the task description, and the DoD section.
- **Test the task**: 
- **Update the status**: The Developer agent should update the status of each task based on their analysis and test results.

## LangAgent Workflow

1. **Definition**: The user invoques the `Manager` by providing a prompt with a first aproach of what they want, for example: "`Create an application that generates an status report of a project based on documents of a folder`".
1. **Deep dive**: the `Manager` has to figure out all the details of the project, in order to do that, it engages in a conversation with the user, asking them about the project's requirements, scope, and architecture. Until all the details are gathered or the user ask to stop asking, For example: `Will the app be running locally in a PC?`, `The report has to be sended via email?`. 
1. **Project details**: the `Manager` shows a sumary of the project and ask the user for confimation, then, stores in a file `README.md` the details of the project. This file will be used by th `Analist` and the `PM` for a deeply understanding of the project. The file needs to have the following structure:
1. **Call the analist**: The `Manager` then calls the analist and asigns the task of reading the README.md file
1. **Call the Project Manager**: The `Manager` then calls the `PM` and assigns the task of reading all the files and create a plan to implement the project.

1. **Read the README.md file**: The `Analyst` reads the README.md file and analyzes its content, identifying potential issues and suggesting solutions.
1. **Research**: For each module and feature The `Analyst` will search in internet to find documentation about libraries needed and existing examples. will digest and embed this information obtained in the internet in a vector db stores inside the project. This documentation about tools, libraries, tools, etc. will be used by the `PM` for further analysis and for the `Developer`.
1. **Ask for clarification**: Present the alternatives to chose the architecture, platform, scope, requeriments, etc. and the questions to clarify the plan and register the answers of the user, then redefine the summary and the modules and the plan with the final information.
Then, generates a list and description of the key elements and modules needed to achieve the goal. Also a list of alternetives or questions about the architecture, platform, scope, requeriments, etc. the agent also suggests a summary of the project. 
Key modules needed: `Data collection`, `Report generation`, `Document parsing`, etc., Alternatives: `Use a database to store data`, `Use an API to fetch data`.
1. **Project structure**: The `Analyst` creates a project structure based on the requirements and scope of the project. It also defines the architecture and platform of the project and stores that information in files.
  - **docs/modules.md**: This file lists all the modules that will be implemented in the project. contains the description of any part of the aplication.
  - **docs/architecture.md**: This file describes the architecture and platform of the project. this file needs to have this information:
1. **Read md files**: Read all the markdown files in the project directory created by the other agents and extract a deep understanding of the meaning, the goal, tools, needs, requeriments, structures, arquitecture, means etc of the project.
1. **Project plan**: Based on the information extracted from the markdown files, create a detailed plan for the project. The plan should include all the necessary steps and tasks required to achieve the goal. The plan is stored in a file named `planning.md` with the following seccions:
- **DoD**: Define the DoD (Definition of Done) for the project. This will include all the criteria that must be met to consider the project complete. This will include all the criteria that must be met to consider the project complete, depending on the type of project (e.g., software development, data analysis, etc.).; The tests specified in the documentation, etc. This section of the file will be used by the `Developer` to ensure thar every task is completed according to the DoD.
- **Execution Plan**: A detailed plan of tasks to be executed, each task with its own description and dependencies


## Files structure

### `README.md`

- **Project Name**: The name of the project, for example: `Enterprise reporter`
- **Description**: A detailed description of the project, it's scope, limitations, public, goals
- **Project files**: A list of files that will be used by the app, each file contains this information at least:
  - **Modules**: see file `docs/modules.md`
  - **Architecture**: @see file `docs/architecture.md`
  - **Planing**: see file `docs/planning.md`
- **Project structure**: Tree list of all directories and files in the project, and a brief description of each directory or file, For example: `docs/ - The documentation files are used to provide information about the project and its components.`

- **Features**: A list of features that the project will have, a feature is a requirement accepted by the user that the app will have to fulfill. each feature contains this information at least:
  - **Title**: The descriptive name of the feature, for example: `Data collection`
  - **Description**: A detailed description of this feature, it's intended use, for example: `Collect all the data from different sources and store it in a centralized database`

### `docs/modules.md`

This file lists all the modules that will be implemented in the project. contains the description of any part of the aplication.
- **Module name**: The name of the module, for example: `Data collection`
- **Description**: A detailed description of this module, it's intended use, for example: `Collect all the data from different sources and store it in a centralized database`
- **Dependencies**: A list of dependencies that the module will have, for example: `pandas`, `numpy`, matplotlib, etc.

### `docs/architecture.md`

This file describes the architecture and platform of the project. this file needs to have this information:

- **platform**: such as Linux, Windows, Docker, Kubernetes, AWS, Azure, etc.
- **programming language**: such as Python, Java, C++, etc.
- **frameworks**: such as Django, Flask, Express.js, etc.
- **libraries**: such as pandas, numpy, matplotlib, etc.
- **tools**: such as Jupyter Notebook, VSCode, PyCharm, etc.
- **sub-systems**: such as mySQL, RabbitMQ,
- **networks**: such as HTTP, HTTPS, WebSocket, etc.
- **persistence**: such as S3, SQLite, MongoDB, PostgreSQL, etc.
- **security**: such as authentication, encryption, etc.
- **deployment**: such as Docker, Kubernetes, AWS, Azure,  etc.
- **testing**: such as unit tests, integration tests, etc.
- **Backup and recovery**: such as backups, restores, disaster recovery, etc.

### `docs/planning.md`

A detailed plan of tasks to be executed, each task with its own description and dependencies

- **Task ID**: A unique identifier for each task, For example: `Task001`
- **Task name**: The name of the task, For example: `Task001: Generate a report`
- **Description**: A detailed description of the task, For example: "For the module `Data collection`, create a function to read data from a CSV file and store it in a database. use the library `pandas` to read the CSV file and the library `sqlite3` to store the data in a database. The function should return a dictionary with the data stored in the database."
- **Module**: The module in `docs/modules.md` that will be implemented by solving this task, For example: `Module: Report generation`
- **Output**: Description of the desired output of the task, file format, or any other relevant information, For example: "`Output: File,  Format: PDF Named 'report.pdf'`
- **Dependencies**: A list of previous tasks that must be completed before this task can be executed, for example: `Dependencies: Task002, Task003`
- **Status**: The current status of the task, either "Pending", "In Progress", or "Completed", for example: "`Status: In Progress`"
- **Tools**: A list of tools used by the IA agents to complete the task, if any,  For example: `Tools: web_search`, `web_scraping`, `file_operations`, `bash_command_execution`
- **Task validation**: A set of rules or criteria that must be met before a task can be considered complete, for example: `Validation: All required files are present and formatted correctly`
