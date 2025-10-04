import subprocess
from langchain_core.tools import tool


@tool
def execute_bash(command: str, timeout: int = 60) -> str:
    """
    Execute a bash command and return the output.
    
    Args:
        command: The bash command to execute
        timeout: Timeout in seconds (default: 60)
        
    Returns:
        Output object of the command 
        {
            "command": string,
            "return code": int,
            "stdout": string,
            "stderr": string,
        }
    """
    try:
        # Run the command
        result = subprocess.run(
            command,
            shell=True,
            timeout=timeout,
            capture_output=True,
            text=True
        )
                
        return {
            "command": command,
            "return code": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
        }

    except subprocess.TimeoutExpired:
        return {
            "command": command,
            "return code": -1,
            "stdout": None,
            "stderr": f"Error executing command: Command timed out after {timeout} seconds",
        }
    except Exception as e:
        return {
            "command": command,
            "return code": -1,
            "stdout": None,
            "stderr": f"Error executing command: {str(e)}",
        }
