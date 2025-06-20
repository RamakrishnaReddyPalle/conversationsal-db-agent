## 🧠 Conversational MongoDB Agent
---
This project allows natural language querying of a financial MongoDB database using a local LLM (e.g., Mistral-7B Instruct) and provides both:

* 🖥️ A REST API via **FastAPI**
* 💬 A chat-based UI via **Streamlit**

> Users can ask questions like:
> *"Show me all transactions over \$1000 in the last 7 days"*
> and get structured MongoDB queries, results, and a human-friendly summary.

---

## 📁 Project Structure

```bash
.
├── .env
├── Dockerfile
├── requirements.txt
├── frontend/
│   └── ui.py               # Streamlit UI app
├── src/
│   ├── agent/
│   │   ├── langchain_agent.py
│   │   ├── query_builder.py
│   │   ├── summarizer.py
│   ├── db/
│   │   └── query_executor.py
│   └── config/
│       └── config.py       # Loads Mongo URI and secrets
├── models/
│   └── mistral-7b-instruct-v0.2/  # Downloaded HuggingFace model folder
└── main.py                 # FastAPI backend entry
```

---

Here’s a clear and professional attribution statement for the **Kaggle financial dataset** you used earlier, which you can include in your `README.md`, documentation, or app footer:

---

## 📊 Dataset Attribution

This project utilizes a financial dataset originally sourced from [Kaggle](https://www.kaggle.com/) for demonstration and experimentation purposes.

**Dataset Title:** Huge Stock Market Dataset
**Source:** Kaggle Dataset URL - https://www.kaggle.com/datasets/borismarjanovic/price-volume-data-for-all-us-stocks-etfs/data

The dataset contains anonymized financial records including **stocks, ETFs**, and has been preprocessed to suit MongoDB storage and natural language querying tasks.

### 📦 MongoDB Sample Dataset

This project also uses the **`sample_analytics`** dataset provided by [MongoDB Atlas Sample Datasets](https://www.mongodb.com/docs/atlas/sample-data/).
It includes anonymized financial and customer analytics data, ideal for demonstrating aggregation pipelines and query generation tasks.

> ✅ All data is used under the terms of the Kaggle dataset's open license. Please refer to the [dataset page](https://www.kaggle.com/) for licensing and citation requirements.

---
## ⚙️ .env Setup
```ini
MONGO_USER=your_mongodb_user
MONGO_PASS=your_mongodb_password
DATABASE_NAME=sylvr_finance
```

---

## 🧪 Sample Prompts (Try these in UI)

| Natural Query                                           | Target Collection       |
| ------------------------------------------------------- | ----------------------- |
| Show me all transactions over \$1000 in the last 7 days | `transactions`          |
| List customers who opened accounts this year            | `customers`, `accounts` |
| What ETFs have gained over 5% this month?               | `ETFs`                  |
| Get accounts with balances above \$50,000               | `accounts`              |
| Which stocks were traded most in last 24h?              | `stocks`                |

---

## 🧠 Code Flow Overview

1. **Query is entered** (via Streamlit or `/query` API).
2. `query_builder.py`:

   * Converts natural language → MongoDB JSON query using local LLM.
3. `query_executor.py`:

   * Executes Mongo query on selected collection.
4. `summarizer.py`:

   * Summarizes the output using local LLM.
5. `langchain_agent.py`:

   * Coordinates single-shot and multi-turn chat workflows.
6. `ui.py`:

   * Renders full frontend chat interface using Streamlit.
7. `main.py`:

   * Runs FastAPI backend for programmatic access.

---

## 🔌 Run Locally Without Docker

### 1. Clone Repo & Install

```bash
git clone [https://github.com/yourname/mongo-conversational-agent.git](https://github.com/RamakrishnaReddyPalle/conversationsal-db-agent.git)
cd conversational-db-agent
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 2. Download the Model (One-Time)

```bash
from transformers import AutoModelForCausalLM, AutoTokenizer
AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2", cache_dir="models/mistral-7b-instruct-v0.2")
AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2", cache_dir="models/mistral-7b-instruct-v0.2")
```

OR download manually from [🤗 Hugging Face](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2) into `./models/mistral-7b-instruct-v0.2/`.

### 3. Start FastAPI Backend

```bash
uvicorn main:app --reload
```

You can now test via **Swagger UI**:

```
http://localhost:8000/docs
```

---

### 4. Start Streamlit Frontend

```bash
streamlit run frontend/ui.py
```

Visit:

```
http://localhost:8501
```

---

## 🐳 Docker Deployment

### 1. Build Docker Image

```bash
docker build -t mongo-agent .
```

### 2. Run Docker Container

```bash
docker run -d -p 8000:8000 --env-file .env mongo-agent
```

> Note: Streamlit must be run **outside** or in a separate container.

---

## 🌍 Swagger Test Guide

1. Go to: [http://localhost:8000/docs](http://localhost:8000/docs)
2. Use the `/query` endpoint with query param:

   ```
   natural_query = Show me all transactions over $1000 in the last 7 days
   ```
3. Check returned MongoDB query, results, and summary.
