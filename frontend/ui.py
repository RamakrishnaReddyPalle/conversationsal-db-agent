import streamlit as st
import datetime
import requests

# ------------------- Config -------------------
FASTAPI_URL = "http://localhost:8000"  # Adjust if running backend on another port or host

# ------------------- Session Initialization -------------------
def initialize_session_state():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "query_input" not in st.session_state:
        st.session_state.query_input = ""

initialize_session_state()

# ------------------- Page Setup -------------------
st.set_page_config(page_title="Conversational DB Agent", layout="wide")
st.title("💬 Conversational MongoDB Agent")

# ------------------- Sidebar Info -------------------
st.sidebar.title("📚 Sylvr Finance DB Info")
st.sidebar.markdown(
    """
    Query the **Sylvr Finance** MongoDB using natural language.

    **Collections available**:
    - `stocks`
    - `ETFs`
    - `customers`
    - `accounts`
    - `transactions`
    """
)

# ------------------- Display Chat History -------------------
def display_chat():
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["type"]):
            st.markdown(msg["content"])
            if msg.get("metadata"):
                if "timestamp" in msg["metadata"]:
                    st.caption(f"🕒 {msg['metadata']['timestamp']}")
                if "collection" in msg["metadata"]:
                    st.caption(f"📦 Collection: {msg['metadata']['collection']}")

# ------------------- Query Handler -------------------
def handle_user_query(user_input, chat_mode=False):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    st.session_state.chat_history.append({
        "type": "user",
        "content": user_input,
        "metadata": {"timestamp": timestamp}
    })

    try:
        endpoint = f"{FASTAPI_URL}/chat_query" if chat_mode else f"{FASTAPI_URL}/query"
        response = requests.get(endpoint, params={"natural_query": user_input})
        data = response.json()

        assistant_msg = f"✅ **Query Result Summary:**\n\n```\n{data.get('summary', 'No summary available')}\n```"
        st.session_state.chat_history.append({
            "type": "assistant",
            "content": assistant_msg,
            "metadata": {
                "timestamp": timestamp,
                "collection": data.get("collection", "N/A"),
                "status": "success"
            }
        })

    except Exception as e:
        st.session_state.chat_history.append({
            "type": "assistant",
            "content": f"❌ Error: {str(e)}",
            "metadata": {"timestamp": timestamp, "status": "error"}
        })

# ------------------- User Input -------------------
query = st.text_input("Ask a financial database question:", key="query_input")

col1, col2, col3 = st.columns(3)

if col1.button("💡 One-Shot Query", use_container_width=True):
    if query:
        handle_user_query(query, chat_mode=False)

if col2.button("🔁 Chat Mode (Memory)", use_container_width=True):
    if query:
        handle_user_query(query, chat_mode=True)

if col3.button("🧹 Clear Chat", use_container_width=True):
    st.session_state.chat_history = []
    st.rerun()

# ------------------- Show Chat -------------------
display_chat()
