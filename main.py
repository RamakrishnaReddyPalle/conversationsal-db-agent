from fastapi import FastAPI, Query
from pydantic import BaseModel

from src.agent.langchain_agent import (
    run_natural_language_query,
    chat_with_agent
)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to the Conversational DB API"}

# For one-shot, non-chat-based querying
@app.get("/query")
def query_db(natural_query: str = Query(..., description="User's natural language query")):
    results = run_natural_language_query(natural_query)
    return {"results": results}

# For conversational agent loop
@app.get("/chat_query")
def chat_db(natural_query: str = Query(..., description="Conversational query with memory")):
    response = chat_with_agent(natural_query)
    return {"response": response}
