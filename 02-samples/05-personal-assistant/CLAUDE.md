# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a personal assistant sample built with Strands Agents using a multi-agent architecture. The system demonstrates "agents as tools" functionality where specialized agents collaborate to handle different domains: calendar management, coding assistance, and web search.

## Development Commands

### Running Individual Agents
```bash
# Calendar Assistant
python -u calendar_assistant.py

# Coding Assistant  
python -u code_assistant.py

# Search Assistant (requires Docker)
python -u search_assistant.py

# Personal Assistant (multi-agent coordinator)
python -u personal_assistant.py
```

### Setup Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Set up virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Configure AWS credentials
aws configure
# OR export environment variables:
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1

# Set up Perplexity API for search functionality
export PERPLEXITY_API_KEY=your_perplexity_api_key
```

## Architecture

### Multi-Agent System
The project implements a hierarchical agent structure with the main coordinator (`personal_assistant.py`) orchestrating three specialized agents:

- **Calendar Assistant** (`calendar_assistant.py`): SQLite-backed appointment scheduling and management
- **Code Assistant** (`code_assistant.py`): Python REPL, file editing, shell access, and journaling capabilities  
- **Search Assistant** (`search_assistant.py`): Web search via Perplexity AI through MCP (Model Context Protocol)

### Agent-as-Tool Pattern
Each specialized agent is exposed as a `@tool` decorated function that can be called by the main personal assistant:

```python
@tool
def calendar_assistant(query: str) -> str:
    response = agent(query)
    return str(response)
```

This allows the main coordinator to delegate domain-specific tasks while maintaining conversational context.

### Model Configuration
All agents use AWS Bedrock with Claude Sonnet 4 via specific inference profile ARNs. The model configuration is consistent across agents for unified behavior.

### Tool Integration Architecture
- **Calendar Tools**: Modular SQLite-based functions in `calendar_tools/` directory (create, list, update, get agenda)
- **Coding Tools**: Leverages `strands_tools` package for REPL, editor, shell, and journal functionality
- **Search Tools**: MCP client connects to Docker-containerized Perplexity server with stdio communication
- **Shared State**: All agents use the same `SESSION_ID` from `constants.py` for tracing continuity

### Database Design
Calendar functionality uses SQLite (`appointments.db`) with schema: id (UUID), date (YYYY-MM-DD HH:MM), location, title, description. Tools handle table creation automatically and provide formatted output with appointment IDs for updates.

### MCP Integration Pattern
The search assistant initializes an MCP client that spawns a Docker container running the Perplexity server. The client maintains a persistent connection during the agent's lifecycle and requires proper cleanup on exit.

## Development Notes

### Interactive Loop Pattern
All agents follow a consistent structure:
- Rich welcome message with capability overview
- Input loop with graceful exit handling ("exit", "quit", "bye", "goodbye")
- Exception handling for KeyboardInterrupt and runtime errors
- Consistent emoji-based UI patterns for better user experience

### Environment Configuration
- `STRANDS_TOOL_CONSOLE_MODE="enabled"` enables rich UI for tools
- Search assistant requires Docker to be running for MCP server container
- Calendar data persists between sessions in local SQLite database

### Error Handling Patterns
Each agent implements comprehensive error handling for initialization failures, runtime exceptions, and user interrupts with informative error messages and recovery suggestions.