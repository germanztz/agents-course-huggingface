"""Tool for executing bash commands."""

import subprocess
from typing import List, Optional
from pydantic import BaseModel, Field
from langchain_core.tools import tool

class BashCommandInput(BaseModel):
    """Input for bash command execution."""
    command: str = Field(..., description="Bash command to execute")
    timeout: Optional[int] = Field(default=60, description="Timeout in seconds for the command")

@tool
def execute_bash(command: str, timeout: int = 60) -> str:
    """
    Execute a bash command and return the output.
    
    Args:
        command: The bash command to execute
        timeout: Timeout in seconds (default: 60)
        
    Returns:
        Output of the command (stdout and stderr)
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
        
        # Prepare the output
        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        returncode = result.returncode
        
        output = f"Command: {command}\n"
        output += f"Return code: {returncode}\n\n"
        
        if stdout:
            output += f"STDOUT:\n{stdout}\n\n"
        
        if stderr:
            output += f"STDERR:\n{stderr}\n\n"
        
        return output
    except subprocess.TimeoutExpired:
        return f"Command timed out after {timeout} seconds: {command}"
    except Exception as e:
        return f"Error executing command: {str(e)}"