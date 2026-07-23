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


@app.post("/generate/linkedin")
def generate_linkedin(data: ContentRequest):
    messages = [
        {"role": "system", "content": "You are a professional LinkedIn content writer. Create engaging, valuable posts."},
        {"role": "user", "content": f"Write a LinkedIn post about: {data.topic}\nTone: {data.tone}\nLanguage: {data.language}\n{f'Additional context: {data.extra_info}' if data.extra_info else ''}"}
    ]
    response = llm.generate(messages)
    return {"content": response, "type": "linkedin"}


@app.post("/generate/twitter")
def generate_twitter(data: ContentRequest):
    messages = [
        {"role": "system", "content": "You are a viral Twitter/X content writer. Create punchy, engaging tweets or threads."},
        {"role": "user", "content": f"Write a Twitter post or thread about: {data.topic}\nTone: {data.tone}\nLanguage: {data.language}\n{f'Additional context: {data.extra_info}' if data.extra_info else ''}"}
    ]
    response = llm.generate(messages)
    return {"content": response, "type": "twitter"}


@app.post("/generate/email")
def generate_email(data: ContentRequest):
    messages = [
        {"role": "system", "content": "You are a professional email copywriter. Write clear, concise, and effective emails."},
        {"role": "user", "content": f"Write a professional email about: {data.topic}\nTone: {data.tone}\nLanguage: {data.language}\n{f'Additional context: {data.extra_info}' if data.extra_info else ''}"}
    ]
    response = llm.generate(messages)
    return {"content": response, "type": "email"}


@app.post("/generate/product")
def generate_product(data: ContentRequest):
    messages = [
        {"role": "system", "content": "You are an expert product copywriter. Write compelling product descriptions that convert."},
        {"role": "user", "content": f"Write a product description for: {data.topic}\nTone: {data.tone}\nLanguage: {data.language}\n{f'Additional context: {data.extra_info}' if data.extra_info else ''}"}
    ]
    response = llm.generate(messages)
    return {"content": response, "type": "product"}


@app.post("/generate/blog")
def generate_blog(data: ContentRequest):
    messages = [
        {"role": "system", "content": "You are a skilled blog writer. Create engaging blog intros, titles, and hooks."},
        {"role": "user", "content": f"Write a blog post intro and title about: {data.topic}\nTone: {data.tone}\nLanguage: {data.language}\n{f'Additional context: {data.extra_info}' if data.extra_info else ''}"}
    ]
    response = llm.generate(messages)
    return {"content": response, "type": "blog"}
