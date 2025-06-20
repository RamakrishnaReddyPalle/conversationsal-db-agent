import streamlit as st
from src.agent.langchain_agent import run_natural_language_query

st.set_page_config(page_title="Conversational DB Agent", layout="wide")

st.title("💬 Conversational MongoDB Agent")

query = st.text_input("Ask your question (natural language):")

if query:
    with st.spinner("Processing your query..."):
        try:
            results = run_natural_language_query(query)
            st.success("Results:")
            st.json(results)
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
