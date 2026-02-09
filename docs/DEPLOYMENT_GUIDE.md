# 🚀 GetSetGoAI Deployment & Subscription Guide

This guide covers everything you need to know to take **GetSetGoAI** from your local machine to the cloud. It includes hosting options, required subscriptions, and the detailed deployment process.

---

## 1. Hosting Options: Where to Deploy?

Since the project has two parts (FastAPI Backend & Streamlit Frontend), you have a few excellent options:

### Option A: One-Click Deploy (Render Blueprint) - *Recommended*
Deploy both services automatically using our Blueprint. Rent will prompt you for all API keys during setup.
- **[Click here to Deploy](https://render.com/deploy?repo=https://github.com/RishabKr15/GetSetGoAI)**

### Option B: Manual Frontend & Backend
Deploy separately if you need custom configurations for each.

### Option B: The "Hybrid" Approach
- **Frontend**: Use **Streamlit Community Cloud** (Free). It's designed specifically for Streamlit apps.
- **Backend**: Use **Render** or **Railway** for the FastAPI server.

> [!TIP]
> **Host for $0/mo with BYOK!**
> Thanks to our **Bring Your Own Key** architecture, you can deploy the app to the cloud without even having your own API keys configured on the server. Visitors will use their own keys via the UI sidebar, meaning you incur zero API usage charges.

---

## 2. Required Subscriptions & API Costs

To run the project in production, you'll need the following API keys. Most offer a generous "Free Tier" to get started:

| Service | Purpose | Free Tier | Paid Tier Starts At |
| :--- | :--- | :--- | :--- |
| **Google AI (Gemini)** | LLM / The Brain | ~15 RPM (Free) | Pay-as-you-go |
| **Tavily Research** | Real-time Search | 1,000 searches/mo | $20/mo |
| **SerpAPI** | Google Search Results | 100 searches/mo | $50/mo |
| **OpenWeatherMap** | Live Weather Data | 1,000 calls/day | $0.15 per 100 calls |
| **ExchangeRate-API** | Currency Conversion | 1,500 requests/mo| $10/mo |

> [!NOTE]
> For a personal project or small demo, the **Free Tiers** are usually more than enough.

---

## 3. The Deployment Process (Step-by-Step)

### Step 1: Prepare Your Repository
Ensure your project is on GitHub. Your repository should have:
- `requirements.txt` or `pyproject.toml` (for dependencies).
- `setup.py` (to make the project installable).
- A clean structure without `.env` files (these will be added to the cloud).

### Step 4: Deploy the FastAPI Backend
1. **Source**: Connect your GitHub repo to Render.
2. **Build Command**: `pip install -r requirements.txt && pip install .`
3. **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 8000`
4. **Environment Variables**: Add all keys (`GOOGLE_API_KEY`, `TAVILY_API_KEY`, etc.). Render will use these to authenticate with the LLM and search tools.

### Step 5: Deploy the Streamlit Frontend
1. **Source**: Connect your GitHub repo.
2. **Build Command**: `pip install -r requirements.txt`
3. **Start Command**: `streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0`
4. **Environment Variables**: 
   - `BACKEND_URL`: Set this to your Backend's **external** URL (e.g., `https://getsetgo-api.onrender.com`).

---

## 4. Docker-Based Deployment (Modern Approach)

If you have Docker installed, you can skip manual environment setup and run everything with a single command. 

### Why Use Docker?
- **Consistency**: The app works exactly the same on Windows, Mac, or Linux.
- **Isolation**: Dependencies don't interfere with your system Python.
- **Speed**: One command to start both Backend and Frontend.

### How to Run via Docker Compose
1. Ensure you have your `.env` file ready with all API keys.
2. Open your terminal in the project root.
3. Run:
   ```bash
   docker-compose up --build
   ```
4. Access the UI at `http://localhost:8501`.

---

## 5. Professional Tools & Services

### 🐳 Docker (Optional but Recommended)
Using Docker ensures your app runs exactly the same in the cloud as it does on your laptop.
- Create a `Dockerfile` for each service.
- Use `docker-compose` to run them together locally before pushing to the cloud.

### 🗄️ Database (For High Performance)
Currently, the app uses in-memory memory (`MemorySaver`). For a production app that remembers users forever, consider:
- **Upstash Redis**: Great for serverless memory.
- **Postgres (via Supabase or Neon)**: The professional choice for LangGraph persistence.

---

## 5. Summary Checklist for Success
1. [ ] Push code to GitHub.
2. [ ] Collect all API keys.
3. [ ] Deploy Backend first (get its URL).
4. [ ] Deploy Frontend second (using the Backend URL).
5. [ ] Perform a live test!

---
**GetSetGoAI Deployment Team**
© 2026 Developed by **[Rishabh Kumar](https://github.com/RishabKr15)**.
