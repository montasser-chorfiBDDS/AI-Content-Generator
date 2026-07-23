import os
import streamlit as st
import requests

st.set_page_config(page_title="AI Content Generator", page_icon="✍️")
st.title("✍️ AI Content Generator")

API_BASE = os.environ.get("API_BASE", "http://localhost:8000").rstrip("/")

st.markdown("Generate professional content for LinkedIn, Twitter, Email, Product Descriptions, and Blog Posts — powered by local AI.")

tab_linkedin, tab_twitter, tab_email, tab_product, tab_blog = st.tabs([
    "💼 LinkedIn", "🐦 Twitter/X", "📧 Email", "📦 Product", "📝 Blog"
])

def generate_content(endpoint: str, topic: str, tone: str, language: str, extra_info: str = ""):
    with st.spinner("Generating content..."):
        try:
            response = requests.post(
                f"{API_BASE}/generate/{endpoint}",
                json={"topic": topic, "tone": tone, "language": language, "extra_info": extra_info},
                timeout=120
            )
            if response.status_code == 200:
                return response.json().get("content", "")
            else:
                return f"Error: {response.status_code}"
        except requests.exceptions.ConnectionError:
            return "Error: Backend not running. Start with: uvicorn main:app --port 8000"
        except Exception as e:
            return f"Error: {str(e)}"

with tab_linkedin:
    st.subheader("💼 LinkedIn Post Generator")
    li_topic = st.text_input("Topic", placeholder="AI in healthcare, leadership tips...")
    li_tone = st.selectbox("Tone", ["Professional", "Inspirational", "Educational", "Conversational"], key="li_tone")
    li_lang = st.selectbox("Language", ["English", "Arabic", "French", "Spanish"], key="li_lang")
    li_extra = st.text_area("Additional context (optional)", placeholder="Target audience, key points to include...", key="li_extra")
    if st.button("Generate LinkedIn Post", key="li_btn"):
        if li_topic:
            result = generate_content("linkedin", li_topic, li_tone, li_lang, li_extra)
            st.text_area("Generated Content", value=result, height=400)
        else:
            st.warning("Please enter a topic")

with tab_twitter:
    st.subheader("🐦 Twitter/X Post Generator")
    tw_topic = st.text_input("Topic", placeholder="Startup tips, tech trends...", key="tw_topic")
    tw_tone = st.selectbox("Tone", ["Witty", "Professional", "Casual", "Provocative"], key="tw_tone")
    tw_lang = st.selectbox("Language", ["English", "Arabic", "French", "Spanish"], key="tw_lang")
    tw_extra = st.text_area("Additional context (optional)", key="tw_extra")
    if st.button("Generate Twitter Post", key="tw_btn"):
        if tw_topic:
            result = generate_content("twitter", tw_topic, tw_tone, tw_lang, tw_extra)
            st.text_area("Generated Content", value=result, height=400)
        else:
            st.warning("Please enter a topic")

with tab_email:
    st.subheader("📧 Email Generator")
    em_topic = st.text_input("Purpose", placeholder="Follow-up, proposal, thank you...", key="em_topic")
    em_tone = st.selectbox("Tone", ["Formal", "Friendly", "Persuasive", "Concise"], key="em_tone")
    em_lang = st.selectbox("Language", ["English", "Arabic", "French", "Spanish"], key="em_lang")
    em_extra = st.text_area("Recipient info / context", key="em_extra")
    if st.button("Generate Email", key="em_btn"):
        if em_topic:
            result = generate_content("email", em_topic, em_tone, em_lang, em_extra)
            st.text_area("Generated Content", value=result, height=400)
        else:
            st.warning("Please enter a purpose")

with tab_product:
    st.subheader("📦 Product Description Generator")
    pr_topic = st.text_input("Product name/type", placeholder="Smart water bottle, SaaS tool...", key="pr_topic")
    pr_tone = st.selectbox("Tone", ["Persuasive", "Professional", "Fun", "Luxury"], key="pr_tone")
    pr_lang = st.selectbox("Language", ["English", "Arabic", "French", "Spanish"], key="pr_lang")
    pr_extra = st.text_area("Key features / target audience", key="pr_extra")
    if st.button("Generate Product Description", key="pr_btn"):
        if pr_topic:
            result = generate_content("product", pr_topic, pr_tone, pr_lang, pr_extra)
            st.text_area("Generated Content", value=result, height=400)
        else:
            st.warning("Please enter a product")

with tab_blog:
    st.subheader("📝 Blog Post Generator")
    bg_topic = st.text_input("Topic", placeholder="How to start with AI, productivity tips...", key="bg_topic")
    bg_tone = st.selectbox("Tone", ["Educational", "Thought Leadership", "How-to", "Listicle"], key="bg_tone")
    bg_lang = st.selectbox("Language", ["English", "Arabic", "French", "Spanish"], key="bg_lang")
    bg_extra = st.text_area("Target audience / key points", key="bg_extra")
    if st.button("Generate Blog Post", key="bg_btn"):
        if bg_topic:
            result = generate_content("blog", bg_topic, bg_tone, bg_lang, bg_extra)
            st.text_area("Generated Content", value=result, height=400)
        else:
            st.warning("Please enter a topic")
