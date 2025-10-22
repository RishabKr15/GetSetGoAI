import streamlit as st
import datetime
import requests
import os
import sys

# Allow overriding the backend URL via env var to avoid IPv6/localhost resolution issues
# Default to IPv4 loopback which avoids some Windows IPv6 binding quirks
BASE_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

# Set page configuration
st.set_page_config(
    page_title="Travel Agent AI",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Page title
st.title("✈️ Travel Agent AI")

# Sidebar with information
with st.sidebar:
    st.header("About Travel Agent AI")
    st.write("""
        Ask about travel plans, destinations, or itineraries, and our AI will provide tailored suggestions.
    """)
    st.image("https://source.unsplash.com/300x200/?travel", caption="Explore the World")
    st.markdown("---")
    st.write(f"Current Time: {datetime.datetime.now().strftime('%H:%M, %d %b %Y')}")
    st.markdown("---")
    st.subheader("Debug")
    st.write("Python executable:")
    st.code(sys.executable)
    # Backend quick check button
    if st.button("Check backend connectivity"):
        try:
            r = requests.get(f"{BASE_URL}/docs", timeout=5)
            if r.status_code == 200:
                st.success(f"Backend reachable at {BASE_URL} (GET /docs returned 200)")
            else:
                st.error(f"Backend responded with status {r.status_code}")
        except Exception as e:
            st.error(f"Backend check failed: {e}")

# Main chat interface
st.header("Chat with Your Travel Assistant")

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Container for chat history
with st.container():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

# Form for user input
with st.form(key="query_form", clear_on_submit=True):
    user_input = st.text_input("Ask about your travel plans:", placeholder="E.g., Plan a trip to Paris")
    submit_button = st.form_submit_button("Send")

# Handle form submission
if submit_button and user_input.strip():
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Show a spinner while fetching the response
    with st.spinner("Getting your travel plan (this may take up to 2 minutes on first run)..."):
        try:
            # Send request to FastAPI endpoint
            response = requests.post(f"{BASE_URL}/query", json={"query": user_input}, timeout=120)
            response.raise_for_status()
            answer = response.json().get("answer", "No response received")

            # Add assistant response to session state
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except requests.RequestException as e:
            # Handle API errors and provide actionable hints
            hint = (
                f"Could not reach the backend at {BASE_URL}.\n"
                "Make sure the FastAPI server is running (see README: `uvicorn main:app --host 0.0.0.0 --port 8000 --reload`).\n"
                "If the server is running, try setting the BACKEND_URL environment variable to the proper host (e.g. http://127.0.0.1:8000) and restart Streamlit."
            )
            error_message = f"Error connecting to the server: {e}\n{hint}"
            st.session_state.messages.append({"role": "assistant", "content": error_message})
    
    # Rerun to update the UI
    st.rerun()