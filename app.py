import os
from datetime import datetime

import streamlit as st
import requests

st.set_page_config(page_title="AI Content Generator", page_icon="✍️")
st.title("✍️ AI Content Generator")

API_BASE = os.environ.get("API_BASE", "http://localhost:8000").rstrip("/")

st.markdown("Generate professional content for LinkedIn, Twitter, Email, Product Descriptions, and Blog Posts — powered by local AI.")

# ── Session history (newest first, capped at 20) ──
if "history" not in st.session_state:
    st.session_state.history = []

TAB_CONFIG = {
    "linkedin": {"title": "💼 LinkedIn Post Generator", "topic_label": "Topic",
                 "topic_ph": "AI in healthcare, leadership tips...",
                 "tones": ["Professional", "Inspirational", "Educational", "Conversational"],
                 "btn": "Generate LinkedIn Post", "limit": 3000},
    "twitter":  {"title": "🐦 Twitter/X Post Generator", "topic_label": "Topic",
                 "topic_ph": "Startup tips, tech trends...",
                 "tones": ["Witty", "Professional", "Casual", "Provocative"],
                 "btn": "Generate Twitter Post", "limit": 280},
    "email":    {"title": "📧 Email Generator", "topic_label": "Purpose",
                 "topic_ph": "Follow-up, proposal, thank you...",
                 "tones": ["Formal", "Friendly", "Persuasive", "Concise"],
                 "btn": "Generate Email", "limit": None},
    "product":  {"title": "📦 Product Description Generator", "topic_label": "Product name/type",
                 "topic_ph": "Smart water bottle, SaaS tool...",
                 "tones": ["Persuasive", "Professional", "Fun", "Luxury"],
                 "btn": "Generate Product Description", "limit": None},
    "blog":     {"title": "📝 Blog Post Generator", "topic_label": "Topic",
                 "topic_ph": "How to start with AI, productivity tips...",
                 "tones": ["Educational", "Thought Leadership", "How-to", "Listicle"],
                 "btn": "Generate Blog Post", "limit": None},
}


def generate_content(endpoint: str, topic: str, tone: str, language: str, extra_info: str = ""):
    """Call the backend. Timeout raised to 600s: CPU inference can take minutes."""
    with st.spinner("Generating content... (local AI, may take ~1 min)"):
        try:
            response = requests.post(
                f"{API_BASE}/generate/{endpoint}",
                json={"topic": topic, "tone": tone, "language": language, "extra_info": extra_info},
                timeout=600,
            )
            if response.status_code == 200:
                return response.json().get("content", ""), None
            return "", f"Error: {response.status_code}"
        except requests.exceptions.ConnectionError:
            return "", "Error: Backend not running. Start with: uvicorn main:app --port 8000"
        except Exception as e:
            return "", f"Error: {str(e)}"


def show_result(endpoint: str, topic: str, tone: str, language: str, content: str):
    """Display a result with char count, copy, download — and save to history."""
    n = len(content)
    limit = TAB_CONFIG[endpoint]["limit"]
    if limit:
        st.caption(f"📏 {n} / {limit} characters")
        if n > limit:
            st.warning(f"⚠️ Exceeds the recommended {limit} characters for this format.")
    else:
        st.caption(f"📏 {n} characters")

    st.code(content, language=None)  # built-in copy button
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.download_button(
        "⬇️ Download (.md)",
        data=content,
        file_name=f"{endpoint}_{ts}.md",
        mime="text/markdown",
        key=f"dl_{endpoint}_{ts}",
    )
    st.session_state.history.insert(0, {
        "type": endpoint, "topic": topic, "tone": tone,
        "language": language, "content": content,
        "time": datetime.now().strftime("%d/%m %H:%M"),
    })
    st.session_state.history = st.session_state.history[:20]


def render_tab(endpoint: str):
    cfg = TAB_CONFIG[endpoint]
    st.subheader(cfg["title"])
    topic = st.text_input(cfg["topic_label"], placeholder=cfg["topic_ph"], key=f"{endpoint}_topic")
    tone = st.selectbox("Tone", cfg["tones"], key=f"{endpoint}_tone")
    lang = st.selectbox("Language", ["English", "Arabic", "French", "Spanish"], key=f"{endpoint}_lang")
    extra = st.text_area(
        "📌 Real facts — business name, places, prices, phone (prevents AI inventions)",
        placeholder="Ex: Agence Palmera Travel, Lieux: Carthage, Sidi Bou Said. Tel +216 53 244 178",
        key=f"{endpoint}_extra",
    )
    if st.button(cfg["btn"], key=f"{endpoint}_btn"):
        if topic:
            content, err = generate_content(endpoint, topic, tone, lang, extra)
            if err:
                st.error(err)
            else:
                show_result(endpoint, topic, tone, lang, content)
        else:
            st.warning(f"Please enter {cfg['topic_label'].lower()}")


tabs = st.tabs(["💼 LinkedIn", "🐦 Twitter/X", "📧 Email", "📦 Product", "📝 Blog"])
for tab, endpoint in zip(tabs, ["linkedin", "twitter", "email", "product", "blog"]):
    with tab:
        render_tab(endpoint)

# ── History sidebar ──
with st.sidebar:
    st.header("📜 History")
    if not st.session_state.history:
        st.caption("No generations yet this session.")
    else:
        if st.button("🗑️ Clear history"):
            st.session_state.history = []
            st.rerun()
        for i, h in enumerate(st.session_state.history):
            with st.expander(f"{h['time']} — {h['type']} — {h['topic'][:30]}"):
                st.caption(f"Tone: {h['tone']} | Lang: {h['language']}")
                st.text(h["content"][:1500])
                st.download_button(
                    "⬇️ Download",
                    data=h["content"],
                    file_name=f"{h['type']}_{i}.md",
                    mime="text/markdown",
                    key=f"hist_dl_{i}",
                )
