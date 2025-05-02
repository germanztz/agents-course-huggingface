"""Tools for file operations."""

import os
from typing import Optional
from pydantic import BaseModel, Field
from langchain_core.tools import tool

class FileWriteInput(BaseModel):
    """Input for writing to a file."""
    filepath: str = Field(..., description="Path to file")
    content: str = Field(..., description="Content to write to file")
    append: bool = Field(default=False, description="Whether to append to file or overwrite")

class FileReadInput(BaseModel):
    """Input for reading a file."""
    filepath: str = Field(..., description="Path to file")

@tool
def write_file(filepath: str, content: str, append: bool = False) -> str:
    """
    Write content to a file.
    
    Args:
        filepath: Path to the file to write
        content: Content to write to the file
        append: Whether to append to file (True) or overwrite (False)
        
    Returns:
        Status message
    """
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        
        mode = "a" if append else "w"
        with open(filepath, mode, encoding="utf-8") as f:
            f.write(content)
        
        return f"Successfully {'appended to' if append else 'wrote'} {filepath}"
    except Exception as e:
        return f"Error writing to {filepath}: {str(e)}"

@tool
def read_file(filepath: str) -> str:
    """
    Read content from a file.
    
    Args:
        filepath: Path to the file to read
        
    Returns:
        Content of the file
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        return content
    except Exception as e:
        return f"Error reading {filepath}: {str(e)}"