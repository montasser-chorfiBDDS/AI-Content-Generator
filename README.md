# AI Content Generator

Generate professional content for LinkedIn, Twitter/X, Email, Product Descriptions, and Blog Posts — powered by a local AI model (Qwen2-0.5B-Instruct). No API keys needed.

## Features

- **LinkedIn Post Generator** — Professional posts
- **Twitter/X Thread Generator** — Punchy tweets
- **Email Generator** — Formal & friendly emails
- **Product Description Generator** — Compelling copy
- **Blog Post Generator** — Titles, intros, hooks

## Stack

- **Backend:** FastAPI
- **Frontend:** Streamlit
- **LLM:** Qwen2-0.5B-Instruct (local, free via HuggingFace)
- **No API keys required**

## Quick Start

```bash
pip install -r requirements.txt

# Start backend
uvicorn main:app --host 0.0.0.0 --port 8000

# In another terminal, start frontend
streamlit run app.py
```

## Author

**Montasse Chorfi** — Master Big Data & Data Science
