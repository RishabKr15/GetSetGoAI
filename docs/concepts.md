# 🧠 Core Agentic Concepts in GetSetGoAI

This project utilizes state-of-the-art AI orchestration to move beyond simple chat responses into a "Reasoning and Acting" (ReAct) paradigm.

## 1. LangGraph: Cognitive Orchestration
Unlike a linear script, **LangGraph** allows the agent to loop, branch, and backtrack.
- **Agent Node**: This is where the LLM (Large Language Model) processes the `SYSTEM_PROMPT` and user query. It generates a thought process and decides on a "Path".
- **Tools Node**: When the Agent decides it needs data (e.g., "What's the weather in Tokyo?"), the workflow switches to this node to execute Python functions.
- **Conditional Routing**: After every thought, the graph asks: *"Is the answer complete, or do I need more tool data?"* This cycle continues until a comprehensive plan is ready.

## 2. Advanced Tool Usage
The agent doesn't just "talk"; it "does".
- **Real-time Research**: Uses Tavily and SerpAPI to find actual hotel links and restaurant prices.
- **Currency Intelligence**: When a user selects a currency (e.g., INR), the agent is instructed via metadata to use the `convert_currency` tool to translate all discovered global prices into the preferred local currency.

## 3. Stateful Memory & Persistence
GetSetGoAI remembers the context of your trip across multiple messages.
- **Thread Management**: Each user session is tracked by a `thread_id`.
- **Checkpointing**: Every state of the conversation is saved. If the agent finds a hotel in message 1, and you ask "Is there a pool?" in message 2, it knows exactly which hotel you are talking about.

## 4. Dual-Interface Synergy
The core agent logic is decoupled from the UI.
- **FastAPI**: Serves as the "Logic API". It can power mobile apps, websites, or CLI tools.
- **Streamlit**: Provides a "Premium Visual Interface" that renders the agent's markdown output with high-end styling.

## 5. Structured Data Extraction
To provide a clean UX, the agent follows a mandatory output structure:
1. **Classical Plan**: The "safe" landmarks.
2. **Off-beat Plan**: The "hidden" gems.
This ensures the user always gets a diverse set of options.

---

### Workflow Visualization
```mermaid
graph TD
    START --> agent["Agent (Thinking)"]
    agent --> condition{Wants Tools?}
    condition -- Yes --> tools["Tools (Acting)"]
    tools --> agent
    condition -- No --> END
```
