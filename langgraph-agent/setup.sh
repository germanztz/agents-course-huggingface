#!/bin/bash

# Setup script for the LangGraph Agent

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "Ollama is not installed. Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
    echo "Ollama installed successfully!"
else
    echo "Ollama is already installed."
fi

# Check if Qwen3 model is available
if ! ollama list | grep -q "qwen3"; then
    echo "Downloading Qwen3 model. This may take a while..."
    ollama pull qwen3
    echo "Qwen3 model downloaded successfully!"
else
    echo "Qwen3 model is already available."
fi

# Create a Python virtual environment
echo "Creating a Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install the required packages
echo "Installing required Python packages..."
pip install -r requirements.txt

# Test Ollama integration
echo "Testing Ollama integration..."
python test_ollama.py
if [ $? -eq 0 ]; then
    echo "Ollama integration test passed!"
else
    echo "Ollama integration test failed. Please check the error messages above."
    echo "You may need to ensure that Ollama is running: 'ollama serve'"
fi

echo "Setup completed!"
echo "To run the agent in interactive mode, use: python main.py --interactive"
echo "To run the agent with a specific query, use: python main.py --query 'your query here'"