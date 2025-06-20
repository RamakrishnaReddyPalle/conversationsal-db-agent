# import os
# import json
# from langchain_openai import ChatOpenAI
# from langchain.output_parsers import StructuredOutputParser, ResponseSchema
# from langchain.prompts import PromptTemplate
# from dotenv import load_dotenv
# from langchain_huggingface import HuggingFaceEndpoint
# import re




# load_dotenv()

# # Define response schema
# response_schemas = [
#     ResponseSchema(name="collection", description="MongoDB collection to query (only from the following five: stocks, ETFs, customers, accounts, transactions)"),
#     ResponseSchema(name="query", description="MongoDB query as a pure Python dict without any additional statements")
# ]

# parser = StructuredOutputParser.from_response_schemas(response_schemas)
# format_instructions = parser.get_format_instructions()

# prompt_template = PromptTemplate(
#     template="""
# You are a MongoDB query generator. Given a natural language question, respond with ONLY the MongoDB query in valid JSON. 
# Your response must be a dictionary with two keys:
# - "collection": the name of the MongoDB collection
# - "query": the filter query to apply

# Do NOT include extra questions or examples. Do NOT add Markdown or `json` code blocks.

# Collections:
# - stocks
# - ETFs
# - customers
# - accounts
# - transactions

# Use only standard JSON — NO markdown, NO triple backticks, NO labels, NO "Answer:" prefix.

# {format_instructions}

# Question: {user_input}
# """,
#     input_variables=["user_input"],
#     partial_variables={"format_instructions": format_instructions},
# )




# llm = HuggingFaceEndpoint(
#     repo_id="HuggingFaceH4/zephyr-7b-beta",
#     huggingfacehub_api_token=os.environ["HUGGINGFACE_API_KEY"],
#     max_new_tokens=512,
#     temperature=0.01, 
# )


# def extract_first_valid_json(text: str) -> str:
#     """
#     Extract the first JSON block from LLM output (naive but effective).
#     """
#     matches = re.findall(r'\{(?:[^{}]|(?:\{[^{}]*\}))*\}', text)
#     if not matches:
#         raise ValueError("❌ No valid JSON block found.")
#     return matches[0]

# def build_query_from_natural_language(user_input: str):
#     prompt = prompt_template.format(user_input=user_input)
#     response = llm.invoke(prompt)
#     print("=== RAW LLM RESPONSE ===")
#     print(response)

#     try:
#         response_clean = extract_first_valid_json(response)
#         print("=== EXTRACTED FIRST JSON BLOCK ===")
#         print(response_clean)
#         parsed = json.loads(response_clean)
#         if "collection" not in parsed or "query" not in parsed:
#             raise ValueError(f"❌ Missing 'collection' or 'query' in response: {parsed}")

#         collection = parsed.get("collection", "").strip().lower()
#         query = parsed.get("query", {})
#         return collection, query

#     except Exception as e:
#         raise ValueError(f"❌ JSON parsing failed: {e}\nResponse: {response[:300]}...")  # Show only a preview



# if __name__ == "__main__":
#     user_question = "Show me all transactions over $1000 in the last 7 days"
#     collection, query = build_query_from_natural_language(user_question)
#     print("Collection:", collection)
#     print("MongoDB Query:", query)

import os
import json
from dotenv import load_dotenv
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint

load_dotenv()

# Define expected response schema
response_schemas = [
    ResponseSchema(
        name="collection",
        description="MongoDB collection to query (only from: stocks, ETFs, customers, accounts, transactions)"
    ),
    ResponseSchema(
        name="query",
        description="MongoDB query as a Python dict, without extra explanation or formatting"
    )
]

parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = parser.get_format_instructions()

# Define the prompt template
prompt_template = PromptTemplate(
    template="""
You are a MongoDB query generator. Given a natural language question, respond with ONLY the MongoDB query in valid JSON. 
Your response must be a dictionary with two keys:
- "collection": the name of the MongoDB collection
- "query": the filter query to apply

Do NOT include extra questions, examples, markdown, triple backticks, or explanation.

Valid Collections:
- stocks
- ETFs
- customers
- accounts
- transactions

{format_instructions}

Question: {user_input}
""",
    input_variables=["user_input"],
    partial_variables={"format_instructions": format_instructions},
)

# Initialize the LLM
llm = HuggingFaceEndpoint(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    huggingfacehub_api_token=os.environ["HUGGINGFACE_API_KEY"],
    max_new_tokens=512,
    temperature=0.01,
)

# Build MongoDB query from user natural language input
def build_query_from_natural_language(user_input: str):
    prompt = prompt_template.format(user_input=user_input)
    response = llm.invoke(prompt)
    
    print("=== RAW LLM RESPONSE ===")
    print(response)

    try:
        # Use the structured parser for clean, typed output
        parsed = parser.parse(response)
        collection = parsed["collection"].strip().lower()
        query = parsed["query"]
        return collection, query

    except Exception as e:
        raise ValueError(f"JSON parsing failed: {e}\nRaw LLM response:\n{response[:300]}...")

# Test block
if __name__ == "__main__":
    user_question = "Show me all transactions over $1000 in the last 7 days"
    collection, query = build_query_from_natural_language(user_question)
    print("Collection:", collection)
    print("MongoDB Query:", query)
