import json
from llama_cpp import Llama

llm = Llama(model_path="./mode/mistral-7b-instruct-v0.2.Q4_K_M.gguf", n_ctx=2048)

def summarize_results(results: list, user_query: str) -> str:
    context = f"The user asked: '{user_query}'.\n\n"
    context += "Here are the top results from the database:\n"
    context += json.dumps(results[:5], indent=2)

    prompt = (
        f"{context}\n\n"
        "Based on these results, give a concise, user-friendly summary of the key findings in 2–3 sentences."
    )

    response = llm(prompt, max_tokens=250)
    return response["choices"][0]["text"].strip()
