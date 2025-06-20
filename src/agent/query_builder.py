import os
import re
import json
from dotenv import load_dotenv
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate
from llama_cpp import Llama

load_dotenv()

# LLM model path
MODEL_PATH = "./mode/mistral-7b-instruct-v0.2.Q4_K_M.gguf"
llm = Llama(model_path=MODEL_PATH, n_ctx=2048)

# Schema definition
response_schemas = [
    ResponseSchema(name="collection", description="MongoDB collection to query (choose one: stocks, ETFs, customers, accounts, transactions)"),
    ResponseSchema(name="query", description="MongoDB query as a Python dict, no formatting or extra explanation"),
]
parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = parser.get_format_instructions()

prompt_template = PromptTemplate(
    template="""
You are a MongoDB query generator. Given a natural language question, output only the MongoDB query in pure JSON format.

The response must be a single JSON object with exactly two keys:
- "collection": the MongoDB collection to query (strictly only from: stocks, ETFs, customers, accounts, transactions)
- "query": the MongoDB filter as a Python dictionary (no MongoDB-specific types like ISODate)

Rules:
- No explanation or extra output
- No markdown formatting
- No labels like "Answer:"
- Output only the pure JSON result for the current question
- Dates must be formatted as ISO 8601 strings

{format_instructions}

Question: {user_input}
""",
    input_variables=["user_input"],
    partial_variables={"format_instructions": format_instructions},
)

def clean_llm_response(text: str) -> str:
    text = re.sub(r'```|json|Answer:|Question:.*', '', text, flags=re.IGNORECASE).strip()
    text = re.sub(r'ISODate\("([^"]+)"\)', r'"\1"', text)
    start_idx = text.find('{')
    end_idx = text.rfind('}') + 1
    return text[start_idx:end_idx] if start_idx >= 0 and end_idx > start_idx else text

def build_query_from_natural_language(user_input: str):
    prompt = prompt_template.format(user_input=user_input)
    output = llm(prompt, max_tokens=300)
    raw = output["choices"][0]["text"]

    print("=== RAW LLM RESPONSE ===")
    print(raw)

    try:
        cleaned = clean_llm_response(raw)
        parsed = parser.parse(cleaned)
        collection = parsed["collection"].strip().lower()
        query = parsed["query"]
        return collection, query
    except Exception as e:
        raise ValueError(f"JSON parsing failed: {e}\nCleaned response:\n{cleaned[:300]}...")

# Test
if __name__ == "__main__":
    q = "Show me all transactions over $1000 in the last 7 days"
    print(build_query_from_natural_language(q))
