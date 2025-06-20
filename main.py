from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.agent.langchain_agent import run_natural_language_query, chat_with_agent

app = FastAPI()

# Allow Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to Streamlit host
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to the Conversational DB API"}

@app.get("/query")
def query_db(natural_query: str):
    results = run_natural_language_query(natural_query)
    return results

@app.get("/chat_query")
def chat_db(natural_query: str):
    response = chat_with_agent(natural_query)
    return {"response": response}
