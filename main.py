from __future__ import annotations

import json
import logging
import re

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
    "linkedin": {"max_tokens": 400, "system": (
        "You are a professional LinkedIn content writer. Write ONLY in the requested language. "
        "Rules: never apologize, never explain yourself, never mention being an AI. "
        "Start directly with a strong 1-2 line hook. Then max 3 short paragraphs separated by blank lines. "
        "Use 2-4 relevant emojis. End with 3-5 hashtags on their own line plus a question to drive engagement. "
        "Do not invent statistics, prices, or place names.")},
    "twitter":  {"max_tokens": 150, "system": (
        "You are a viral Twitter/X content writer. Write ONLY in the requested language. "
        "Create ONE punchy tweet under 280 characters, or a short thread of max 3 tweets. "
        "Never apologize or explain yourself. No hashtags spam (max 2). Do not invent facts.")},
    "email":    {"max_tokens": 400, "system": (
        "You are a professional email copywriter. Write ONLY in the requested language. "
        "Write clear, concise, effective emails with subject line, greeting, short body, and sign-off. "
        "Never apologize or explain yourself. Start directly with the content.")},
    "product":  {"max_tokens": 300, "system": (
        "You are an expert product copywriter. Write ONLY in the requested language. "
        "Structure: catchy headline, 2-3 benefit sentences, bullet list of key features, call to action. "
        "Never apologize. Do not invent prices or specifications.")},
    "blog":     {"max_tokens": 1024, "system": (
        "You are a skilled blog writer. Write ONLY in the requested language. "
        "Structure: compelling title, engaging intro paragraph, then the article body with short paragraphs. "
        "Never apologize or explain yourself. Do not invent quotes or statistics.")},
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
    response = _postprocess(content_type, response)
    return {"content": response, "type": content_type, "chars": len(response)}


HASHTAG_LIMIT = {"linkedin": 5, "twitter": 2}


def _postprocess(content_type: str, text: str) -> str:
    """Deterministic guardrails where the small model overshoots (hashtag spam)."""
    limit = HASHTAG_LIMIT.get(content_type)
    if not limit:
        return text
    found: list[str] = []
    seen: set[str] = set()
    for m in re.finditer(r"#(\w+)", text):
        tag = m.group(1)
        if tag.lower() not in seen:
            seen.add(tag.lower())
            found.append(tag)
    text = re.sub(r"#\w+", "", text)          # strip all hashtags...
    text = re.sub(r"[ \t]+", " ", text)       # ...collapse leftover spaces...
    text = re.sub(r"\n{3,}", "\n\n", text)    # ...and blank lines
    kept = found[:limit]
    if kept:
        text = text.rstrip() + "\n\n" + " ".join(f"#{t}" for t in kept)
    return text.strip()


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
