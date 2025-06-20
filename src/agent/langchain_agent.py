from langchain.agents import Tool, initialize_agent
from langchain_openai import ChatOpenAI
from langchain_community.tools import tool

from src.agent.query_builder import build_query_from_natural_language
from src.db.query_executor import execute_query

llm = ChatOpenAI(model="gpt-4", temperature=0)

@tool
def mongo_query_tool(input_text: str) -> str:
    """Query the financial MongoDB collections using natural language."""
    collection, query = build_query_from_natural_language(input_text)
    result = execute_query(collection, query)
    return str(result[:10])  # limit results in preview

tools = [mongo_query_tool]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True
)

def run_natural_language_query(user_input:str):
    collection, query = build_query_from_natural_language(user_input)
    print(f"Running on collection: {collection}")
    print(f"Query: {query}")
    results = execute_query(collection, query)
    return results
