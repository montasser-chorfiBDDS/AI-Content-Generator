import os
from dotenv import load_dotenv
from hf_client import ChatHFClient

load_dotenv()

HF_MODEL = os.getenv("HF_MODEL", "Qwen/Qwen2-0.5B-Instruct")
HF_TEMPERATURE = 0.7
HF_MAX_TOKENS = 1024

llm = ChatHFClient(model_name=HF_MODEL, temperature=HF_TEMPERATURE, max_tokens=HF_MAX_TOKENS)
