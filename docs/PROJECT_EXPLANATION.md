# ✈️ GetSetGoAI: Project Deep Dive & Technical Walkthrough

This document provides a comprehensive, start-to-finish explanation of the **GetSetGoAI** project. It is designed to prepare you to present, explain, or deliver the project with full technical and conceptual clarity.

---

## 1. The Vision: Why GetSetGoAI?

In the current travel landscape, planning a trip usually involves hopping between 10 different tabs: Google Maps, TripAdvisor, Weather.com, currency converters, and hotel booking sites. It's fragmented and exhausting.

**GetSetGoAI** solves this by introducing an **"Agentic Concierge"**. 
- It doesn't just "chat"; it **reasons**.
- It doesn't "hallucinate" prices; it **researches** them.
- It delivers a **premium, data-driven itinerary** with financial intelligence and live logistics in a single, beautiful interface.

---

## 2. Technical Architecture: The Engine Under the Hood

GetSetGoAI is built on a modern, decoupled architecture:

### 🧠 The Brain: Reactive Agentic Workflow (LangGraph)
The core intelligence resides in `Agent/agentic_workflow.py`. We use **LangGraph** to build a **Stateful, Non-Blocking Multi-Agent System**.
- **Efficient Resource Utilization**: The entire workflow is built on a non-blocking I/O paradigm. This ensures that even when the agent is conducting deep research across multiple APIs, the server remains responsive and can handle other concurrent users.
- **State Machine**: The agent enters a reasoning cycle where it decides which tool to use next based on the user's progress.
- **Persistence**: Using `MemorySaver`, the agent remembers trip context (like traveler count or preferred currency) across multiple chat turns.

### 🛠️ The Toolkit: Specialized Tools
The agent has access to a variety of specialized tools located in the `tools/` directory:
- **Location Explorer**: Uses **SerpAPI** and **Tavily** for real-time web lookups (hotels, attractions, restaurants).
- **Meteorologist**: Fetches live weather and 5-day forecasts via OpenWeatherMap.
- **Accountant**: Performs precise arithmetic for daily budgets and total costs.
- **Forex Bureau**: Real-time currency conversion for global travelers.

### 🌐 The Backbone: High-Performance REST Gateway
The backend (in `main.py`) provides a robust RESTful API leveraging non-blocking communication for external services. This ensures high throughput and scalability, making the project production-ready for cloud environments like Render.

### 🎨 The Interface: Streamlit Premium
The frontend (in `streamlit_app.py`) isn't a standard Streamlit app. It uses **Custom CSS** to create a **Glassmorphic, Dark-Themed UI** that feels premium and high-end, matching the "Elite Concierge" branding.

---

## 3. Core Concepts & Innovations

### ☯️ The Duality Strategy: Classic vs. Off-Beat
A signature feature of GetSetGoAI is that it *always* generates two distinct paths:
1. **The Classic Route**: For the first-timer who wants to see the Eiffel Tower and the Louvre.
2. **The Off-Beat Path**: For the seasoned traveler looking for hidden cafes in Le Marais or secret gardens in the 11th arrondissement.

### 💵 Dynamic Financial Intelligence
Most AI planners give vague estimates. GetSetGoAI uses its **Currency Converter** and **Expense Calculator** to provide:
- Line-item budget breakdowns.
- Conversions into the user's preferred currency (INR, USD, EUR, etc.).
- Proactive price adjustments based on the number of travelers.

### 🔑 "Bring Your Own Key" (BYOK) Architecture
To address the costs of public deployments, we implemented a sophisticated BYOK model:
- **Dynamic Key Injection**: Users can input their own API keys in the Streamlit sidebar.
- **Session-Based Isolation**: These keys are passed through the FastAPI layer into the LangGraph state at runtime, allowing the agent to authenticate with specific providers (Google, Tavily, etc.) using the user's own account.
- **Privacy First**: User keys are stored purely in memory (`st.session_state`) and are never saved on the server.

### 🔍 Research over Hallucination
By mandating tool-use in the `SYSTEM_PROMPT`, we ensure the agent rarely "invents" names. It must find the entity via search tools before recommending it.

---

## 4. Code Highlight: How the Agent Thinks

In `Agent/agentic_workflow.py`, notice the `agent_function`:
- It **Sanitizes History**: Filters out technical glitches to keep the conversation clean.
- It **Extracts Structured Data**: Uses Regex to find JSON blocks within the LLM's response to provide metadata back to the UI.
- It **Handles Errors Gracefully**: If a tool fails, it provides a friendly, human-centric recovery message rather than a raw stack trace.

In `prompt_library/prompt.py`, the **System Message** acts as the "Constitution" for the agent, enforcing:
- Mandatory output structures.
- Use of Markdown links for credibility.
- Strict avoidance of technical "leaks" (like raw tool tags).

---

## 5. Ready-to-Deliver Script (Presenter's Guide)

*Use these talking points for a live demo or executive summary:*

> "Welcome to the future of travel. This is **GetSetGoAI**. 
> 
> Instead of a simple chat response, we've built a **Non-Blocking Reasoning Engine** powered by LangGraph. When you ask for a trip, the agent triggers a multi-phase research cycle that is designed for high concurrency, allowing for massive performance and scalability.
> 
> What sets us apart is our **BYOK (Bring Your Own Key) Architecture**. We've solved the cost-to-scale problem by allowing visitors to use their own API credentials directly in the interface. 
> 
> The agent looks at live weather, searches for real hotels via Google and Tavily, and calculates your budget in your home currency. We provide a unique **Dual-Path Strategy**—giving you both the 'Top-Hits' and the 'Local Secrets'.
> 
> Technically, it's a decoupled stack: a high-throughput backend and a premium, glassmorphic Streamlit frontend. It's not just a demo; it's a scalable, production-ready AI concierge.
> 
> That is GetSetGoAI: Elite Intelligence for Elite Travelers."

---

## 6. Future Roadmap
- **Image Generation**: Integration with DALL-E/Midjourney for visual itineraries.
- **Booking Integration**: Direct deep-linking to flight and hotel booking engines.
- **Flight Tracking**: Real-time flight status and gate notification agents.

---
**Developed by [Rishabh Kumar](https://github.com/RishabKr15)**
© 2026 GetSetGoAI Project.
