from langchain.agents import Tool, initialize_agent
from langchain_community.tools import tool
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.llms.base import LLM
from llama_cpp import Llama

from src.agent.query_builder import build_query_from_natural_language
from src.db.query_executor import execute_query
from src.agent.summarizer import summarize_results

# === Step 1: Local LLM Wrapper ===
class LocalLLM(LLM):
    def __init__(self, model_path="./mode/mistral-7b-instruct-v0.2.Q4_K_M.gguf", max_tokens=512):
        self.model = Llama(model_path=model_path, n_ctx=2048)
        self.max_tokens = max_tokens

    def _call(self, prompt: str, stop=None):
        output = self.model(prompt, max_tokens=self.max_tokens)
        return output["choices"][0]["text"].strip()

    @property
    def _llm_type(self):
        return "local-llama"

# === Step 2: Mongo Tool ===
@tool
def mongo_query_tool(input_text: str) -> str:
    """Query the financial MongoDB collections using natural language."""
    collection, query = build_query_from_natural_language(input_text)
    result = execute_query(collection, query)
    return str(result[:10])  # preview only

tools = [mongo_query_tool]

# === Step 3: Chat Agent ===
local_llm = LocalLLM()
memory = ConversationBufferMemory()
chat_agent = initialize_agent(
    tools=tools,
    llm=local_llm,
    agent="zero-shot-react-description",
    memory=memory,
    verbose=True
)

# === Step 4: Entry Function ===
def run_natural_language_query(user_input: str):
    """Single-shot natural language query (used outside the agent loop)."""
    collection, query = build_query_from_natural_language(user_input)
    print(f"Running on collection: {collection}")
    print(f"Query: {query}")
    results = execute_query(collection, query)
    summary = summarize_results(results, user_input)
    return {"collection": collection, "query": query, "results": results, "summary": summary}

def chat_with_agent(user_input: str):
    """Multi-turn conversational interaction using LangChain agent."""
    return chat_agent.run(user_input)
