# 💬 Chat with Ollama - Local LLM Chat UI (Streamlit)

This is a lightweight **chat UI built using Streamlit** that lets you chat with **local LLM models** running via [Ollama](https://ollama.com/). It supports multiple models like `mistral`, `llama3`, `sqlcoder:15b`, and `deepseek-coder-v2`, and stores your chat history locally.

---

## 🚀 Features

- ✅ Chat with locally hosted Ollama models
- ✅ Support for multiple models via sidebar
- ✅ Persistent chat history saved in `chat_history.json`
- ✅ Start new chats and load previous ones anytime
- ✅ Simple UI built with Streamlit

---

## 🛠 Prerequisites

### 1. Install Python
Make sure Python 3.8+ is installed.  
Download from: https://www.python.org/downloads/

### 2. Install Ollama
Install Ollama to run LLM models locally:

bash
curl -fsSL https://ollama.com/install.sh | sh



**Pull LLM Models**
       ollama pull mistral:latest
       ollama pull deepseek-r1:latest
       ollama pull deepseek-r1:7b

       
**Create Virtual env**


    python -m venv venv


**Activate Virtual env**


    venv\Scripts\activate


**Install Required Packages**


       pip install ollama streamlit requests



On Windows, download and install via https://ollama.com/download

Then pull models like:

ollama pull mistral
ollama pull llama3
ollama pull sqlcoder:15b
ollama pull deepseek-coder-v2



Install Python dependencies:


pip install streamlit requests




▶️ Running the App
Start Ollama (if not already running):

ollama serve

Start the Streamlit app:


streamlit run chat_ui.py

 check  this port
 Local URL: http://localhost:8501


