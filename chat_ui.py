import os
import json
import streamlit as st
import requests
from datetime import datetime

HISTORY_FILE = "chat_history.json"

# ---- Load & Save Functions ----
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_history(sessions):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(sessions, f, ensure_ascii=False, indent=2)

# ---- App UI Setup ----
st.set_page_config(page_title="Chat with Ollama", page_icon="💬")
st.title("💬 Chat with Ollama")
st.markdown("Chat with models like **Mistral**, **SQLCoder**, or **DeepSeek-Coder** running locally via Ollama.")

# ---- Initialize Session State ----
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = load_history()

if "selected_chat_index" not in st.session_state:
    st.session_state.selected_chat_index = None

if "model" not in st.session_state:
    st.session_state.model = "deepseek-coder-v2:latest"

# ---- Sidebar with Model Selector and Chat History ----
with st.sidebar:
    st.header("⚙️ Model")
    st.session_state.model = st.selectbox(
        "Choose Ollama Model",
        ["mistral", "llama3", "sqlcoder:15b", "deepseek-coder-v2:latest"],
        index=["mistral", "llama3", "sqlcoder:15b", "deepseek-coder-v2:latest"].index(st.session_state.model)
    )

    st.markdown("---")
    st.subheader("📁 Chat History")

    # List past saved chat sessions
    for i, session in enumerate(st.session_state.chat_sessions):
        title = session["title"]
        timestamp = session["timestamp"]
        if st.button(f"🗂 {title} ({timestamp})", key=f"chat_{i}"):
            st.session_state.messages = session["messages"]
            st.session_state.selected_chat_index = i

    # New Chat Button
    st.markdown("---")
    if st.button("➕ New Chat"):
        if st.session_state.messages:
            # Get title from first user message
            user_msg = next((msg for msg in st.session_state.messages if msg["role"] == "user"), None)
            title = user_msg["content"][:30] + "..." if user_msg else "Untitled Chat"

            # Save current chat
            st.session_state.chat_sessions.append({
                "title": title,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "messages": st.session_state.messages.copy()
            })
            save_history(st.session_state.chat_sessions)

        # Start new chat
        st.session_state.messages = []
        st.session_state.selected_chat_index = None

# ---- Function to Get Response from Ollama ----
def generate_response(prompt, model):
    url = 'http://localhost:11434/api/generate'
    headers = {'Content-Type': 'application/json'}
    payload = {
        'model': model,
        'prompt': prompt,
        'stream': False
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json().get("response", "").strip()
        else:
            return f"❌ Error: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        return f"❌ Connection Error: {e}"

# ---- Display Chat in Main Area ----
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---- User Input + Generate Response ----
user_prompt = st.chat_input("Type your message here...")

if user_prompt:
    # Show and store user message
    st.chat_message("user").markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    # Get and show assistant's response
    assistant_response = generate_response(user_prompt, st.session_state.model)
    st.chat_message("assistant").markdown(assistant_response)
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
