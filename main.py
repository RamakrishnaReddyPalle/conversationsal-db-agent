from fastapi import FastAPI
from src.agent.langchain_agent import run_natural_language_query

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to the Conversational DB API"}

@app.get("/query")
def query_db(natural_query: str):
    results = run_natural_language_query(natural_query)
    return {"results": results}
