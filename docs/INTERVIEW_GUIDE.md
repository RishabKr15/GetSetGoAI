# 🎙️ GetSetGoAI: Interview Preparation Guide

This guide is designed to help you explain the technical decisions, architecture, and "why" behind **GetSetGoAI** during professional interviews.

## 1. Project Overview
**What is GetSetGoAI?**
It's a premium, agentic travel concierge that doesn't just "search" but "plans." It uses dynamic AI agents to research flights, hotels, weather, and currency, providing a comprehensive, stateful travel itinerary.

## 2. Core Architecture
The project follows a modern, distributed architecture:
- **Frontend**: Streamlit (Reactive UI for fast prototyping and premium specialized widgets).
- **Backend**: FastAPI (Asynchronous, type-safe REST API).
- **Orchestration**: LangGraph (Stateful, multi-agent workflow management).
- **Persistence**: MemorySaver (Thread-safe state persistence).

## 3. High-Level Technical Decisions (The "Whys")

### 🚀 Why Non-Blocking I/O & `httpx`?
*   **The Problem**: Conventional `requests` is "blocking." If the AI is waiting for a weather API response, the entire server thread waits, unable to handle other users.
*   **The Solution**: We refactored the entire I/O layer to use a non-blocking architecture.
*   **Interview Answer**: *"I implemented a high-concurrency I/O architecture using FastAPI and httpx. This allows the server to handle a large volume of concurrent queries by yielding the event loop during external API calls, significantly improving throughput and resource efficiency."*

### 🧠 Why LangGraph?
*   **The Problem**: Simple LLM chains are linear and hard to debug when complexity grows.
*   **The Solution**: We used LangGraph to define the AI's behavior as a directed graph.
*   **Interview Answer**: *"I chose LangGraph for orchestration because it provides explicit control over state and loops. It allows the agent to 'think' and 're-evaluate'—for example, if a restaurant search fails, the agent can loop back and try a different strategy based on current state, which is much more robust than a simple linear chain."*

### 🐳 Why Docker & Render Blueprints?
*   **The Problem**: "It works on my machine" is a common deployment headache.
*   **The Solution**: Dockerized the services and created a `render.yaml` Blueprint.
*   **Interview Answer**: *"I automated the deployment using Render Blueprints to ensure Infrastructure as Code (IaC). This allows anyone to spin up the entire stack—Backend and Frontend—with a single click, with Render automatically prompting for the necessary environment secrets."*

### 🔑 Why Bring Your Own Key (BYOK)?
*   **The Problem**: Public deployment of LLM apps is expensive for the host.
*   **The Solution**: Implemented a multi-tenant session architecture where visitors provide their own keys in the UI.
*   **Interview Answer**: *"I designed a Bring Your Own Key (BYOK) architecture to solve the cost-scalability problem. By dynamically injecting user-provided keys from the Streamlit frontend into the LangGraph state at runtime, the application remains free for the host to maintain while remaining fully functional for visitors."*

## 4. Feature Highlights for Discussion
1.  **Tool-Augmented Generation**: The agent has real-time tools for Weather, Currency, and Web Search (Tavily/SerpAPI).
2.  **State Persistence**: Uses `thread_id` to maintain context across multiple user interactions.
3.  **Proactive Logic**: The agent doesn't just answer; it proactively converts currencies and checks weather based on the user's travel month.

## 5. Potential Follow-up Questions
*   **Q: How would you scale this for 1 million users?**
    *   *A: Switch from MemorySaver to Upstash Redis for distributed state, implement rate limiting at the FastAPI level, and use a load balancer for the backend services.*
*   **Q: Why use Google Gemini?**
    *   *A: It offers a massive context window (2M tokens) and excellent tool-calling performance at a lower cost-per-token compared to competitors.*

---
© 2026 Developed by **[Rishabh Kumar](https://github.com/RishabKr15)**. Prepared for Technical Excellence.
