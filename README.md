# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Common Development Commands

### Environment Setup
```powershell
# Install dependencies
pip install -e .
# Or using requirements.txt directly
pip install -r requirements.txt
```

### Running the Application
```powershell
# Start the FastAPI backend server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Start the Streamlit frontend (in a separate terminal)
streamlit run streamlit_app.py
```

### Development and Testing
```powershell
# Run a single test file
pytest tests/test_specific_file.py

# Run tests with verbose output
pytest -v

# Check code formatting
black . --check

# Format code
black .

# Install in editable mode for development
pip install -e .
```

## Architecture Overview

This is a **LangGraph-based AI Travel Agent** that provides comprehensive trip planning with real-time data integration. The application uses a multi-agent workflow architecture with specialized tools for different travel-related tasks.

### Core Architecture Components

**Agent Workflow System (`Agent/agentic_workflow.py`)**
- Built on LangGraph with StateGraph for workflow orchestration
- Uses MessagesState for maintaining conversation context
- Implements a reactive agent pattern with conditional edges between agent and tools
- Supports multiple LLM providers (DeepSeek, MistralAI) through configurable model loading

**Tool-Based Architecture**
The system uses specialized tool classes that follow a consistent pattern:
- Each tool class initializes its respective service and exposes LangChain @tool decorated functions
- Tools are aggregated in the GraphBuilder and bound to the LLM for function calling
- Tool categories: Weather (`weather_info_tool.py`), Location Search (`place_search_tool.py`), Currency Conversion (`currency_converter_tool.py`), Arithmetic Operations (`arithematic_operations_tool.py`)

**Multi-Interface Deployment**
- **FastAPI Backend** (`main.py`): REST API endpoint (`/query`) that accepts travel queries and returns structured responses
- **Streamlit Frontend** (`streamlit_app.py`): Interactive web UI with chat interface and session management
- Both interfaces communicate through the same GraphBuilder agent workflow

**Configuration Management**
- YAML-based configuration (`config/config.yaml`) for LLM provider settings
- Environment-based API key management through `.env` files
- Modular config loading through `utils/config_loader.py`

### Key Architectural Patterns

**Tool Integration Pattern**: Tools are self-contained classes that expose their functionality through LangChain tool decorators, making them easily discoverable and callable by the LLM agent.

**State Management**: Uses LangGraph's MessagesState for maintaining conversation history and context across tool calls and agent responses.

**Model Abstraction**: The `ModelLoader` class abstracts different LLM providers behind a common interface, allowing easy switching between DeepSeek and MistralAI models.

**Dual Interface Architecture**: The same agent workflow powers both programmatic API access (FastAPI) and user-friendly web interface (Streamlit), demonstrating separation of concerns.

## Project-Specific Guidelines

### Adding New Tools
1. Create a new tool class in `tools/` following the existing pattern
2. Implement `_setup_tools()` method returning a list of @tool decorated functions
3. Add the tool to `GraphBuilder` initialization and tool aggregation
4. Ensure proper error handling and API key management

### LLM Provider Configuration
- Add new providers in `utils/model_loaders.py` following the existing pattern
- Update `config/config.yaml` with provider-specific settings
- Ensure API keys are loaded from environment variables

### System Prompt Modifications
The travel agent behavior is controlled by `SYSTEM_PROMPT` in `prompt_library/prompt.py`. This defines the agent's persona and response format requirements (comprehensive travel plans with cost breakdowns, weather info, etc.).

### Graph Visualization
The system automatically generates Mermaid graph visualizations of the workflow when processing queries, saved as `graph.png` in the current working directory.