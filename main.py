from __future__ import annotations

import json
import logging

from fastapi import FastAPI
from pydantic import BaseModel

from config import llm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Content Generator")


class ContentRequest(BaseModel):
    topic: str
    tone: str = "professional"
    language: str = "english"
    extra_info: str = ""


@app.get("/")
def root():
    return {"message": "AI Content Generator API", "status": "running"}


# Per-type settings: max tokens tuned to the format (faster + cheaper).
TYPE_CONFIG = {
    "linkedin": {"max_tokens": 400, "system": "You are a professional LinkedIn content writer. Create engaging, valuable posts."},
    "twitter":  {"max_tokens": 150, "system": "You are a viral Twitter/X content writer. Create ONE punchy tweet under 280 characters, or a short thread of max 3 tweets."},
    "email":    {"max_tokens": 400, "system": "You are a professional email copywriter. Write clear, concise, and effective emails."},
    "product":  {"max_tokens": 300, "system": "You are an expert product copywriter. Write compelling product descriptions that convert."},
    "blog":     {"max_tokens": 1024, "system": "You are a skilled blog writer. Create engaging blog intros, titles, and hooks."},
}

TASK_VERBS = {
    "linkedin": "Write a LinkedIn post about",
    "twitter": "Write a Twitter post or thread about",
    "email": "Write a professional email about",
    "product": "Write a product description for",
    "blog": "Write a blog post intro and title about",
}


def _do_generate(content_type: str, data: ContentRequest) -> dict:
    cfg = TYPE_CONFIG[content_type]
    messages = [
        {"role": "system", "content": cfg["system"]},
        {"role": "user", "content": f"{TASK_VERBS[content_type]}: {data.topic}\nTone: {data.tone}\nLanguage: {data.language}\n{f'Additional context: {data.extra_info}' if data.extra_info else ''}"}
    ]
    response = llm.generate(messages, max_tokens=cfg["max_tokens"])
    return {"content": response, "type": content_type, "chars": len(response)}


@app.post("/generate/linkedin")
def generate_linkedin(data: ContentRequest):
    return _do_generate("linkedin", data)


@app.post("/generate/twitter")
def generate_twitter(data: ContentRequest):
    return _do_generate("twitter", data)


@app.post("/generate/email")
def generate_email(data: ContentRequest):
    return _do_generate("email", data)


@app.post("/generate/product")
def generate_product(data: ContentRequest):
    return _do_generate("product", data)


@app.post("/generate/blog")
def generate_blog(data: ContentRequest):
    return _do_generate("blog", data)
