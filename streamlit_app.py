import streamlit as st
import datetime
import requests

BASE_URL = "http://localhost:8000"

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
    with st.spinner("Getting your travel plan..."):
        try:
            # Send request to FastAPI endpoint
            response = requests.post(f"{BASE_URL}/query", json={"query": user_input})
            response.raise_for_status()
            answer = response.json().get("answer", "No response received")
            
            # Add assistant response to session state
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except requests.RequestException as e:
            # Handle API errors
            error_message = f"Error connecting to the server: {e}"
            st.session_state.messages.append({"role": "assistant", "content": error_message})
    
    # Rerun to update the UI
    st.rerun()